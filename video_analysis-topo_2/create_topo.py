#!/usr/bin/python

from mininet.topo import Topo
from mininet.node import CPULimitedHost # ??
from mininet.link import TCLink         # ??
from mininet.net  import Mininet
from mininet.node import OVSController
from mininet.cli  import CLI

from subprocess   import call
from argparse     import ArgumentParser
from collections  import deque

from bw_opti      import bw_opti

import sys
sys.path.insert(0, './utility_scripts/')
import misc_func

class StarTopo(Topo):
    def __init__(self, cpu, bw_host, delay, maxq):
	"""creating topology"""

        # Add default members to class.
        super(StarTopo, self ).__init__()

        # number of hosts
        n_hosts = 9
        
	# Number of switches
        n_sw    = 6

        # Create host nodes
        for i in xrange(n_hosts):
            self.addHost('h%d' % (i+1), cpu=cpu )

        # Create switches
	for i in xrange(n_sw):
	    self.addSwitch('s%d' % (i+1), fail_mode='open')

        # Creating connections between the hosts and the switches
        self.addLink('h1', 's1', bw=bw_host, max_queue_size=int(maxq) ) # HD sender
        self.addLink('h2', 's1', bw=bw_host, max_queue_size=int(maxq) ) # SD sender
        self.addLink('h3', 's1', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h4', 's6', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h5', 's6', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h6', 's6', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h7', 's3', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h8', 's3', bw=bw_host, max_queue_size=int(maxq) )
        self.addLink('h9', 's3', bw=bw_host, max_queue_size=int(maxq) )

        # Creating connections between the switches
	for i in xrange(n_sw - 1):
            self.addLink('s%d' % (i+1), 's%d' % (i+2), bw = bw_host, max_queue_size = int(maxq))

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
        #print"dafsfsf"
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

    #print '[INFO] : Experiment scenario number [%s]' % exp_num

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
    bbnet()
