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

	file_name = 'all_vid_psnr.csv'

	plt_title = 'PSNR Value (Case %s)'

	metric_marker   = ['bs','ko','c^','r*']

	line_style = ['-', '--']

	exp_type = ['Base', 'H2DQ']

	plt_font_size_axis = misc_func.get_plt_font_size_axis()

	plt_font_size_legend = misc_func.get_plt_font_size_legend()

	plt_marker_size = misc_func.get_plt_marker_size()

	plt_font_size_tick = misc_func.get_plt_font_size_tick()

	plt_num = int(sys.argv[1])

	###############

	csv_file = csv.reader(open(path_to_stat + file_name, 'r'))

	csv_data = []

	for row in csv_file:
		fl_row = map(float,row)

		new_fl_row = []

		for i in xrange(len(fl_row)/2):
			avg_del = (fl_row[2*i] + fl_row[2*i + 1])/2
			new_fl_row.append(avg_del)

		csv_data.append(new_fl_row)

	csv_data_np = np.array(csv_data)

	# x axis ticks
	x_axis = misc_func.give_num_con_l('h2dq')

	# converted string to float
	csv_data_np = csv_data_np.astype('float')

	# all zero elements are turned to nan
	csv_data_np[csv_data_np == 0] = 'nan'

	fig, ax = plt.subplots()


	for i in xrange(2):
		#print csv_data_np[plt_num + 4*i], len(csv_data_np[plt_num + 4*i])

		delay_hd = csv_data_np[plt_num + 4*i][0::2] # at even position 0 2 4
		delay_sd = csv_data_np[plt_num + 4*i][1::2] # at odd position 1 3 5

		plt.plot(x_axis, \
			delay_hd, \
			metric_marker[2*i], \
			markersize = plt_marker_size, \
			linestyle = line_style[i], \
			lw = 2.5, \
			label = '(%s) HD' % (exp_type[i]))

		plt.plot(x_axis, \
			delay_sd, \
			metric_marker[2*i+1], \
			markersize = plt_marker_size, \
			linestyle = line_style[i], \
			lw = 2.5, \
			label = '(%s) SD' % (exp_type[i]))
		

	plt.grid(True)
	plt.xlabel('Number of Connections', fontsize = plt_font_size_axis)
	plt.ylabel('PSNR', fontsize = plt_font_size_axis)
	plt.title(plt_title % (plt_num+1))
	plt.xticks(fontsize = plt_font_size_tick)
        plt.yticks(fontsize = plt_font_size_tick)

	box = ax.get_position()

	# changing size of plot to accomodate legend
	ax.set_position([box.x0, \
                        box.y0 + box.height * 0.1, \
                        box.width, \
                        box.height * 0.9])

	# adjusting legend
	ax.legend(loc = 'upper center', \
		bbox_to_anchor = (0.5, -0.15), \
		ncol=2, \
		fontsize = plt_font_size_legend)

	# adjusting plot padding
	plt.subplots_adjust( \
			left = 0.12, \
			right = 0.97, \
			top = 0.95, \
			bottom = 0.30)

	# saving plot as PDF
	pic_to_pdf = plt.gcf()
	pic_to_pdf.set_size_inches(6,5)
	#plt.tight_layout()

	pdf_file_name = '%s_%s.pdf' % (file_name.split('.')[0], plt_num + 1)

	plt.savefig(pdf_file_name, dpi = 200)
 
if __name__ == '__main__':
	main()
