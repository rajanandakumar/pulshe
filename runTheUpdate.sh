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

tmp=`grep optionalTrainings configuration.py | awk -F ":" '{print $2}' | cut -b 2-5`
if [ $tmp == "True" ]; then
	echo "Moving the training directory into final location"
	trainDir=$pulsheDir$locTrainDir"/ppd"
	mv $trainDir $trainDir"-"$today
	cp -Rp $locTrainDir $trainDir

	echo "Copy the organogram into prod area"
	cp $orgGram $pulsheDir"/prod/ppd"
else
	echo "Updates to mandatory training only. Not moving to production area."
fi
