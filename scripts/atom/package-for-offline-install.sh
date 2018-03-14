#!/bin/sh


ATOM_PKG=$1
URL=$2
EXT=tar.gz

echo "Downloading package..."
echo "wget -O ${ATOM_PKG}.${EXT} ${URL}"
wget -O $ATOM_PKG.$EXT $URL

echo "Extracting package..."
echo "tar -xvf ${ATOM_PKG}.${EXT}"
tar -xvf $ATOM_PKG.$EXT

echo "Installing npm packages..."
cd $ATOM_PKG
npm install

cd ..
echo "Removing original package..."
rm $ATOM_PKG.$EXT

echo "Creating package with bundled dependencies..."
tar -cvf $ATOM_PKG.tar $ATOM_PKG

echo "Removing package directory..."
rm -rf $ATOM_PKG

echo "Gzipping package..."
gzip $ATOM_PKG.tar

