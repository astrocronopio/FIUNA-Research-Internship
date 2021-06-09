#Borra las líneas en blanco y las líneas sin datos

datafile="../../../Local-Machine/Datasets/Muons/raw_muones.txt"
output_file="../../../Local-Machine/Datasets/Muons/muons_deleted_spaces.txt"

awk '{if(NF>140) print $0}' "$datafile" > "$output_file"