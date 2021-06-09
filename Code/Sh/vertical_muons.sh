#Written by: Evelyn Coronel

# Se  ejecuta como bash vertical_muons.sh

# datafile="../../../Local-Machine/Datasets/muones_30-min_bin.txt"
# output_file="../../../Local-Machine/Datasets/vertical_total_muons_30-min_bin.txt"

# datafile="../../../Local-Machine/Datasets/muones_1h_bin.txt"
# output_file="../../../Local-Machine/Datasets/vertical_total_muons_1h_bin.txt"


# $1 - column: UTC time, interval 10 seconds

##### Columns of vertical muons data #######

# $15,  $28,  $41,  $54,  $67,  $80,  $93,  $106, $119, $132,   $145
# A1B1, A2B2, A3B3, A4B4, A5B5, A6B6, A7B7, A8B8, A9B9, A10B10, A11B11 

#It makes sense after seeing  detector.jpeg 


#### Special columns #####

#$22     $20     #70     #68      #105     #77     $127      $125
#A1B8   #A1B6   #A5B8   #A5B6    $A8B7    $A6B3   $A10B5    $A10B3



# -F',' le dice que las columnas estan separadas con comas

awk -F',' '{  if($0) # if not empty (empty line)
                {   
                    sum_total=0; 
                    sum_vertical=0;
                    sum_special=0;

                    for (i=2; i<=NF; i++) 
                        { sum_total+= $i };

                    sum_vertical = $15 +  $28 + $41 +  $54 + $67 + $80 + $93 +  $106 + $119 + $132 + $145
                    sum_special = $22  +  $20 + $70 +  $68 + $105+ $77 + $127+  $125
                    
                    print  $1 , sum_vertical, sum_special, sum_total, $22, $20, $70, $68, $105, $77, $127,  $125
                }
                
                }' "$datafile" > "$output_file"
                    #input        #output  

                    # No se porque no funciona
                    # for (j=15; j<=NF; j+=13) 
                    #     { sum_vertical+= $j }