#!/bin/bash

if [ "$#" -lt 1 ]; then
	echo "usage : sudo ./run experiment_number 0/1 [number of iperf sessions] (Standard or modified algorithm)"
	exit 1
fi

echo "[INFO] : Start video analytics experiment"

sudo sysctl -w net.ipv4.tcp_congestion_control=reno
sudo sysctl -w net.ipv4.tcp_min_tso_segs=1

input_file_name="sample_files/input_file"
exp_num=$1

# Creating streaming script

if [ "$#" -eq 3 ]; then
	# if number of arguments is 3,
	# then use connection number from argument
	# otherwise use connection number from file
	python utility_scripts/create_miniscr.py -i $input_file_name -e $exp_num -c $3
else
	python utility_scripts/create_miniscr.py -i $input_file_name -e $exp_num
fi

# Creating topology

if [ $2 -eq 1 ]; then
	# differentiated services flag is enabled
	if [ "$#" -lt 3 ]; then
		# number of arguments < 3
		# use connection number from file
		sudo python create_topo_new.py --bw-host 1000 --delay 1 --maxq 100 --input_file $input_file_name --diff
	elif [ "$#" -eq 3 ]; then
		# number of arguments == 3
		# use connection number from argument list
		sudo python create_topo_new.py --bw-host 1000 --delay 1 --maxq 100 --input_file $input_file_name --diff -c $3
	else
		echo "ERROR! [1]"
	fi
elif [ $2 -eq 0 ]; then
	# differentiated services flag is disabled
	if [ "$#" -lt 3 ]; then
		# number of args < 3
		# use connection number from file
		sudo python create_topo_new.py --bw-host 1000 --delay 1 --maxq 100 --input_file $input_file_name
	elif [ "$#" -eq 3 ]; then
		# number of args == 3
		# use connection number from argument list
		sudo python create_topo_new.py --bw-host 1000 --delay 1 --maxq 100 --input_file $input_file_name -c $3
	else
		echo "ECHO [3]"
	fi	
else
	echo $2
	echo "ERROR! [2]"
	exit 1
fi

# Cleaning topology
echo "[INFO] : cleaning up..."
sudo mn -c > /dev/null 2>&1
