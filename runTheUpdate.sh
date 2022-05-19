#!/bin/bash

# Basic defaults
pulsheDir="/data/pulshe/"
pulsheDir="/home/nraja/work/"
orgGram="ppd_organogram.json"
locTrainDir="training"


cd $pulsheDir"/pulshe"
today=`date -I`

echo "Tidy up training directory locally"
mv $locTrainDir $locTrainDir"-"$today
mkdir $locTrainDir

echo "Actually generate the trainings - assume that the needed files are"
echo "downloaded and properly located already"
./generateTrainings.sh

echo"Moving the training directory into final location"
trainDir=$pulsheDir$locTrainDir"/ppd"
mv $trainDir $trainDir"-"$today
cp -Rp $locTrainDir $trainDir

echo "Copy the organogram into prod area"
cp $orgGram $pulsheDir"/prod/ppd"
