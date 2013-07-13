import numpy as np
cimport numpy as np
cimport cython

@cython.boundscheck(False)
def nonlineq(np.ndarray[np.complex128_t, ndim=2] zmat, np.ndarray[np.complex128_t, ndim=2] cmat, np.ndarray[np.int64_t, ndim=2] itermat, double limitsquare, int maxiter):
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

cdef double square(double a, double b):
	return a*a+b*b

cdef nonlina(complex z, complex c):
	return complex(z.real*z.real-z.imag*z.imag+c.real, 2*z.real*z.imag+c.imag)

cdef nonlin_real(double a, double b, double c):
	return a*a-b*b+c
	
cdef nonlin_imag(double a, double b, double c):
	return 2*a*b+c
