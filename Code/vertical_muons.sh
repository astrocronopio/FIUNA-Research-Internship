#Written by: Evelyn Coronel

# Se  ejecuta como bash vertical_muons.sh

datafile="../../Local-Machine/Datasets/datos/muones.txt"
output_file="../../Local-Machine/Datasets/datos/vertical_total_muons.txt"


# $1 - column: UTC time, interval 10 seconds

# Columns of vertical muons data

# $15,  $28,  $41,  $54,  $67,  $80,  $91,  $106, $119, $132,   $145
# A1B1, A2B2, A3B3, A4B4, A5B5, A6B6, A7B7, A8B8, A9B9, A10B10, A11B11 

#It makes sense after seeing  detector.jpeg 

# -F',' le dice que las columnas estan separadas con comas

awk -F',' '{  if($0) # if not empty 
                {   
                    sum_total=0; 
                    sum_vertical=0;

                    for (i=2; i<=NF; i++) 
                        { sum_total+= $i };

                    sum_vertical = $15 +  $28 + $41 +  $54 + $67 + $80 + $91 +  $106 + $119 + $132 + $145
                
                    print  $1 , sum_vertical, sum_total
                }
                
                }' "$datafile" > "$output_file"
                    #input        #output  

                    # No se porque no funciona
                    # for (j=15; j<=NF; j+=13) 
                    #     { sum_vertical+= $j }