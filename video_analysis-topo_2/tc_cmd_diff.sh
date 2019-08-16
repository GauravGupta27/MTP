#!/bin/bash

#Size of the queue
qlen=$1
#Delay per link
sdelay=$2'ms'
#Link bandwidth
total_rate=$3'kbps'
#Video bandwidth
udp_hd_rate=$4'kbps'
udp_sd_rate=$5'kbps'
#Best effort bandwidth for tcp connections
tcp_rate=$6'kbps'
rec_port_1=$7
rec_port_2=$8

function add_qdisc {

    dev=$1

    echo 'Applying tc on '$dev
    
    # deleting default qdisc. This is mandatory
    tc qdisc del dev $dev root
    # echo qdisc removed

    # adding custom qdisc (Root node of HTB)
    tc qdisc add dev $dev root handle 1:0 htb default 1
    # echo qdisc added

    # creating classes for tcp and udp traffic
    ## 1:1 is child node of 1:0. 1:1 has b/w of total_rate
    ## 1:11 and 1:12 are child nodes of 1:1
    tc class add dev $dev parent 1:0 classid 1:1  htb rate $total_rate  ceil $total_rate
    tc class add dev $dev parent 1:1 classid 1:11 htb rate $udp_hd_rate ceil $udp_hd_rate
    tc class add dev $dev parent 1:1 classid 1:12 htb rate $udp_sd_rate ceil $udp_sd_rate
    tc class add dev $dev parent 1:1 classid 1:13 htb rate $tcp_rate    ceil $tcp_rate
    # echo classes created

    # creating link delays and queues
    # adding delay and buffer size to 1:11 and 1:12
    tc qdisc add dev $dev parent 1:11 handle 11: netem delay $sdelay limit $qlen
    tc qdisc add dev $dev parent 1:12 handle 12: netem delay $sdelay limit $qlen
    tc qdisc add dev $dev parent 1:13 handle 13: netem delay $sdelay limit $qlen
    # echo "delay and queue added"

    # matching the tcp/udp traffic to the appropriate class
    # 1x11 - UDP | 1x06 - TCP | 1x01 - ICMP
    tc filter add dev $dev parent 1:0 protocol ip u32 \
	match ip src 10.0.0.1/32 \
	flowid 1:11	# UDP HD
    tc filter add dev $dev parent 1:0 protocol ip u32 \
	match ip src 10.0.0.2/32 \
	flowid 1:12 	# UDP SD
    tc filter add dev $dev parent 1:0 protocol ip u32 \
	match ip src 10.0.0.3/32 \
	flowid 1:13 	# TCP
    
    # echo filters added

}

add_qdisc s1-eth1
add_qdisc s1-eth2
add_qdisc s1-eth3
add_qdisc s1-eth4
