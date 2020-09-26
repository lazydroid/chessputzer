#!/usr/bin/env python
# encoding: utf-8
#
# Assuming you have a book you want to check for the chess diagrams. Here are 3 steps:
#	1. convert the book into pages, every page is a .png file
#	2. use THIS script to extract the diagrams from the pages
#	3. use chessputzzer to recognize the diagrams
#	4. profit!!! =)
#
# This script assumes 

import os, sys, cv2
import numpy as np
import json

import datetime
from itertools import takewhile

def mean_coords( coords ) :
	x = [c[0] for c in coords]
	y = [c[1] for c in coords]
	return ((min(x)+max(x))/2, (min(y)+max(y))/2)

def save_board( page_num, num, board ) :
	#now = datetime.datetime.now()
	#suffix = '%Y-%m-%d_%H%M'
	#folder = 'boards_%s' % suffix
	#os.mkdir( 'boards' )
	name = os.path.join( 'boards', 'page_%03d_board_%d.png' % (page_num, num))
	print 'saving board', name
	cv2.imwrite( name, board )

if __name__ == '__main__' :

	r, d, files = os.walk('pages').next()
	for f in files :
		#f = 'dee3ed3205b763ac0ad29cf218b93810-120.png'
		print f
		name = os.path.join( r, f )

		page_num = int(f.split('-')[1].split('.')[0])

		img = cv2.imread( name )
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		#cv2.imshow( 'contours', gray )
		#cv2.waitKey(0)
	
		ret, thresh = cv2.threshold( gray, 127, 255, 0)

		kernel = np.ones((10,1), np.uint8)
		dilated = cv2.dilate( thresh, kernel, iterations=7)

		contours, hierarchy = cv2.findContours( dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		#print json.dumps([c.tolist() for c in contours], indent=4)
		#print hierarchy

		#cv2.drawContours(img, contours, -1, (0,255,0), 3)

		means = []
		for c in contours[1:] :
			coords = [seg[0].tolist() for seg in c]
			#print mean_coords(coords)
			means.append( mean_coords(coords) )
			#print mean_coords(coords)

		means.sort( key = lambda x : x[1])	# sort by 'x'

		means_sorted = []
		while len(means) :
			slice = list(takewhile(lambda x: abs(x[1] - means[0][1]) < 10, means))
			means_sorted.extend( sorted(slice) )
			means = means[len(slice):]

		means = means_sorted
		
		for m in means : print m

		for num,(a,b) in enumerate(zip(means[::2], means[1::2])) :
			size = abs(a[0]-b[0])
			left = min(a[0], b[0])
			top = a[1]-size/2
			#cv2.rectangle( img, (left, top), (left+size, top+size), (255,0,0), 1)

			b = img[top:top+size, left:left+size]

			save_board( page_num, num, b )

			#cv2.imshow( 'contours', b )
			#cv2.waitKey(0)

		#cv2.imshow( 'contours', img )
		#cv2.waitKey(0)

		#break
