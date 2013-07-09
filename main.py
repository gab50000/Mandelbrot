#!/usr/bin/python

import pygame
import pygame.locals as pl
import cmath, math
import numpy as np

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
		return pygame.Color(0,0,0)

def draw_imag(surface, complmat, (xmax, ymax)):
	pa=pygame.PixelArray(surface)	
	for x in xrange(xmax):
		for y in xrange(ymax):
			pa[x][y]=imagcolor(complmat[x,y])
	del pa
	
def calc_converge(surface, limitmat, complmat, cvalmat, maxiter, maxdev):
	startvalmat=np.array(complmat)
	for i in xrange(maxiter):
		complmat=complmat*complmat+cvalmat
		limitmat+=(complmat-startvalmat)<maxdev

def draw_iter(surface, limitmat, maxlimit, (xmax, ymax)):
	pa=pygame.PixelArray(surface)
	for x in xrange(xmax):
		for y in xrange(ymax):
			pa[x][y]=pygame.Color(*[limitmat[x,y]/maxlimit*255]*3)
	
pygame.init()
size=(1024,768)
fps=pygame.time.Clock()
windowSurface=pygame.display.set_mode(size)

clipping=(-2-2j, 2+2j)
complmat=np.zeros(size, dtype=complex)
cvalmat=np.array([[complex(clipping[0].real+j*(clipping[1].real-clipping[0].real)/size[0], clipping[0].imag+i*(clipping[1].imag-clipping[0].imag)/size[1]) for i in xrange(size[1])] for j in xrange(size[0])])
limitmat=np.zeros(size, dtype=int)

for i in xrange(200):
	print i
	complmat=complmat*complmat+cvalmat

try:
	while 1:
		draw_imag(windowSurface, complmat, size)
		pygame.display.update()
		fps.tick(1)
		
		for event in pygame.event.get():
			if event.type==pl.MOUSEBUTTONDOWN:
				complmat=complmat*complmat+cvalmat
				#~ for i in xrange(size[0]):
					#~ for j in xrange(size[1]):
						#~ complmat[i,j]=nonlineq(complmat[i,j], complex(clipping[0].real+i*(clipping[1].real-clipping[0].real)/size[0], clipping[0].imag+j*(clipping[1].imag-clipping[0].imag)/size[1]))
		
except RuntimeError:
	pygame.quit()
