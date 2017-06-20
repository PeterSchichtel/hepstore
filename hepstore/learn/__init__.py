import os

import analysis

############################################################################
## run the app
############################################################################
def run():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to learn from data in .npy format")

    # setup arg parser    
    parser.add_argument("-f", "--file", default=[],
                        help="list of data files to be learned from (.npy format)",
                        required=True, nargs='+')
    # main options
    parser.add_argument("-l", "--label", default=["1*1.0"],
                        help="cycle to be used for data labels in classification, understands multiplication",
                        nargs='+',
                        type=str)
    
    parser.add_argument(      "--random_state", default=0, type=int,           help="random state for machine learning")
    parser.add_argument(      "--test_size",    default=0.25, type=float,      help="realtive size of test sample")
    parser.add_argument("-c", "--classifier",   default="svc", type=str,       help="machine learning algorithm")
    parser.add_argument(      "--luminosity",   default=2000., type=float,     help="luminosity for analysis")
    parser.add_argument(      "--crossection",  default=[0.5,0.5], type=float, help="crossection for signal and background", nargs='+')
    parser.add_argument(      "--ntotal",       default=1000,                  help="number of total expected events")
    parser.add_argument(      "--path",         default=os.getcwd(),           help="where to save results")

    # parse args   
    args = parser.parse_args()

    # learn from data
    analysis = analysis.analysis(args)
    analysis.run()
    
    pass # run
############################################################################

