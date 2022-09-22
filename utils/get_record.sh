# Gets records from shapefile
file=$1
location=$2
length=$3

hexdump $file -s $location -n $length -C | cut -d ' ' -f2-20