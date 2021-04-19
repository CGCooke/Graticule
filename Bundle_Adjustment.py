'''
Fundamentally, the bundle adjustment is performed by scipy.optimize.least_squares.

`scipy.optimize.least_squares(fun = bundle_adjustment_function, x0 = x0, jac_sparsity = jac_sparsity_matrix, args = bundle_adjustment_function_args)`

Fundamentally, we need to provide it with 4 things.

1. A function which computes the vector of residuals (bundle_adjustment_function).
2. An initial estimate of the independent variables (x0).
3. An array defining the sparsity structure of the jacobian matrix (jac_sparsity_matrix). 
4. Arguments passed to our function bundle_adjustment_function (bundle_adjustment_function_args).
'''

import numpy as np
from scipy.spatial.transform import Rotation as Rot

class Bundle_Adjustmment(object):
	"""The position and orientation of either a tag or a camera"""
	def __init__(self):

	def bundle_adjustment_sparsity(self):
		pass

	def optimisation_function(self):
		pass

	def project_points(self):
		pass
