import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import parallel, prange

@cython.boundscheck(False)
def nonlineq(np.ndarray[np.complex128_t, ndim=2] zmat, np.ndarray[np.complex128_t, ndim=2] cmat, np.ndarray[np.int64_t, ndim=2] itermat, double limitsquare, int maxiter):
	cdef unsigned int i,j
	cdef unsigned int iteration=0
	for iteration in range(maxiter):
		for i in range(zmat.shape[0]):
			for j in range(zmat.shape[1]):
				if square(zmat[i,j].real, zmat[i,j].imag) < limitsquare:
					zmat[i,j]=nonlin(zmat[i,j],cmat[i,j])
					itermat[i,j]+=1

cdef double square(double a, double b):
	return a*a+b*b

cdef nonlin(complex z, complex c):
	return complex(z.real*z.real-z.imag*z.imag+c.real, 2*z.real*z.imag+c.imag)
