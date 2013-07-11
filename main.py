#!/usr/bin/python

import pygame
import pygame.locals as pl
import cmath, math
import numpy as np
import time
import pdb

#~ ColorMap=
ColourPalette = [(241, 233, 191), (248, 201, 95), (255, 170, 0), (204, 108, 0), (153, 87, 0), (106, 52, 3), (66, 30, 15), (25, 7, 26), (25, 7, 26), (9, 1, 47), (4, 4, 73), (0, 7, 100), (12, 44, 138), (24, 82, 177), (57, 125, 209), (134, 181, 229), (211, 236, 248)]


class imageSection:
	def __init__(self, surface, (x,y)):
		self.anchor=(x,y)
		self.rect=pygame.Rect((x,y), (0,0))
		self.surface=surface
		self.color=pygame.Color(255,255,0)
		
	def resize(self, (x,y)):
		self.rect.width=x-self.anchor[0]
		#~ self.rect.height=y-self.anchor[1]
		self.rect.height=int(float(self.rect.width)*self.surface.get_size()[1]/self.surface.get_size()[0])
		if (y < self.anchor[1] and x > self.anchor[0]) or (y > self.anchor[1] and x < self.anchor[0]):
			self.rect.height*=-1
	def draw(self):
		pygame.draw.rect(self.surface, self.color, self.rect, 1)

def nonlineq(number, c):
	return number*number+c

def imagcolor(number):
	angle=math.degrees(cmath.phase(number))
	intensity=255.
	if angle<0:
		angle+=360
	if 0<=angle<60:
		(R,G,B)=(intensity, intensity/60*angle, 0)
	elif 60<=angle<120:
		(R,G,B)=(intensity-intensity*(angle-60)/60, intensity, 0)
	elif 120<=angle<180:
		(R,G,B)=(0, intensity, intensity*(angle-120)/60)
	elif 180<=angle<240:
		(R,G,B)=(0, intensity-intensity*(angle-180)/60, intensity)
	elif 240<=angle<300:
		(R,G,B)=((angle-240)/60*intensity, 0, intensity)
	else:
		(R,G,B)=(intensity, 0, intensity-(angle-300)/60*intensity)	
	#~ pdb.set_trace()
	try:
		return pygame.Color(int(R),int(G),int(B))
	except ValueError:
		return pygame.Color(255,255,255)

def draw_imag(surface, complmat, (xmax, ymax)):
	pa=pygame.PixelArray(surface)	
	for x in xrange(xmax):
		for y in xrange(ymax):
			pa[x][y]=imagcolor(complmat[x,y])
	del pa
	
def draw_iter(surface, limitmat, maxlimit, (xmax, ymax)):
	pa=pygame.PixelArray(surface)
	for x in xrange(xmax):
		for y in xrange(ymax):
			#~ try:
				#~ pa[x][y]=pygame.Color(int(float(limitmat[x,y])/maxlimit*255),0, int(float(limitmat[x,y])/maxlimit*255))
			#~ except ValueError:
				#~ pdb.set_trace()
			pa[x][y]=pygame.Color(*ColourPalette[limitmat[x,y]%17])
	del pa
	
def calc_converge(surface, limitmat, complmat, cvalmat, maxiter, maxdev):
	startvalmat=np.array(complmat)
	limitmat.fill(0)
	complmat.fill(0)
	for i in xrange(maxiter):
		complmat=complmat*complmat+cvalmat
		limitmat+=abs(complmat-startvalmat)<maxdev

def calc_clipping(surface, complmat, limitmat, clipping):
	cvalmat=np.array([[complex(clipping[0].real+j*(clipping[1].real-clipping[0].real)/size[0], clipping[0].imag+i*(clipping[1].imag-clipping[0].imag)/size[1]) for i in xrange(size[1])] for j in xrange(size[0])])
	calc_converge(surface, limitmat, complmat, cvalmat, 500, 2)
	
def reclip(clipping, rect, size):
	left=(clipping[1].real-clipping[0].real)*float(rect.left)/size[0]+clipping[0].real
	right=(clipping[1].real-clipping[0].real)*float(rect.right)/size[0]+clipping[0].real
	up=(clipping[1].imag-clipping[0].imag)*float(rect.bottom)/size[1]+clipping[0].imag
	down=(clipping[1].imag-clipping[0].imag)*float(rect.top)/size[1]+clipping[0].imag
	newclip=(complex(min(left,right),max(up,down)), complex(max(left,right),min(up,down)))
	return newclip
	
start=time.time()
pygame.init()
size=(400,300)
maxiter=200
fps=pygame.time.Clock()
windowSurface=pygame.display.set_mode(size)
mandelSurface=pygame.Surface(size)

clipping=(-2.5+1.5j, 1.5-1.5j)
complmat=np.zeros(size, dtype=complex)
limitmat=np.zeros(size, dtype=int)
cvalmat=np.zeros(size, dtype=complex)
calc_clipping(mandelSurface, complmat, limitmat, clipping)
draw_iter(mandelSurface, limitmat, maxiter, size)
ausschnitt=None

try:
	while 1:
		windowSurface.blit(mandelSurface, (0,0))
		for event in pygame.event.get():
			if event.type==pl.MOUSEBUTTONUP:
				if not ausschnitt:
					ausschnitt=imageSection(windowSurface, event.pos)
				else:
					ausschnitt.resize(event.pos)
					#hier clipping resize
					clipping=reclip(clipping, ausschnitt.rect, size)
					ausschnitt=None
					calc_clipping(mandelSurface, complmat, limitmat, clipping)
					draw_iter(mandelSurface, limitmat, maxiter, size)
			elif event.type ==pl.MOUSEMOTION:
				if ausschnitt:
					ausschnitt.resize(event.pos)
				
		if ausschnitt:
			windowSurface.blit(mandelSurface, (0,0))
			ausschnitt.draw()
		pygame.display.update()
		fps.tick(20)
except RuntimeError:
	pygame.quit()
