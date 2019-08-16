from argparse   import ArgumentParser
import misc_func

def main():
	f = open(args.input_list, 'r')
	
	input_list = []

	# Extracting data from input file and appending it to an array
	for row in f:
		# Lines starting with '#' are comments
		if row[0] != '#':
			input_list.append(row.strip())

	# Script pause time
	pause_time  = 3

	# iperf duration
	iperf_dur     = '190'

	
	# number of background TCP connections

	num_con = 0

	if args.conn_num == '':
		num_con = int(input_list[0])
	else:
		num_con = int(args.conn_num)

	print '[INFO] : iperf sessions = %d' % num_con

	snd_l 		= []	# sender host name
	inp_vid_l 	= []	# input video name/path
	str_dur_l 	= []	# video stream duration
	rec_l 		= []	# receiver host name
	rec_port_l 	= []	# receiver host port
	rec_ip_l	= []	# receiver ip
	snd_ip_l	= []	# sender ip


	for i in xrange(4):
		snd_l.append(input_list[1 + i*4])
		inp_vid_l.append(input_list[2 + i*4])
		str_dur_l.append(input_list[3 + i*4])
		rec_l.append(input_list[4 + i*4])
		rec_ip_l.append('10.0.0.%s' % rec_l[i][1])
		snd_ip_l.append('10.0.0.%s' % snd_l[i][1])

	# receiver ports
	rec_port_1  = misc_func.give_port_l()[0]
	rec_port_2  = misc_func.give_port_l()[1]

	# Buffer monitoring duration will be maximum of the streaming duration of both the files
	max_str_dur = max(map(int, str_dur_l))
	
	# FILES TO BE CREATED (VIDEO + TCPDUMPS)
	
	out_vid_l = []

	for i in xrange(4):
		tmp_vid_name = misc_func.give_vid_name(args.exp_no, \
			num_con, \
			misc_func.flow_len(rec_l[i]), \
			misc_func.vid_def(inp_vid_l[i]), \
			(i%2) + 1)

		out_vid_l.append(tmp_vid_name)
	
	tdp_snd_l = []
	tdp_rec_l = []


	for i in xrange(2):
		tdp_snd_l.append(misc_func.give_tdp_name(args.exp_no, num_con, snd_l[i*2]))
		tdp_rec_l.append(misc_func.give_tdp_name(args.exp_no, num_con, rec_l[i*2]))

	tcp_hosts_rec = misc_func.give_tcp_rec_host(args.exp_no)
	tcp_hosts_rec_ip = [misc_func.host_to_ip(tcp_hosts_rec[0]),misc_func.host_to_ip(tcp_hosts_rec[1])]
	
	tcp_hosts_snd = 'h3'
	# file name of tcpdump iperf sender
	tdp_tcp_snd = misc_func.give_tdp_name(args.exp_no, num_con, tcp_hosts_snd)
	# file names of tcpdumps iperf receivers
	tdp_tcp_rec = [misc_func.give_tdp_name(args.exp_no, num_con, tcp_hosts_rec[0]), misc_func.give_tdp_name(args.exp_no, num_con, tcp_hosts_rec[1])]

                        # Initiating tcpdumps at VLC sender
	file_content = ['%s timeout %s sudo tcpdump -w %s &\n'                 % (snd_l[0], int(str_dur_l[0]) + pause_time, tdp_snd_l[0]), \
                        '%s timeout %s sudo tcpdump -w %s &\n'                 % (snd_l[2], int(str_dur_l[2]) + pause_time, tdp_snd_l[1]), \
			
			# Initiating tcpdumps for iperf senders
			'%s timeout %s sudo tcpdump -w %s &\n'                 % (tcp_hosts_snd, int(str_dur_l[0]) + pause_time, tdp_tcp_snd), \

                        # Initiating tcpdumps at VLC receiver
                        '%s timeout %s sudo tcpdump -w %s &\n'                 % (rec_l[0], int(str_dur_l[0]) + pause_time, tdp_rec_l[0]), \
                        '%s timeout %s sudo tcpdump -w %s &\n'                 % (rec_l[2], int(str_dur_l[2]) + pause_time, tdp_rec_l[1]), \
                        
			# Initiating tcpdumps for iperf receivers
			'%s timeout %s sudo tcpdump -w %s &\n'                 % (tcp_hosts_rec[0], int(str_dur_l[0]) + pause_time, tdp_tcp_rec[0]), \
                        '%s timeout %s sudo tcpdump -w %s &\n'                 % (tcp_hosts_rec[1], int(str_dur_l[2]) + pause_time, tdp_tcp_rec[1]), \

                        # Starting receiver side VLC
                        '%s python utility_scripts/vlc_rec.py %s %s %s &\n'    % (rec_l[0], out_vid_l[0], int(str_dur_l[0]) + pause_time, rec_port_1), \
                        '%s python utility_scripts/vlc_rec.py %s %s %s &\n'    % (rec_l[1], out_vid_l[1], int(str_dur_l[1]) + pause_time, rec_port_2), \
                        '%s python utility_scripts/vlc_rec.py %s %s %s &\n'    % (rec_l[2], out_vid_l[2], int(str_dur_l[2]) + pause_time, rec_port_1), \
                        '%s python utility_scripts/vlc_rec.py %s %s %s &\n'    % (rec_l[3], out_vid_l[3], int(str_dur_l[3]) + pause_time, rec_port_2), \

                        # Starting receiver side iperf
                        '%s ./utility_scripts/tcp_rec %s dummy\n'              % (tcp_hosts_rec[0], num_con/2), \
                        '%s ./utility_scripts/tcp_rec %s dummy\n'              % (tcp_hosts_rec[1], num_con/2), \

                        # Starting monitoring script
                        'h1 ping -c %s h1\n' % (pause_time), \
                        'sh nohup timeout %s sudo python exp_monitor.py -e %s -n %s > /dev/null 2>&1 &\n' % (max_str_dur, args.exp_no, num_con), \

                        # Starting sender side VLC and iperf session
                        '%s python utility_scripts/vlc_snd.py %s %s %s %s &\n' % (snd_l[0], inp_vid_l[0], rec_ip_l[0],  str_dur_l[0], rec_port_1), \
                        '%s python utility_scripts/vlc_snd.py %s %s %s %s &\n' % (snd_l[1], inp_vid_l[1], rec_ip_l[1],  str_dur_l[1], rec_port_2), \
                        '%s python utility_scripts/vlc_snd.py %s %s %s %s &\n' % (snd_l[2], inp_vid_l[2], rec_ip_l[2],  str_dur_l[2], rec_port_1), \
                        '%s python utility_scripts/vlc_snd.py %s %s %s %s &\n' % (snd_l[3], inp_vid_l[3], rec_ip_l[3],  str_dur_l[3], rec_port_2), \

                        # Starting sender side iperf
                        '%s ./utility_scripts/tcp_snd %s %s %s dummy\n'        % (tcp_hosts_snd, tcp_hosts_rec_ip[0],  num_con/2, iperf_dur), \
                        '%s ./utility_scripts/tcp_snd %s %s %s dummy\n'        % (tcp_hosts_snd, tcp_hosts_rec_ip[1],  num_con/2, iperf_dur)]

	if file_content[5] == file_content[6]:
		del(file_content[5])

	script_name = args.script_name

	nf = open(script_name, 'w')

	# Creating script file
	for i in file_content:
		nf.write(i)

	nf.close()

	print '[INFO] : Script file [%s] created' % script_name

if __name__ == '__main__':
	parser = ArgumentParser(description='Creates streaming script for the topology')

	parser.add_argument('--input-file', '-i',
			    dest="input_list",
			    action="store",
			    help="Name of the input file",
			    required=True)

	parser.add_argument('--script-name', '-s',
			    dest="script_name",
			    action="store",
			    help="Name of the generated script file",
                            default='str_scr'
                            )

        parser.add_argument('--exp', '-e',
                            dest="exp_no",
                            action="store",
                            help="Experiment number by which the buffer file will be saved",
                            required=True)

	parser.add_argument('--conn', '-c',
                            dest="conn_num",
                            action="store",
                            help="Use connection number (number of background iperf sessions) from argument instead of file",
                            default='',
                            required=False)

	args = parser.parse_args()

	main()
