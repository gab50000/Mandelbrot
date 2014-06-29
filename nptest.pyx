import numpy as np
cimport numpy as np
cimport cython
from cython.parallel import prange

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.cdivision(True)
def nonlineq(np.complex128_t [:, ::1] zmat, np.complex128_t [:, ::1] cmat, np.uint16_t[:, ::1] itermat, double limitsquare, int maxiter):
	# cdef int i,j, iteration
	cdef Py_ssize_t i,j, iteration
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
@cython.wraparound(False)
@cython.cdivision(True)
def nonlineq_2(np.complex128_t [:, ::1] cmat, np.uint16_t[:, ::1] itermat, double limitsquare, int maxiter):
	# cdef int i,j, iteration
	cdef Py_ssize_t i,j, iteration
	cdef double a
	cdef double z_real
	cdef double z_imag
	for i in range(cmat.shape[0]):
		for j in range(cmat.shape[1]):
			z_real = 0
			z_imag = 0
			for iteration in range(maxiter):
				if square(z_real, z_imag) < limitsquare:
					a=nonlin_real(z_real, z_imag, cmat[i,j].real)
					z_imag=nonlin_imag(z_real, z_imag, cmat[i,j].imag)
					z_real=a
					itermat[i,j]+=1


cdef double square(double a, double b) nogil:
	return a*a+b*b

cdef complex nonlina(complex z, complex c):
	return complex(z.real*z.real-z.imag*z.imag+c.real, 2*z.real*z.imag+c.imag)

cdef double nonlin_real(double a, double b, double c) nogil:
	return a*a-b*b+c
	
cdef double nonlin_imag(double a, double b, double c) nogil:
	return 2*a*b+c

# cdef double square(double a, double b) nogil:
# 	cdef double result = a*a+b*b
# 	return result

# cdef nonlina(complex z, complex c):
# 	return complex(z.real*z.real-z.imag*z.imag+c.real, 2*z.real*z.imag+c.imag)

# cdef nonlin_real(double a, double b, double c) nogil:
# 	cdef double result 
# 	result = a*a-b*b+c
# 	return result
	
# cdef nonlin_imag(double a, double b, double c) nogil:
# 	cdef double result
# 	result = 2*a*b+c
# 	return result
