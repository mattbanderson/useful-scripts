#!/bin/sh

docker_img=$1

# split image name on forward slash
IFS='/' read -a img_parts <<< "$docker_img"

# use split image name to build output file name
outfile=${img_parts[0]}-${img_parts[1]}.tar

split_prefix=$outfile-part-

echo 'Pulling docker image...'
sudo docker pull $docker_img
echo 'Docker pull complete.'

echo 'Saving docker image...'
sudo docker save $docker_img -o $outfile
sudo chmod +r  $outfile
echo 'Docker save complete.'

echo 'Splitting files...'
split -b 21m $outfile $split_prefix
rm -f $outfile
echo 'Split complete.'

echo 'Base64 encoding...'
for FILE in ./$split_prefix*
do
    base64 $FILE > $FILE.txt
    rm -f $FILE
done
echo 'Base64 encode complete.'

echo 'Zipping Base64 encoded splits...'
zip $outfile.txt.zip $split_prefix*
rm -f $split_prefix*
echo 'Zip complete.'

