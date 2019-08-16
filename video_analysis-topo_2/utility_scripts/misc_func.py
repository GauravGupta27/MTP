import csv

#-----[DATA]-----

def give_exp_no_l():
	exp_no_l = [1,2,3,4]

	return exp_no_l

def give_client_host_d():
	exp_dic = { \
	1:['h4', 'h5', 'h6'], \
	2:['h7', 'h8', 'h9'], \
	3:['h4', 'h8', 'h6', 'h9'], \
	4:['h7', 'h5', 'h6', 'h9']}

	return exp_dic

def give_vid_host_d():
	exp_dic = {
	1:['h1', 'h2', 'h4', 'h5'], \
	2:['h1', 'h2', 'h7', 'h8'], \
	3:['h1', 'h2', 'h4', 'h8'], \
	4:['h1', 'h2', 'h7', 'h5']}

	return exp_dic

def give_bw_limits():
        # Row 1 : HD
        # Row 2 : SD
        # Row 3 : best effort

        lim_mat = [ \
                [600,350], \
                [300,150], \
                [ 40,20]]

	return lim_mat

def give_vid_list():
	vid_l = [ \
		'~/Videos/hd_1_184sec.mp4', \
		'~/Videos/hd_2_179sec.mp4', \
		'~/Videos/sd_1_180sec.mp4', \
		'~/Videos/sd_2_187sec.mp4']

	return vid_l

def get_plt_font_size_axis():
	return 19

def get_plt_font_size_legend():
	return 19

def get_plt_marker_size():
	return 12

def get_plt_font_size_tick():
	return get_plt_font_size_axis() - 4

# Link bandwidth
def give_max_link_cap():
	# in kilobytes per second
        max_bw = 2048

	return max_bw

def get_flow_wt():
	wt_arr = [0.60, 0.25, 0.15]

	return wt_arr

def give_port_l():
	port_l = ['9004', '5004']

	return port_l

#-----[CONDITIONAL DATA]-----

def give_num_con_l(exp_type):
	num_con_l = [10,14,18,22,26,30,34,38,42,46,50]

	if exp_type == 'base':
		return num_con_l[0:6]
	elif exp_type == 'h2dq':
		return num_con_l

	return -1

def host_to_ip(hostname):
	return '10.0.0.%s' % (hostname[1])

def give_host_to_vid_type(node_id):
	if node_id == 'h4' or node_id == 'h7' or node_id == 'h1':
		return 'hd'
	elif node_id == 'h5' or node_id == 'h8' or node_id == 'h2':
		return 'sd'
	else:
		return -1

def give_vid_snd(node_id):
	if node_id == 'h4' or node_id == 'h7':
		return 'h1'
	elif node_id == 'h5' or node_id == 'h8':
		return 'h2'
	else:
		return -1

def give_tcp_rec_host(case_id):
	case_dic = {
		'1':['h6','h6'], \
		'2':['h9','h9'], \
		'3':['h6','h9'], \
		'4':['h6','h9']}

	return case_dic[case_id]

def flow_len(node_id):
        
        if node_id[1] == '4' or node_id[1] == '5':
                return 'l'
        else:
                return 's'

# Returns video quality of video file depending on file name convention
# hd or sd
def vid_def(file_name):

        return file_name.strip().split('/')[2][0:2]
        # Sample file name = ~/Video/hd_3_180sec.mp4
        # stripping white space -> splitting by '/'
        # -> taking 3rd string -> taking first 2 characters

# only receiver side dump files
def give_all_tdp_files(exp_type):

        exp_no_l = give_exp_no_l()
        num_con_l = give_num_con_l(exp_type)
        tdp_file_path = '../stats/%s/case%s/'

        exp_dic = give_client_host_d()

        file_l = []

        for i in exp_no_l:
                case_l = []
                for j in num_con_l:
                        for k in exp_dic[i]:
                                tdp_file_name = give_tdp_name(i,j,k)
                                full_name = tdp_file_path % (exp_type,i) + tdp_file_name
                                case_l.append(full_name)

                file_l.append(case_l)

        return file_l

# both client and receiver side dump files minus tcp traffic
def give_all_tdp_files_v2(exp_type):

        exp_no_l = give_exp_no_l()
        num_con_l = give_num_con_l(exp_type)
        tdp_file_path = '../stats/%s/case%s/'

        exp_dic = give_vid_host_d()

        file_l = []

        for i in exp_no_l:
                case_l = []
                for j in num_con_l:
                        for k in exp_dic[i]:
                                tdp_file_name = give_tdp_name(i,j,k)
                                full_name = tdp_file_path % (exp_type,i) + tdp_file_name
                                case_l.append(full_name)

                file_l.append(case_l)

        return file_l

def give_all_video_files(exp_type):

        exp_no_l = give_exp_no_l()
        num_con_l = give_num_con_l(exp_type)
        video_file_path = '../stats/%s/case%s/'

        exp_dic = give_client_host_d()

        file_l = []

        for i in exp_no_l:
                case_l = []
                for j in num_con_l:
                        for k in exp_dic[i][0:2]:
                                for l in xrange(2):
                                        vid_file_name = give_vid_name(i, j, flow_len(k), give_host_to_vid_type(k), l+1)
                                        full_name = video_file_path % (exp_type,i) + vid_file_name
                                        case_l.append(full_name)
                file_l.append(case_l)

        return file_l


#-----[FILE NAMES]-----

def give_vid_name(exp_no, num_con, flow_len, vid_def, vid_num):
	return '%s_%s_%s_%s_%s.mp4' % (exp_no, num_con, flow_len, vid_def, vid_num)

def give_tdp_name(exp_no, num_con, host_name):
	return '%s_%s_%s.pcap' % (exp_no, num_con, host_name)

def give_pcap_to_csv_name(pcap_file, host_type, index):
	return '%s_%s%s.csv' % (pcap_file, host_type, index)

def give_pcap_csv_name(pcap_file, vid_num):

        # path of pcap file
        pcap_file_path = '/'.join(pcap_file.split('/')[0:-1]) + '/'

        # name of pcap file
        pcap_file_name = pcap_file.split('/')[-1].split('.')[0]

	# host type [hd/sd]
	host_type = give_host_to_vid_type(pcap_file_name[-2:])

        # name of converted csv file
        pcap_csv_file = give_pcap_to_csv_name(pcap_file_name, host_type, vid_num + 1)
	
        # path appended to converted csv file
        full_path_csv_file = pcap_file_path + pcap_csv_file

        return full_path_csv_file

def give_pcap_csv_name_rec(exp_type):
	exp_no_l = give_exp_no_l()
        num_con_l = give_num_con_l(exp_type)
        csv_file_path = '../stats/%s/case%s/'

	file_l = []

	for i in exp_no_l:
		file_r = []
		for j in num_con_l:
			for k in give_vid_host_d()[i][-2:]:
				for l in xrange(2):
					csv_file_rec = '%s_%s_%s_%s%s.csv' % (i, j, k, give_host_to_vid_type(k), l+1)
					csv_file_snd = '%s_%s_%s_%s%s.csv' % (i, j, give_vid_snd(k), give_host_to_vid_type(k), l+1)
					file_r.append([csv_file_path % (exp_type,i) + csv_file_snd, csv_file_path % (exp_type,i) + csv_file_rec])
		file_l.append(file_r)

	return file_l
			
# Returns length of flow depending on destination
# Long (l) or short (s)

#-----[COMPUTATION]-----

# it is actually giving the nth column
def give_nth_row(some_list, n):
	return [row[n] for row in some_list]

def get_avg(some_list):
	return sum(some_list) / float(len(some_list))

def get_nth_line(f_name, n):
	fp = open(f_name, 'r')

	i = 0

	for row in fp:
		tmp_line = row

		if i == (n-1):
			fp.close()
			return tmp_line.strip()
		i += 1

def scn_mapping(i):
        """
        Mapping connection number to b/w requirements
        Must be even number
        """
        return (i-6)/4

def write_to_file(file_name, some_l):
	fp = open(file_name, 'a')
	fpc = csv.writer(fp)

	for i in some_l:

		fpc.writerow(i)

	fp.close()

def divide_list(some_list, n):
	new_list = [i/n for i in some_list]

	return new_list
