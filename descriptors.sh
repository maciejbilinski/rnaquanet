#!/bin/bash

core_path=$(pwd)/$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo '';)
script_directory=/home/antczak;
rm $core_path"/descs" -r 2> /dev/null;
mkdir -p $core_path"/descs" && cd $core_path"/descs";

cp $1 $core_path"/descs/file.pdb"
cp /app/in-contact-residues-identification-based-on-c5prim-only.exp $core_path
docker run --rm -e DB_HOST="172.17.0.1" -v $core_path:/tmp/ --entrypoint ./descs descs-standalone --execution-mode DESCRIPTORS_BUILDING --input-file "/tmp/descs/file.pdb" --molecule-type rna --in-contact-residues-expression-file /tmp/in-contact-residues-identification-based-on-c5prim-only.exp > $core_path/descs/results.txt
awk 'BEGIN {FS="\t";} NF==7 {printf("%s,%s,\n",$2,$3);}' <  $core_path"/descs/"results.txt >  $core_path"/descs/"filter-results.txt
for i in $(cat  $core_path"/descs"/filter-results.txt )
do
	arrIN=(${i//,/ })
	echo -n ${arrIN[1]}" "
	echo $(find $core_path"/descs/out/" -wholename "*"${arrIN[0]}".pdb" -printf "%p" ) 
done


