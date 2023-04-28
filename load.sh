#!/bin/bash
check_for_device(){
	device=$(rshell boards | grep -oh "/dev/\w*.\w*" | head -1)
	if [[ -c "$device" ]]; then
		echo "[  DEV  ] Device found: $device"
		export AMPY_PORT=$device
	else
		echo "[ERROR] Device not found. Check if the connection is secure or if you've loaded in bootloader mode"
		exit 1
	fi
}

collect_project_items(){
	echo "[   1   ] Collecting project items from $projectRoot..."
	projItems=$(find $projectRoot -maxdepth 1 -regex "$projectRoot/.*")
	echo "[SUCCESS] Collected project items from $projectRoot..."
}

# [TODO] Add getopt for `update`, i.e. don't clear the Pico
remove_pico_items(){
	echo "[   2   ] Removing all files from Pico..."
	ampy reset
	echo "[SUCCESS] Removed all files from Pico."
}

loading_pico(){
	echo "[   3   ] Loading all files from $projectRoot onboard the Pico"
	for i in "$@"; do
		ampy put $i
	done
	echo "[SUCCESS] Loaded all files from $projectRoot onboard the Pico"
}

check_for_device

projectRoot=$1
projItems=()

collect_project_items

remove_pico_items
loading_pico $projItems

echo "[FINISHED] Project loaded. You may now disconnect the board."
