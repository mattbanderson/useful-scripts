#!/bin/sh
set -e

if [ "$1" != "" ]; then
  cd $1
fi

npm ll --parseable | sed 's#\(.*\):\(.*\):\(.*\)#npm install \2#;w ./install-packages.sh'
mkdir -p ./npm-cache-mirror
mv ./install-packages.sh ./npm-cache-mirror
cd ./npm-cache-mirror
npm cache clean --force
chmod +x ./install-packages.sh 
./install-packages.sh
cd ../
rm -rf npm-cache-mirror
