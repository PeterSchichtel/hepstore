#!/usr/bin/env python

import os
import school

############################################################################
## run the app
############################################################################
def main():

    # we need to setup the arg parser
    import argparse
    parser = argparse.ArgumentParser(description="This App allows to learn from data in .npy format")

    # setup arg parser    
    parser.add_argument("-f", "--file", default=[],
                        help="list of data files to be learned from (.npy format)",
                        required=True, nargs='+',
                        type=str)
    # main options
    parser.add_argument("-l", "--label", default=["1*1.0","1*0.0"],
                        help="cycle to be used for data labels in classification, understands multiplication",
                        required=True, nargs='+',
                        type=str)
    
    parser.add_argument(      "--random_state",      default=0,           type=int,    help="random state for machine learning")
    parser.add_argument(      "--test_size",         default=0.25,        type=float,  help="realtive size of test sample")
    parser.add_argument("-c", "--classifier",        default="svc",       type=str,    help="machine learning algorithm")
    parser.add_argument("-p", "--path",              default=os.getcwd(), type=str,    help="where to save results")
    parser.add_argument(      "--points",            default=2000,        type=int,    help="number of support points for probability map creation")
    parser.add_argument(      "--zoom",              default=0.15,        type=float,  help="zoom values for probability map creation")
    parser.add_argument("-e", "--explore",           action='store_true',              help="explore the classifier before training it")
    parser.add_argument(      "--only_explore",      action='store_true',              help="explore the classifier without training it")
    parser.add_argument(      "--signal_labels",     default=["1.0"],     type=str,    help="specify labels used as signal in ROC curve")
    parser.add_argument(      "--background_labels", default=["0.0"],     type=str,    help="specify labels used as background in ROC curve")

    # parse args   
    args = parser.parse_args()

    # learn from data
    teacher = school.Teacher(args)
    teacher.teach()
    teacher.save()
    
    pass # run
############################################################################

############################################################################
## make executable script
############################################################################
if __name__ == "__main__":
    main()
    pass
############################################################################

