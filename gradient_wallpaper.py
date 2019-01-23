#!/usr/bin/env python

import sys
import matplotlib.pyplot as pp
import numpy as np

# function to give a smoothly changing image
def get_smooth_colour(height, length, r, g, b):

	# check 'r', 'g' and 'b'
	# these are the weights which will be used to get the final colour image
	if r < 0 or r > 1:
		raise ValueError('Invalid value for \'r\' argument.')
	if g < 0 or g > 1:
		raise ValueError('Invalid value for \'g\' argument.')
	if b < 0 or b > 1:
		raise ValueError('Invalid value for \'b\' argument.')

	'''
		The size of the image is given as (length, height)
		but a matrix is represented as (height, length)
		because 'height' is actually the number of rows and
		'length' is the number of columns.
	'''
	intensity_map = np.zeros([height, length])

	# initialising values for the loop
	row_start = 0 # the colour of the first pixel in a row
	row_step = 1.0 / (height - 1) # the amount by which 'row_start' will change on advancing one row
	print 'generating a mask'

	# filling the matrix with smoothly varying values
	for x in range(height):

		# initialising values for nested loop
		shade = row_start # the colour of [x, y] pixel
		column_step = (1.0 - row_start) / (length - 1) # the amount by which 'shade' will change on advancing one column
		print 'generating row %d of %d\r' % (x + 1, height),
		sys.stdout.flush()

		# actually writing values to the matrix happens here
		for y in range(length):

			# set pixel value and set up next loop iteration
			intensity_map[x, y] = 1 - shade
			shade += column_step
		row_start += row_step

	print '\nDone!'
	# this is the actual image, because matplotlib requires RGB
	img = np.zeros([height, length, 3])

	# depending on last three arguments, choose how the RGB channels are filled
	img[:, :, 0] = r * intensity_map
	img[:, :, 1] = g * intensity_map
	img[:, :, 2] = b * intensity_map

	'''
		Limitations of floating point representation cause errors
		in the above calculations. Some values may be slightly less
		than 0, and others, greater than 1. (I have seen values
		which were 1e-16 outside the bounds.) Hence, this is
		required.
	'''
	img = np.clip(img, 0, 1)
	return img

# main
if __name__ == '__main__':

	# set image dimensions
	try:
		height = abs(int(sys.argv[1]))
		length = abs(int(sys.argv[2]))
		r = abs(float(sys.argv[3]))
		g = abs(float(sys.argv[4]))
		b = abs(float(sys.argv[5]))
	except IndexError:
		print 'usage:'
		print '\t./smooth_gradient.py <height> <length> <red> <green> <blue>'
		raise SystemExit

	mask = get_smooth_colour(height, length, r, g, b)
	pp.imsave('desktop_background.png', mask)
