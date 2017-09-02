#python 2.7
#github: rocketOC
#reddit: https://www.reddit.com/user/derivative_art/
#imgur: derart
from PIL import Image
from math import floor
import sys
import random
import time
import sys
import datetime
import matplotlib.pyplot as plt
import numpy as np

sys.setrecursionlimit(10000000)

later = set()
im = None
searhed = None
pixels = None
orig = None
spacer = '-'*40
bg_val = None


class Network:
	"""class for a network/collection/cluster of pixels"""
	def __init__(self,networkid,value):
		self.networkid = networkid
		self.value = value #original value of pixells in the network
		self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255),1)
		self.pixels = set()

	def centroid(self):
		if len(self.pixels)>0:
			xcent = sum([p[0] for p in self.pixels])/len(self.pixels)
			ycent = sum([p[1] for p in self.pixels])/len(self.pixels)
			return (xcent,ycent)
		else:
			return None

	def size(self):
		return len(self.pixels)


def bw_filter(pixels,im0,im1):
	"""black and white filter"""
	for i in range(im0):
		for j in range(im1):
			avg = int(floor((pixels[i,j][0] + pixels[i,j][1] + pixels[i,j][2])/3.0))
			pixels[i,j] = (avg,avg,avg,1)

def thresh_filter(pixels,im0,im1,lev,less,more):
	"""Threshold Filter."""
	for i in range(im0):
		for j in range(im1):
			level = less
			if pixels[i,j][0] > lev:
				level = more
			pixels[i,j] = (level,level,level,1)

def iso_filter(pixels,im0,im1):
	"""Isolation filter. Flip pixels that are alone when
	checking non-corner adjacent pixels. Will NOT flip edge pixels."""
	for i in range(1,im0-1):
		for j in range(1,im1-1):
			if ((pixels[i,j][0] != pixels[i+1,j][0]) 
				  and (pixels[i,j][0] != pixels[i-1,j][0])
				  and (pixels[i,j][0] != pixels[i,j+1][0])
				  and (pixels[i,j][0] != pixels[i,j-1][0])):
				if pixels[i,j][0] == 255:
					pixels[i,j] = (0,0,0,1)
				else:
					pixels[i,j] = (255,255,255,1)


def paint_red_scale(networks):
	"""color the image in redscale"""
	sizes = [n.size() for n in networks]
	bins = np.linspace(0,max(sizes),40)
	cols = np.linspace(0,255,40)
	for n in nets:
		ncol = -1
		for i in range(1,len(bins)):
			if n.size() > bins[i-1] and n.size() <= bins[i]:
				ncol = cols[i]
		if ncol <128:
			colornet(n,2*int(ncol),0,0,0)
		else:
			colornet(n,255,2*int(ncol)-255,2*int(ncol)-255,0)

def paint_centroid(networks):
	"""color by cluster/network's centroid distance from center."""
	global im
	maxd = np.sqrt(np.power(im.size[0]/2.00,2) +  np.power(im.size[1]/2.00,2) )
	bins = np.linspace(0,maxd,40)
	cols = np.linspace(0,255,40)
	for n in nets:
		cent = n.centroid()
		dis = np.sqrt( np.power(cent[0] - im.size[0]/2.00,2)
				+  np.power(cent[1] - im.size[1]/2.00,2) )
		ncol = -1
		for i in range(1,len(bins)):
			if dis >= bins[i-1] and dis < bins[i]:
				ncol = cols[i]
		if ncol == -1:
			ncol = 255
		if ncol <128:
			colornet(n,2*int(ncol),0,0,0)
		else:
			colornet(n,255,2*int(ncol)-255,2*int(ncol)-255,0)

def get_next(i,j,maxx,maxy):
	"""return the ajacent ixels that are the same color and not yest searched."""
	global pixels
	next = []
	val = pixels[i,j][0]
	if i-1 >= 0:
		if searched[i-1,j] ==0 and pixels[i-1,j][0] == val:
			next.append((i-1,j))
	if j-1 >= 0:
		if searched[i,j-1] ==0 and pixels[i,j-1][0] == val:
			next.append((i,j-1))
	if i-1 >= 0 and j-1 >= 0:
		if searched[i-1,j-1] ==0 and pixels[i-1,j-1][0] == val:
			next.append((i-1,j-1))
	if i-1 >= 0 and j+1 < maxy:
		if searched[i-1,j+1] ==0 and pixels[i-1,j+1][0] == val:
			next.append((i-1,j+1))
	if j+1 < maxy:
		if searched[i,j+1] ==0 and pixels[i,j+1][0] == val:
			next.append((i,j+1))
	if i+1 < maxx:
		if searched[i+1,j] ==0 and pixels[i+1,j][0] == val:
			next.append((i+1,j))
	if i+1 < maxx and j+1 < maxy:
		if searched[i+1,j+1] ==0 and pixels[i+1,j+1][0] == val:
			next.append((i+1,j+1))
	if i+1 < maxx and j-1 >= 0:
		if searched[i+1,j-1] ==0 and pixels[i+1,j-1][0] == val:
			next.append((i+1,j-1))
	return next


def explorebg(i,j,maxx,maxy,net,depth):
	"""build a network by exploring the backgroud."""
	global later, pixels,im,searched
	if depth < 10000: #encountered my recursion limit on bigger images
		next = get_next(i,j,maxx,maxy)
		searched[i,j] = 1
		pixels[i,j] = (pixels[i,j][0],0,255,0)
		net.pixels.add((i,j))
		for n in next:
			net.pixels.add(n)
			pixels[n[0],n[1]] = (pixels[n[0],n[1]][0],255,255,0)
			searched[n[0],n[1]] = 1
		for n in next:
			explorebg(n[0],n[1],maxx,maxy,net,depth+1)
	else:
		pixels[i,j] = (pixels[i,j][0],0,255,0)
		later.add((i,j))

def superbg(i,j,maxx,maxy,net):
	"""needed to get around a recursion depth issue on large images."""
	global later
	explorebg(i,j,maxx,maxy,net,0)
	while len(later) > 0:
		todo = later.pop()
		explorebg(todo[0],todo[1],maxx,maxy,net,0)

def colornet(net,r,g,b,a):
	"""color all the pixels in a given network with the same color"""
	global pixels
	for p in net.pixels:
		pixels[p[0],p[1]] = (r,g,b,a)

def stripalpha(img):
	"""strip the alpha channel from the image"""
	pixelsa = img.load()
	for i in range(img.size[0]):
		for j in range(img.size[1]):
			pixelsa[i,j] = (pixelsa[i,j][0],pixelsa[i,j][1],pixelsa[i,j][2])

def paint_random(nets,colors=None):
	"""paint the networks randomly"""
	if colors is None:
		for n in nets:
			r = random.randint(0,255)
			g = random.randint(0,255)
			b = random.randint(0,255)
			colornet(n,r,g,b,0)
	else:
		for n in nets:
			col= colors[random.randint(0,len(colors)-1)]
			colornet(n,col[0],col[1],col[2],1)

def multi_color_rand(nets,num,filename,ext):
	"""genrate and save multiple random colorings of the image"""
	global im
	for k in range(num):
		name = filename + '_' + str(k)+ ext
		paint_random(nets)
		imt = im.copy()
		stripalpha(imt)
		imt.save(name)

def count_blacks_in_image():
	"""count the number of black pixels in image.
	Useful to determine if any pixel was included in more than one network..."""
	blacks = 0
	for i in range(im.size[0]):
		for j in range(im.size[1]):
			if pixels[i,j][0] == 0:
				blacks += 1
	return blacks

def bin_value(value,bins):
	""" return the center of the bin that value fits into
	using the NumPy histogram convention of [x,y)
	for all bins but the last which uses [x,y].
	If the value fits in no bin, return None"""
	bin = None
	if len(bins) >1:
		for i in range(len(bins)-1):
			if i + 2 < len(bins):
				if value >= bins[i] and value < bins[i+1]:
					bin = (bins[i] + bins[i+1])*.5
				else:
					pass
			else:
				if value >= bins[i] and value <= bins[i+1]:
					bin = (bins[i] + bins[i+1])*.5
				else:
					pass
	return bin


def hist_and_color(nets,limit):
	""""create a histogram of network sizes and the correspondinglycolored image."""
	global im
	cm = plt.cm.get_cmap('rainbow')
	sizes = [n.size() for n in nets if n.size() < limit]
	n, bins, patches =plt.hist(sizes,10, color='pink')
	bin_centers = 0.5 * (bins[:-1] + bins[1:])
	# scale values to interval [0,1]
	col = bin_centers - min(bin_centers)
	max_col = max(col)
	col /= max_col
	for c, p in zip(col, patches):
		plt.setp(p, 'facecolor', cm(c))

	plt.xlabel('pixels in cluster')
	plt.ylabel('number of clusters')
	plt.title(orig + ' with cluster size < ' + str(limit))

	for n in nets:
		if n.size() < limit:
			#get net's bin's centerpoint and put on 0_>1 scale
			loc = (bin_value(n.size(),bins) - min(bin_centers))/ (max_col*1.0)
			col = cm(loc)
			colornet(n,int(floor(col[0]*255)),int(floor(col[1]*255)),int(floor(col[2]*255)),0)
		else:
			#the nets with a size bigger than the limit will be black
			colornet(n,0,0,0,0)

	im.show()
	plt.show()


def loadnew(filename=None,bg_value=None):
	"""load a new image for processing"""
	global im, pixels, orig, searched, bg_val
	later.clear()
	if filename is None:
		orig = raw_input('input file name (default biophilia2.png): ')
		if len(orig) == 0:
			orig = 'biophilia2.png'
			bg_value = 0
	else:
		orig = filename
	if bg_value is None:
		response = raw_input('is the background black (b) or white (w): ')
		if response == "black" or response == "b":
			bg_val = 0
		else:
			bg_val = 255
	else:
		bg_val = bg_value
	im = Image.open(orig)
	pixels = im.load()
	searched = np.zeros((im.size[0],im.size[1]))

def filterchain(thresh_split):
	"""apply an initial filter chain to the image"""
	global im, pixels
	thresh_filter(pixels,im.size[0],im.size[1],thresh_split,0,255)
	bw_filter(pixels,im.size[0],im.size[1])
	iso_filter(pixels,im.size[0],im.size[1])

def save_current():
	"""save the current image"""
	global im
	filename = raw_input('input file name for saving or q for cancel: ')
	if filename != "q" and len(filename) >0:
		im2 = im.copy()
		stripalpha(im2)
		im2.save(filename)
	else:
		pass

def show_current():
	"""show the current image"""
	global im
	im.show()

def multi_rand(nets):
	"""get user to input variables for several random colorings"""
	filename = raw_input('input file name for saving: ')
	number_of = int(raw_input('input number of random colorings: '))
	multi_color_rand(nets=nets,num=number_of,filename=filename)

def network_search():
	global bg_val
	"""returns the networks in the image given the background value"""
	global pixels, searched
	nets = []
	startt = datetime.datetime.now()
	for i in range(im.size[0]):
		for j in range(im.size[1]):
			if searched[i,j] == 0 and pixels[i,j][0] == bg_val:
				idn = i*j
				newnet = Network(idn,bg_val)
				superbg(i,j,im.size[0],im.size[1],newnet)
				nets.append(newnet)
	endt = datetime.datetime.now()
	print 'network search took (seconds):', (endt-startt).seconds
	return nets

if __name__ == '__main__':
	print spacer
	print "**I need a job as of 8/31/17. Please PM me if interested.**"
	loadnew(filename=None,bg_value=None)
	filterchain(thresh_split=180)
	show_current() #post filtered image
	print 'discovering networks...'
	nets = network_search()
	show_current() #discovered networks will be recolored
	print 'total clusters:',  len(nets)
	print 'clusters > 10 pixels: ', len([n.size() for n in nets if n.size() > 10])
	#multi_color_rand(nets=nets,num=2,filename='biotest',ext='.png')
	colors = ((142,1,82),(197,27,125),(222,119,174),(241,182,218),(253,224,239)
		,(230,245,208),(184,225,134),(127,188,65),(77,146,33),(39,100,25))
	paint_random(nets,colors=colors)
	show_current()
	paint_random(nets)
	show_current()
	paint_red_scale(nets) #if one net dominates, the image will essentially be black and white
	show_current()
	paint_centroid(nets)
	show_current()
	hist_and_color(nets,800)
	save_current()




