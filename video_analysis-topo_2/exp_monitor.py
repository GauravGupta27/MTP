from multiprocessing import Process
from argparse        import ArgumentParser
from time            import sleep, time
from subprocess      import *

import re

default_dir = '.'

def monitor_qlen(iface, interval_sec = 0.01, fname='%s/qlen.txt' % default_dir):
    pat_queued = re.compile(r'backlog\s[^\s]+\s([\d]+)p')
    cmd = "tc -s qdisc show dev %s" % (iface)
    ret = []
    open(fname, 'w').write('')
    while 1:
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.stdout.read()
        # Not quite right, but will do for now
        matches = pat_queued.findall(output)
        if matches and len(matches) > 1:
            ret.append(matches[1])
            t = "%f" % time()
            open(fname, 'a').write(t + ',' + matches[1] + '\n')
        sleep(interval_sec)
    return

def qmon():
    port_nm        = 's1-eth3'
    buff_file_name = '%s_%s_que.txt' % (args.exp, args.ncon)
    buff_scan_int  = 0.01

    monitor = Process(target=monitor_qlen, args=(port_nm, buff_scan_int, buff_file_name))
    monitor.start()

    print "Monitoring Queue Occupancy ... will save it to %s" % buff_file_name

if __name__ == '__main__':
    parser = ArgumentParser(description="CWND/Queue Monitor")
    parser.add_argument('--exp', '-e',
                        dest="exp",
                        action="store",
                        help="Name of the Experiment",
                        required=True)

    parser.add_argument('--ncon', '-n',
                        dest="ncon",
                        action="store",
                        help="Number of background TCP connections",
                        required=True)

    args = parser.parse_args()

    qmon()
