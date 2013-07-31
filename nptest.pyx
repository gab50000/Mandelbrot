import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
def nonlineq(np.ndarray[np.complex128_t, ndim=2] zmat, np.ndarray[np.complex128_t, ndim=2] cmat, np.ndarray[np.uint16_t, ndim=2] itermat, double limitsquare, int maxiter):
	cdef unsigned int i,j
#~ 	cdef Py_ssize_t i,j
	cdef double a
	for iteration in range(maxiter):
		for i in range(zmat.shape[0]):
			for j in range(zmat.shape[1]):
				if square(zmat[i,j].real, zmat[i,j].imag) < limitsquare:
#~ 					zmat[i,j]=nonlina(zmat[i,j],cmat[i,j])
					a=nonlin_real(zmat[i,j].real, zmat[i,j].imag, cmat[i,j].real)
					zmat[i,j].imag=nonlin_imag(zmat[i,j].real, zmat[i,j].imag, cmat[i,j].imag)
					zmat[i,j].real=a
					itermat[i,j]+=1
					
@cython.boundscheck(False)
def nonlineq2(np.ndarray[np.complex128_t, ndim=2] zmat, np.ndarray[np.uint16_t, ndim=2] itermat, double boundleft, double boundright, double boundup, double bounddown, double limitsquare, int maxiter):
	cdef unsigned int i,j
#~ 	cdef Py_ssize_t i,j
	cdef double a, creal, cimag
	for iteration in range(maxiter):
		for i in range(zmat.shape[0]):
			for j in range(zmat.shape[1]):
				creal=boundleft+(boundright-boundleft)/zmat.shape[0]*i
				cimag=bounddown+(boundup-bounddown)/zmat.shape[1]*j
				if square(zmat[i,j].real, zmat[i,j].imag) < limitsquare:
#~ 					zmat[i,j]=nonlina(zmat[i,j],cmat[i,j])
					a=nonlin_real(zmat[i,j].real, zmat[i,j].imag, creal)
					zmat[i,j].imag=nonlin_imag(zmat[i,j].real, zmat[i,j].imag, cimag)
					zmat[i,j].real=a
					itermat[i,j]+=1

#~ def nonlineq3(np.ndarray[np.uint16_t, ndim=2] itermat, double boundleft, double boundright, double boundup, double bounddown, double limitsquare, int maxiter):
#~ 	cdef unsigned int i,j
#~ 	cdef double a, creal, cimag
#~ 	for i in range(itermat.shape[0]):
#~ 		for j in range(itermat.shape[1]):
#~ 			
#~ 			for iteration in range(maxiter):

cdef double square(double a, double b):
	return a*a+b*b

cdef nonlina(complex z, complex c):
	return complex(z.real*z.real-z.imag*z.imag+c.real, 2*z.real*z.imag+c.imag)

cdef nonlin_real(double a, double b, double c):
	return a*a-b*b+c
	
cdef nonlin_imag(double a, double b, double c):
	return 2*a*b+c
