import csv
import os
import numpy as np

import sys
sys.path.insert(0, '../utility_scripts/')
import misc_func

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def main():
	# all constants
	path_to_stat = '../stats/csv/'

	file_name_l = ['all_tcp_rtt_avg.csv','all_tcp_rtt_stdev.csv']

	plt_title = ['RTT (Average)', 'RTT (Standard Deviation)']

	metric_marker   = ['bs','ko','c^','r*']

	line_style = ['-', '--']

	exp_type = ['Base', 'H2DQ']

	plt_font_size_axis = misc_func.get_plt_font_size_axis()

	plt_font_size_legend = misc_func.get_plt_font_size_legend()

	plt_marker_size = misc_func.get_plt_marker_size()

	plt_font_size_tick = misc_func.get_plt_font_size_tick()

	plt_num = int(sys.argv[1])

	###############

	csv_file = csv.reader(open(path_to_stat + file_name_l[plt_num], 'r'))

	csv_data = []

	for row in csv_file:
		fl_row = map(float,row)
		csv_data.append(fl_row)

	csv_data_np = np.array(csv_data)

	# x axis ticks
	x_axis = misc_func.give_num_con_l('h2dq')

	# converted string to float
	csv_data_np = csv_data_np.astype('float')

	# all zero elements are turned to nan
	csv_data_np[csv_data_np == 0] = 'nan'

	fig, ax = plt.subplots()

	for i in xrange(8):
		plt.plot(x_axis, \
			csv_data_np[i], \
			metric_marker[i%4], \
			markersize = plt_marker_size, \
			linestyle = line_style[i/4], \
			lw = 2.5, \
			label = '(%s) Case %s' % (exp_type[i/4], (i)%4 + 1))

	plt.grid(True)
	plt.xlabel('Number of Connections', fontsize = plt_font_size_axis)
	plt.ylabel('Time (ms)', fontsize = plt_font_size_axis)
	plt.title(plt_title[plt_num])
	plt.xticks(fontsize = plt_font_size_tick)
        plt.yticks(fontsize = plt_font_size_tick)

	box = ax.get_position()

	# changing size of plot to accomodate legend
	ax.set_position([box.x0, \
                        box.y0 + box.height * 0.1, \
                        box.width, \
                        box.height * 0.9])

	# adjusting legend
	ax.legend(loc = 'upper center', bbox_to_anchor = (.5, 1.02), ncol=2, fontsize = plt_font_size_legend)

	# adjusting plot padding
	plt.subplots_adjust(left = 0.12, right = 0.97, top = 0.90, bottom = 0.10)

	# saving plot as PDF
	pic_to_pdf = plt.gcf()
	pic_to_pdf.set_size_inches(6,5)
	#plt.tight_layout()
	plt.savefig('%s.pdf' % (file_name_l[plt_num].split('.')[0]), dpi = 200)
 
if __name__ == '__main__':
	main()
