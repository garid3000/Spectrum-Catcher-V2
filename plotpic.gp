set datafile separator ','
set title 'tite'
set ylabel 'digital'
set xlabel 'wavelegnth'
set yrange [0:255]
set grid
set term png
set output ofname
plot for [col=1:2] ifname using 0:col with lines title columnheader
