#!/usr/bin/python
# -*- coding: utf-8 -*-


from mininet.topo import Topo
from mininet.node import CPULimitedHost # ??
from mininet.link import TCLink         # ??
from mininet.net  import Mininet
from mininet.node import OVSController
from mininet.cli  import CLI

from mininet.nodelib import LinuxBridge
from mininet.node import IVSSwitch
        
from subprocess   import call
from argparse     import ArgumentParser
from collections  import deque

from bw_opti      import bw_opti

import sys
sys.path.insert(0, './utility_scripts/')
import misc_func
import networkx as net
import random
import os
from itertools import izip
import numpy as np



# number of hosts
n_hosts = 0
        
# host list
hosts_l=[]

#switch list
sw_l=[]

# Number of switches
n_sw    = 0


def pairwise(iterable):
    a = iter(iterable)
    return izip(a, a)



class StarTopo(Topo):
    def __init__(self, cpu, bw_host, delay, maxq):
        """creating topology"""

        # Add default members to class.
        super(StarTopo, self ).__init__()

      
        
        
        # Create switches
        FielName="edge1.txt"
        Graphtype=net.Graph()   
        G = net.read_edgelist(FielName, create_using=Graphtype, nodetype=str)
        sw_l=G.nodes()
        print sw_l
        for s in sw_l:
            self.addSwitch(s,cls=LinuxBridge,stp=True)
            
      


        # number of hosts
        n_hosts =2*len(sw_l);


        # Create host nodes
        for i in xrange(n_hosts):
            self.addHost('h%d' % (i+1), cpu=cpu )
            hosts_l.append('h%d' % (i+1))

        print hosts_l



# Creating connections between the hosts and the switches        
        s_list=[] 
        for x, y in pairwise(hosts_l):
            sw=random.choice(sw_l)
            sw_l.remove(sw)
            print('host-1-%s--host-2-%s \t swich-%s' % (x,y,sw))
            #if(x=="h1"or y=="h1"):
            if x in hosts_l[:len (hosts_l)/2] or y in hosts_l[:len (hosts_l)/2]:
                s_list.append(sw)
            
            self.addLink(x, sw, bw=bw_host, max_queue_size=int(maxq) ) 
            self.addLink(y, sw, bw=bw_host, max_queue_size=int(maxq) )

        file_switch=open("tc_cmd_base_switch.txt","w")
        for s in s_list:
            ss=s+"\n";
            file_switch.write(ss);
        file_switch.close()


        # Creating connections between the switches
        file = open("switch.txt", "r") 
        for line in file:
            line = line.strip()
            if '\t' in line:
                s1,s2= line.split('\t')
                print 'swich con--%s\t%s' % (s1,s2)
                self.addLink(s1, s2, bw = bw_host, max_queue_size = int(maxq))
                #os.system('ovs-vsctl set bridge %s stp-enable=true' %s1)
                #os.system('ovs-vsctl set bridge %s stp-enable=true' %s2)
                #s2.cmd('ovs-vsctl set bridge s2 stp-enable=true')
        file.close()



# loop detection funtion detect the loop in switches connection and remove it
def loop_detction():
    #with open("rocketfuel.txt") as f:
    #    lines = list(f)

   # file = open("edge.txt", "w") 
   # for i in range(20):
   #     line=random.choice(lines)
   #     line = line.strip()
   #     if ' ' in line:
   #        s1,s2,ip1,h,ip2 = line.split(' ')
   #         ss=s1+'\t'+s2+'\n'
   #         file.write(ss)
   # file.close()


    
    FielName="switches_edge.txt"
    Graphtype=net.Graph()   
    G = net.read_edgelist(FielName, create_using=Graphtype, nodetype=str)
    G2 = net.Graph()


    graphs = net.connected_component_subgraphs(G, copy=False)
    for g in graphs:
        T = net.minimum_spanning_tree(g)
        G2.add_edges_from(T.edges())
        G2.add_nodes_from(T.nodes())

    #H = G2.to_directed()

    H = net.DiGraph();
    nodes = G2.nodes()
      
    sw_l=nodes
    # Number of switches
    n_sw    = len(nodes)
    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            if nodes[j] in G2[nodes[i]]:
                H.add_edge(nodes[i],nodes[j])


    file1 = open("final_switch.txt", "w") 
    for x in H.nodes():
        for y in H.adj[x]:

            #print("node" , x, "adj node ",y)
            switch_con=x+"\t"+y+"\n"
            #print '%s\t%s' % (s1,s2)
            file1.writelines(switch_con)
    file1.close()



def bbnet():
    topo = StarTopo(cpu=None,
                    bw_host=args.bw_host,
                    delay='%sms' % args.delay,
                    maxq=args.maxq)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoPinCpus=True, controller=OVSController)
    net.start()

    # total capacity of each link
    total_bw = str(misc_func.give_max_link_cap())

    # Creating bandwidth limitations

    if args.diff == False:
        print '[INFO] : Using standard bandwidth algorithm'
        print '[INFO] : Total capacity %s' % (total_bw)
        call(['sudo', 'bash', 'tc_cmd_base.sh', str(args.maxq), str(args.delay), str(total_bw)])
    else:
        
        print '[INFO] : Using modified bandwidth algorithm'
        print '[INFO] : Total capacity %s' % (total_bw)

        port_list = misc_func.give_port_l()

        # stores experiment scenario
        conn_num = ''

        # argument not supplied in runtime
        # fetching argument from file
        if args.conn_num == '':
            conn_num = int(misc_func.get_nth_line(args.input_file, 2))
            print '[INFO] : [create_topo.py] conn_num from file %d' % (conn_num)

        else:
            conn_num = int(args.conn_num)
            print '[INFO] : [create_topo.py] conn_num from args %d' % (conn_num)

        # determing experiment number
        exp_num = misc_func.scn_mapping(conn_num)

        print '[INFO] : Experiment scenario number [%s]' % exp_num

        # running optimization module
        exp_bw = bw_opti(conn_num)

        if conn_num == 0:
                # just putting a dummy value as there is no tcp streams
                exp_bw[2] = 100

        print '[INFO] : B/w used %s %s %s' % (exp_bw[0], exp_bw[1], exp_bw[2])
        
        call(['sudo', 'bash', 'tc_cmd_diff.sh', 
                  str(args.maxq), str(args.delay), str(total_bw), 
                  str(exp_bw[0]), str(exp_bw[1]), str(exp_bw[2]), 
                  str(port_list[0]), str(port_list[1])])

    CLI(net)

if __name__ == '__main__':
    # Parse arguments

    parser = ArgumentParser(description="BufferBloat tests")

    parser.add_argument('--bw-host', '-B',
                dest="bw_host",
                type=float,
                action="store",
                help="Bandwidth of host links",
                required=True)

    parser.add_argument('--delay',
                dest="delay",
                type=float,
                help="Delay in milliseconds of host links",
                default=10)
    
    parser.add_argument('--maxq',
                dest="maxq",
                action="store",
                help="Max buffer size of network interface in packets",
                default=500)

    parser.add_argument('--diff',
                    action="store_true",
                    help="Flag argument to mention whether to use different treatment for different kinds of traffic",
                    required=False)

    parser.add_argument('--input_file',
                    action="store",
                    dest="input_file",
                    help="Put name of input file here",
                    required=True)

    parser.add_argument('--conn', '-c',
                    dest="conn_num",
                    action="store",
                    help="Use connection number (number of background iperf sessions) from argument instead of file",
                    default='',
                    required=False)
    # Expt parameters
    args = parser.parse_args()
    loop_detction()
    bbnet()
