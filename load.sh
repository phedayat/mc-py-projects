#!/bin/bash
device=$(rshell boards | grep -oh "/dev/\w*.\w*" | head -1)

if [[ -c "$device" ]]; then
	echo "Device found: $device"
	export AMPY_PORT=$device
else
	echo "[ERROR] Device not found. Check if the connection is secure or if you've loaded in bootloader mode"
	exit 1
fi

projectRoot=$1

currentProjItems=$(find $projectRoot -maxdepth 1 -regex "$projectRoot/.*")
echo "Collected project files and dirs from $projectRoot..."

currentPicoFiles=$(ampy ls)
echo "Collected files currently onboard the Pico..."

# TODO Add if-statement here and corresponding option
#	for `update`, meaning we don't need to clear
#	the Pico

for i in $currentPicoFiles; do
	if [[ -d "$i" ]]; then
		ampy rmdir $i
	else
		ampy rm $i
	fi
done
echo "Removed all files from Pico..."

for i in $currentProjItems; do
	ampy put $i
done
echo "Put all files from $projectRoot onboard the Pico"

echo "Project loaded. You may now disconnect the board."

