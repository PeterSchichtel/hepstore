#!/usr/bin/env python



class analysis(object):

    def __init__(self,options):
        self.options = options
        self.student = None
        # create cyclers for options
        self.label = cycle(tools.options_to_list(options.label))
        pass

    def run(self):
        # load data
        for fin in self.options.file:
            raw_data = np.load(fin)
            data     = dataunit(raw_data,[next(self.label)]*len(raw_data))
            if self.student == None:
                self.student = student(self.options,data)
                pass
            else:
                self.student.add_data(data)
                pass
            pass
        # train student
        self.student.prepare()
        self.student.train()
        self.student.test()
        # save results and cross checks
        self.save()
        pass

    def save(self):
        tools.mkdir(self.options.path)
        # preparation results
        if self.options.explore:
            pass
        # training data
        np.save(os.path.join(self.options.path,"data_train.npy")     ,self.student.data_train)
        np.save(os.path.join(self.options.path,"label_train.npy")    ,self.student.label_train)
        # testing data
        np.save(os.path.join(self.options.path,"data_test.npy")      ,self.student.data_test)
        np.save(os.path.join(self.options.path,"label_test.npy")     ,self.student.label_test)
        # classifier map
        np.save(os.path.join(self.options.path,"probability_map.npy"),self.probability_map())
        # ROC
        np.save(os.path.join(self.options.path,"roc.npy")            ,self.roc())
        # significance
        np.save(os.path.join(self.options.path,"significance.npy")   ,self.significance())
        # info on screen
        print self
        pass

    def probability_map(self):
        data   = np.concatenate((self.student.data_train,self.student.data_test))
        field  = []
        ranges = []
        # define a range with x% zoom for better plotting
        for i in range(0,data.shape[1]):
            values = [min(data[:,i]),max(data[:,i])]
            zoom   = self.options.zoom*abs(values[1]-values[0])
            values = [values[0]-zoom,values[1]+zoom]
            ranges.append(values)
            pass
        # create support points randomly
        for i in range(0,self.options.points):
            point = []
            for arange in ranges:
                point.append(np.random.uniform(arange[0],arange[1]))
                pass
            field.append(point)
            pass
        # fill field with classifier responce
        result = []
        for classification,coordinates in zip(self.student.classifier.predict_proba(self.student.scaler.transform(field))[:,1:],field):
            result.append(([classification[0]]+coordinates))
            pass
        return np.array(result)

    def efficiency(self,is_signal,bins=1000):
        # load data
        data_scaled = np.concatenate((self.student.data_train_scaled, self.student.data_test_scaled))
        labels      = np.concatenate((self.student.label_train      , self.student.label_test))
        data        = {}
        for label in np.unique(labels):
            data[label] = []
            pass
        for label,classification in zip( labels, self.student.classifier.predict_proba( data_scaled ) ):
            data[label].append(classification[0])
            pass
        # collect signal and background
        results     = None
        for label in data:
            if not is_signal or label in self.options.signal:
                if results == None:
                    results = data[label]
                    pass
                else:
                    results = np.concatenate((results,data[label]))
                    pass
                pass
            pass
        # compute signal and background efficiencies
        return np.histogram(results,bins=bins,range=(0,1),normed=True)
        
    def roc(self,bins=1000):
        delta       = 1./float(bins) 
        counts_signal    , bin_edges_signal     = self.efficiency(True ,bins=bins)
        counts_background, bin_edges_background = self.efficiency(False,bins=bins)
        # generate ROC
        points = []
        for i in range(0,bins):
            x = sum(counts_signal[:i])*delta
            y = 1.0 - sum(counts_background[:i])*delta
            points.append([x,y])
            pass
        return np.array(points)
    
    def significance(self,bins=1000):
        delta       = 1./float(bins) 
        counts_signal    , bin_edges_signal     = self.efficiency(True ,bins=bins) 
        counts_background, bin_edges_background = self.efficiency(False,bins=bins)
        # generate significance curve
        points = []
        for i in range(0,bins):
            es  = sum(counts_signal[:i]    )*delta
            eb  = sum(counts_background[:i])*delta
            if es>0.0 or eb>0.0:
                sig = np.sqrt( (self.options.luminosity * es**2 * self.options.crossection[0]**2 )/( es * self.options.crossection[0]  +  eb * self.options.crossection[1] ) )
                pass
            else:
                sig = 0.0
                pass
            points.append([es,sig])
            pass
        return np.array(points)

    
    def maximum_significance(self,bins=1000):
        sig   = max(      self.significance(bins=bins)[:,1])
        index = np.argmax(self.significance(bins=bins)[:,1])
        es    =           self.significance(bins=bins)[index,0]
        return (sig,es,index)
    
    def two_sigma_luminosity(self,bins=1000):
        max_s,max_es,index = self.maximum_significance(bins=bins)
        max_eb             = self.efficiency(False,bins=bins)[0][index]
        return 4.0 * ( max_es * self.options.crossection[0]  +  max_eb * self.options.crossection[1] ) / ( max_es**2 * self.options.crossection[0]**2 )
    
    def excluded_crossection(self,bins=1000):
        # save signal cross section
        old_signal_crossection           = self.options.crossection[0]
        # scan signal modifier to find maximum significance of 2
        if self.maximum_significance(bins=bins)[0]<2.0:
            while self.maximum_significance(bins=bins)[0]<2.0:
                self.options.crossection[0] *= 1.1
                pass
            pass
        else:
            while self.maximum_significance(bins=bins)[0]>2.0:
                self.options.crossection[0] *= 0.9
                pass
            pass
        exclusion_limit                  = self.options.crossection[0]
        self.options.crossection[0]      = old_signal_crossection
        return exclusion_limit
    
    def __str__(self):
        thestr = "--analysis: sigma = %f at epsilon_s = %f  \n" % self.maximum_significance()[0:2]
        thestr+= "--analysis: lumi  = %f at sigma     = 2.0 \n" % self.two_sigma_luminosity()
        thestr+= "--analysis: excluded above xsec = %f  " % self.excluded_crossection()
        return thestr
    
    pass
 
