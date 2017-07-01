#!/usr/bin/env bash

## produce data for this example
./produce_data.py

## plot scatter
hepstore-plot -f data_1.npy data_2.npy -k scatter \
	      -c blue red \
	      --xmin -5 --xmax 5 \
	      --ymin -5 --ymax 5 \
	      --legend 'single gaussian' 'double gaussian' \
	      --alpha 0.6 \
              --title 'example plot a.)' 'scatter'\
	      --path $(pwd)/example_a.pdf

## plot histogram of x axis
hepstore-plot -f data_1.npy data_2.npy -k histogram \
	      -a 0 \
	      -c blue red \
	      --normed \
	      --bins 20 \
	      --xmin -5 --xmax 5 \
	      --ymax 0.6 \
	      --ylabel '$\rho(x)$' \
	      --legend 'single gaussian' 'double gaussian' \
	      --alpha 0.6 \
	      --title 'example plot b.)' 'histogram'\
	      --path $(pwd)/example_b.pdf

## plot histogram of x axis
hepstore-plot -f data_1.npy data_2.npy -k histogram \
	      -a 1 \
	      -c blue red \
	      --normed \
	      --bins 20 \
	      --xmin -5 --xmax 5 \
	      --ymax 0.6 \
	      --xlabel 'y' \
	      --ylabel '$\rho(y)$' \
	      --legend 'single gaussian' 'double gaussian' \
	      --alpha 0.6 \
	      --title 'example plot c.)' 'histogram'\
	      --path $(pwd)/example_c.pdf




