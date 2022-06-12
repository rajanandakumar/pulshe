#!/bin/bash

# Basic defaults
pulsheDir="/data/pulshe/"
orgGram="ppd_organogram.json"
locTrainDir="training"

cd $pulsheDir"/pulshe"
end_date=`date -I`
today=`date '+%C%y%m%d' -d "$end_date-7 days"`

echo "Tidy up training directory locally"
mv $locTrainDir $locTrainDir"-"$today
mkdir $locTrainDir

echo "Actually generate the trainings - assume that the needed files are"
echo "downloaded and properly located already"
./generateTrainings.sh

echo "Moving the training directory into final location"
trainDir=$pulsheDir$locTrainDir"/ppd"
sudo mv $trainDir $trainDir"-"$today
sudo cp -Rp $locTrainDir $trainDir

echo "Copy the organogram into prod area"
sudo cp $orgGram $pulsheDir"/prod/ppd"
