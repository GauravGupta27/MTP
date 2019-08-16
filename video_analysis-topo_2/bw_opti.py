import sys
sys.path.insert(0,'./utility_scripts/')
import misc_func

from cvxpy import *

def bw_opti(num_be_flows):
	# number of best effort flows
	n = num_be_flows

	# number of HD & SD flows
	n_hd = 2
	n_sd = 2

        # cvx variables
        x = Variable() * n_hd
        y = Variable() * n_sd
	z = Variable() * n

	lim_mat = misc_func.give_bw_limits()

	# Link bandwidth

        max_bw = misc_func.give_max_link_cap()

	# Weight array
	# applying a weight on each type of traffic
	wt = [0,0,0]

	if n != 0:
		wt = misc_func.get_flow_wt()
	else:
		wt = [0.50, 0.50, 0.0]

        constraints = [x + y + z <= max_bw,           		# total b/w available
                               x <= lim_mat[0][0] * n_hd,    	# upper limit of class 1
                               y <= lim_mat[1][0] * n_sd,    	# upper limit of class 2
                               z <= lim_mat[2][0] * n,		# upper limit of best effort flow
                               x >= lim_mat[0][1] * n_hd,    	# lower limit of class 1
                               y >= lim_mat[1][1] * n_sd,    	# lower limit of class 2
                               z >= lim_mat[2][1] * n]  	# lower limit of best effort flow

        # objective function
        obj     = Maximize(wt[0]*log(x) + wt[1]*log(y) + wt[2]*log(z))

        # creating the problem, which is a combination of objective function and constraints
        prob    = Problem(obj, constraints)

        # solving the problem and storing the maximized value
        max_val = prob.solve()

	ret_arr = [round(x.value), round(y.value), round(z.value), round(x.value + y.value + z.value)]

	return ret_arr
