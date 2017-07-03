#!/usr/bin/env bash

## produce data for this example
./produce_data.py

## tune quadratic linear discriminant
hepstore-school -c qda -f $(pwd)/data_1.npy $(pwd)/data_2.npy \
		-l 0.0 1.0 --only_explore \
		--random_state 7 \
		--path $(pwd)/tuning

## which yields:--QDA: explore
#--info: RandomizedSearchCV took 24.36 seconds for 200 candidates parameter settings.
#--info: Model with rank: 1
#--info: Mean validation score:  8.06e-01 (std:  3.28e-03)
#--info: Parameters: {'reg_param': 0.0027454802945078294, 'tol': 0.00072971227653656045}
#--info: Model with rank: 2
#--info: Mean validation score:  8.05e-01 (std:  3.19e-03)
#--info: Parameters: {'reg_param': 0.00862957001583331, 'tol': 0.00068120836729054681}
#--info: Model with rank: 3
#--info: Mean validation score:  8.05e-01 (std:  3.19e-03)
#--info: Parameters: {'reg_param': 0.014999438477383165, 'tol': 0.00091459513377715248}

## plot cross validation
vars=('reg_param' 'tol')
for var in ${vars[@]} ; do
    hepstore-plot -f $(pwd)/tuning/train_scores_${var}.npy \
		  $(pwd)/tuning/test_scores_${var}.npy \
		  -k errorband --logx \
		  --legend 'train' 'test' \
		  -c yellow blue \
		  --title "Cross validation QDA" \
		  --xlabel "$var" \
		  --ylabel 'score' \
		  --path $(pwd)/$var.pdf
done

## perform the actuall machine learning
hepstore-school -c qda -f $(pwd)/data_1.npy $(pwd)/data_2.npy \
		-l 0.0 1.0 \
		--reg_param 0.002745 --tol 0.0007291 \
		--random_state 7 \
		--path $(pwd)/learning

## ROC curve
hepstore-plot -f $(pwd)/learning/roc.npy -k line \
	      --legend 'ROC' \
	      -c black \
	      --ymax 1.1 \
	      --title "ROC curve QDA" \
	      --xlabel '$\epsilon_{S}$' \
	      --ylabel '$1-\epsilon_{B}$' \
	      --path $(pwd)/roc.pdf

## probability map
hepstore-plot -f $(pwd)/data_1.npy $(pwd)/data_2.npy \
	      $(pwd)/learning/probability_map.npy \
	      -k "2*scatter" contour \
	      -c blue red Blues \
	      --xmin -5 --ymin -5 --xmax 5 --ymax 5 \
	      --alpha 0.3 \
	      --legend 'background' 'signal' \
	      --title "probability map QDA" \
	      --path $(pwd)/probability_map.pdf

