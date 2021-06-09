datafile="../../../Local-Machine/Datasets/rtsw_plot_data_30-min_bin.txt"
outfile="../../../Local-Machine/Datasets/rtsw_utc_plot_data_30-min_bin.txt"

#Timestamp     Source    Bt-med    Bt-min    Bt-max    Bx-med    Bx-min    
#1  2             3        4          5       6           7       8

#Bx-max    By-med    By-min    By-max    Bz-med    Bz-min    Bz-max  
# 9       10          11      12          13      14            15

#Phi-mean   Phi-min   Phi-max  Theta-med Theta-min Theta-max  Dens-med  
#  16          17      18          19      20          21     22

#Dens-min  Dens-max Speed-med Speed-min Speed-max  Temp-med  Temp-min  Temp-max
#  23          24      25          26          27      28          29        


awk '{system("date -d \x27"  $1 " " $2 "\x27  +\x22%s " $16 "\x22")}' "$datafile" >  "$outfile"