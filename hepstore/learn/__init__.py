import os

from hepstore.learn.analysis import *
from hepstore.eas.fileIO import *
from hepstore.eas.unbinned import *

############################################################################
## run the app
############################################################################
def run():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to learn from the EAS results with python 2.7.")

    # setup arg parser    
    parser = argparse.ArgumentParser(description='main steering program for machine learning')
    parser.add_argument("-f", "--file", default=[],
                        help="list of data files to be analysed, including identifier of the data object in file label, e.g  'filepath:uniquename:x_rho:s' or 'filepath:uniquename:x_rho:b' for signal vs background",
                        required=True, nargs='+')
    parser.add_argument(      "--random_state", default=0, type=int,           help="random state for machine learning")
    parser.add_argument(      "--test_size",    default=0.25, type=float,      help="realtive size of test sample")
    parser.add_argument("-c", "--classifier",   default="svc", type=str,       help="machine learning algorithm")
    parser.add_argument(      "--figure",       default=os.getcwd(),           help="folder to save output figure")
    parser.add_argument(      "--luminosity",   default=2000., type=float,     help="luminosity for analysis")
    parser.add_argument(      "--crossection",  default=[0.5,0.5], type=float, help="crossection for signal and background", nargs='+')
    parser.add_argument(      "--enhance_data", default=[0.,0.,0.], type=float,       help="enhance data by [int_num,spread_x,spread_y, etc]",nargs='+')
    parser.add_argument(      "--ntotal",       default=1000,                  help="number of total expected events")
    parser.add_argument(      "--use_labels",   default=['s','b'],             help="labels for statistical analysis", nargs='+')

    # parse args   
    args = parser.parse_args()

    # analysis object
    analysis = DataAnalysis(random_state=args.random_state,test_size=args.test_size,classifier=args.classifier,luminosity=args.luminosity,crossection=args.crossection)

    # loop through data files
    for item in args.file:
        fname = os.path.dirname(item.split(":")[0])
        uname = item.split(":")[1]
        dname = item.split(":")[2]
        label = item.split(":")[3]
        # load data
        areader = reader(fname)
        thefile = unbinned(dname)
        areader.read(thefile)
        thedata = DataUnit(name=uname)
        thedata.loadFromUnbinned(thefile,label)
        thedata.enhance(args.enhance_data)
        analysis.addData(thedata)
        pass

    ## prepare run
    analysis.enhance    = args.enhance_data[0]
    analysis.ntotal     = args.ntotal
    analysis.use_labels = args.use_labels
    analysis.prepare()
    
    ## train and test
    analysis.train()
    analysis.test()
    
    ## plot results
    analysis.plot(args.figure)
    
    ## print results
    print analysis
    
    pass # run
############################################################################

