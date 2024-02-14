#!/bin/bash

image_name="descs-standalone"
if ! docker image inspect "$image_name" &> /dev/null; then
	docker load -i /app/descs-standalone.tar -q &> /dev/null
fi

core_path=/tmp/$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 13 ; echo '';)
# script_directory=/home/antczak;
rm $core_path"/descs" -r 2> /dev/null;
mkdir -p $core_path"/descs";

filename="${1##*/}"
filename="${filename%.*}"

cp $1 $core_path"/descs/file.pdb";
cd $core_path"/descs";
cp /app/in-contact-residues-identification-based-on-c5prim-only.exp $core_path
docker run --rm \
-v $core_path:/tmp/ descs-standalone \
--execution-mode DESCRIPTORS_BUILDING \
--input-file "/tmp/descs/file.pdb" \
--molecule-type RNA \
--in-contact-residues-expression-file /tmp/in-contact-residues-identification-based-on-c5prim-only.exp \
> $core_path/descs/results.txt
awk 'BEGIN {FS="\t";} NF==7 {printf("%s\t%s\t%s\t%s\t%s\t%s\n",$2,$3,$4,$5,$6,$7);}' <  $core_path"/descs/"results.txt >  $core_path"/descs/"filter-results.txt
echo -e "num_of_segs\tresidue_range\tsequence\tdescriptor_name\tfile_path"
while IFS=$'\t' read -r col1 col2 col3 col4 col5 col6; do
    echo -ne "$col2\t"
    echo -ne "$col5\t"
    echo -ne "$col6\t"
    descriptor_path=$(find "$core_path/descs/out/" -wholename "*${col1}.pdb" -printf "%p")
	descriptor_name="${descriptor_path##*/}"
	descriptor_name="${descriptor_name%.*}"
    echo -ne "$filename${descriptor_name:4}\t"
	echo -ne "$descriptor_path\n"
done < "$core_path/descs/filter-results.txt"
