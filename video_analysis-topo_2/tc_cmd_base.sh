#!/bin/bash

#Size of the queue
qlen=$1
#Delay per link
sdelay=$2'ms'
#Total b/w of link
rate=$3'kbps'
 
function add_qdisc {

    dev=$1

    echo 'Applying tc on '$dev    

    tc qdisc del dev $dev root
    # echo qdisc removed
 
    # added root qdisc
    tc qdisc add dev $dev root handle 1:0 htb default 1
    # echo qdisc added
 
    # added class
    tc class add dev $dev parent 1:0 classid 1:1 htb rate $rate ceil $rate
    # echo classes created
 
    # added delay and buffer size
    tc qdisc add dev $dev parent 1:1 handle 10: netem delay $sdelay limit $qlen
    # echo delay added
}
 
# applying the above function to all interfaces

input="tc_cmd_base_switch.txt"
s1=""
s2=""
s3=""
s4=""
while IFS= read -r line
do
  #echo "$line"
	s1="$line-eth3"
	#s2="$line-eth2"
	#s3="$line-eth3"
	add_qdisc $s1
	#add_qdisc $s2
 	#add_qdisc $s3
done < "$input"  
# add_qdisc s1-eth1
# add_qdisc s1-eth2
# add_qdisc s1-eth3
#add_qdisc s1-eth4