"""
Module for polynomial related LazyLinearOps.
"""
import numpy as np
from numpy.polynomial import Polynomial as P
import scipy as sp
from lazylinop import *
import warnings
warnings.simplefilter(action='always')


try:
    import dask
    from dask.distributed import Client, LocalCluster, wait
except ImportError:
    print("Dask ImportError")


class poly(P):#np.polynomial.Polynomial):
    def __init__(self, p, op=None):
        """Init instance of poly.

        Args:
            p: numpy.polynomial.Polynomial
            op: LazyLinearOp

        References:
            See `numpy.polynomial package <https://numpy.org/doc/stable/reference/routines.polynomials.html>`_ for more details.
        """
        self.__p = p
        self.__op = op

    def _val(self, op=None, basis: str='monomial'):
        # TODO
        pass
        # # # Check if coeffs is not None
        # # if self.__p.coeffs is None:
        # #     if self.__basis == 'monomial':
        # #         self.coeffs = np.polynomial.polynomial.polyfromroots(self.roots)
        # #     elif self.__basis == 'chebyshev':
        # #         self.coeffs = np.polynomial.chebyshev.chebfromroots(self.roots)
        # #     else:
        # #         pass
        # # Call polyval according to the basis
        # if basis == 'monomial':
        #     if self.__op is not None or op is not None:
        #         if self.__p.__basis == 'monomial':
        #             return polyval(self.__p.coef, self.__op if op is None else op)
        #         else:
        #             return polyval(np.polynomial.chebyshev.cheb2poly(self.coeffs), self.__L if L is None else L)
        #     else:
        #         raise Exception('LazyLinearOp is None.')
        # elif basis == 'chebyshev':
        #     if self.__L is not None or L is not None:
        #         if self.__basis == 'monomial':
        #             return chebval(
        #                 np.polynomial.chebyshev.poly2cheb(self.coeffs),
        #                 self.__L if L is None else L)
        #         else:
        #             return chebval(self.coeffs, self.__L if L is None else L)
        #     else:
        #         raise Exception('LazyLinearOp is None.')
        # else:
        #     pass

    def __call__(self, op=None, basis: str='monomial', n: int=1):
        """
        Thanks to Python __call__ instance behaves like function.
        """
        if n is not None and n > 1:
            # Compute n-th powers of self.__L
            return power(n, self.__op if op is None else op, use_numba=True)
        else:
            # Compute polynomial of LazyLinearOp
            return poly._val(self, op, basis)


class lpoly():
    """This class implements a polynomial that is described
    by coefficients, roots and basis representation (monomial or Chebyshev).
    If coefficients are not given, compute from roots.
    If roots are not given, compute from coefficients.
    Therefore, coefficients and roots from a poly instance are always not None.
    It is also possible to assign a LazyLinearOp. You can add, subtract
    and multiply two instances p1 and p2. Thanks to Python `__call__`
    you can add two instances p1 and p2 and use the syntax `(p1+p2)(Op) @ x`
    to compute polynomial of LazyLinearOp Op applied to a vector x.
    To compute n-th power of LazyLinearOp applied to vector x simply use `p1(Op, n=n) @ x`.
    Thanks to Numpy/SciPy functions you can switch between monomial and
    Chebyshev basis.
    """

    def __init__(self, L=None, coeffs=None, roots=None, basis: str='monomial'):
        """Init instance of poly.

        Args:
            L: LazyLinearOp
            coeffs: 1d or 2d array
            roots: 1d or 2d array
            basis: str, optional
        """
        # lazy linear operator
        self.__L = L
        # basis
        if basis != 'monomial' and basis != 'chebyshev':
            raise ValueError('basis must be either monomial or chebyshev.')
        else:
            self.__basis = basis
        # Polynomial coefficients and roots from a poly
        # instance are always not None.
        if coeffs is not None and roots is None:
            self.coeffs = coeffs
            if basis == 'monomial':
                self.roots = np.polynomial.polynomial.polyroots(coeffs)
            elif basis == 'chebyshev':
                self.roots = np.polynomial.chebyshev.chebroots(coeffs)
        elif coeffs is not None and roots is not None:
            self.coeffs = coeffs
            self.roots = roots
        elif coeffs is None and roots is not None:
            if basis == 'monomial':
                self.coeffs = np.polynomial.polynomial.polyfromroots(roots)
            elif basis == 'chebyshev':
                self.coeffs = np.polynomial.chebyshev.chebfromroots(roots)
            self.roots = roots
        else:
            raise Exception('Expect coeffs or roots to be different from None.')

    def print(self):
        """Print polynomial details.
        """
        print('coefficients:')
        print(self.coeffs)
        print('roots:')
        print(self.roots)
        print('basis:')
        print(self.__basis)
        print('LazyLinearOp:')
        print(self.__L)

    @property
    def L(self):
        return self.__L

    @L.setter
    def L(self, op):
        """Change LazyLinearOp of self instance.

        Args:
            op: LazyLinearOp
        """
        self.__L = op

    def get_coeffs(self):
        return self.coeffs

    def set_coeffs(self, coeffs, basis):
        """Change coefficients of self instance.

        Args:
            roots: 1d or 2d array
        """
        self.coeffs = coeffs
        # Polynomial coefficients and roots from a poly
        # instance are always not None.
        if basis == 'monomial':
            self.roots = np.polynomial.polynomial.polyroots(coeffs)
        else:
            self.roots = np.polynomial.chebyshev.chebroots(coeffs)

    # @property
    # def coeffs(self):
    #     return self.coeffs

    # @coeffs.setter
    # def coeffs(self, coeffs, basis):
    #     """Change coefficients of self instance.

    #     Args:
    #         roots: 1d or 2d array
    #     """
    #     self.coeffs = coeffs
    #     if basis == 'monomial':
    #         self.roots = np.polynomial.polynomial.polyroots(coeffs)
    #     else:
    #         self.roots = np.polynomial.chebyshev.chebroots(coeffs)

    def get_roots(self):
        return self.roots

    def set_roots(self, roots):
        """Change roots of self instance.

        Args:
            roots: 1d or 2d array
        """
        self.roots = roots
        # Polynomial coefficients and roots from a poly
        # instance are always not None.
        if basis == 'monomial':
            self.coeffs = np.polynomial.polynomial.polyfromroots(roots)
        else:
            self.coeffs = np.polynomial.chebyshev.chebfromroots(roots)

    # @property
    # def roots(self):
    #     return self.roots

    # @roots.setter
    # def roots(self, roots):
    #     """Change roots of self instance.

    #     Args:
    #         roots: 1d or 2d array
    #     """
    #     self.roots = roots
    #     if basis == 'monomial':
    #         self.coeffs = np.polynomial.polynomial.polyfromroots(roots)
    #     else:
    #         self.coeffs = np.polynomial.chebyshev.chebfromroots(roots)

    @property
    def basis(self):
        return self.__basis

    @basis.setter
    def basis(self, basis):
        """Change basis of self instance.

        Args:
            basis: str
        """
        if self.__basis != basis:
            if self.__basis == 'monomial' and basis == 'chebyshev':
                self.coeffs = np.polynomial.chebyshev.poly2cheb(self.coeffs)
                self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)
            if self.__basis == 'chebyshev' and basis == 'monomial':
                self.coeffs = np.polynomial.chebyshev.cheb2poly(self.coeffs)
                self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
            self.__basis = basis

    # Evaluation of a (Chebyshev) polynomial from coefficients
    def _val(self, L=None, basis: str='monomial'):
        # Check if coeffs is not None
        if self.coeffs is None:
            if self.__basis == 'monomial':
                self.coeffs = np.polynomial.polynomial.polyfromroots(self.roots)
            elif self.__basis == 'chebyshev':
                self.coeffs = np.polynomial.chebyshev.chebfromroots(self.roots)
            else:
                pass
        # Call polyval according to the basis
        if basis == 'monomial':
            if self.__L is not None or L is not None:
                if self.__basis == 'monomial':
                    return polyval(self.coeffs, self.__L if L is None else L)
                else:
                    return polyval(np.polynomial.chebyshev.cheb2poly(self.coeffs), self.__L if L is None else L)
            else:
                raise Exception('LazyLinearOp is None.')
        elif basis == 'chebyshev':
            if self.__L is not None or L is not None:
                if self.__basis == 'monomial':
                    return chebval(
                        np.polynomial.chebyshev.poly2cheb(self.coeffs),
                        self.__L if L is None else L)
                else:
                    return chebval(self.coeffs, self.__L if L is None else L)
            else:
                raise Exception('LazyLinearOp is None.')
        else:
            pass

    # Thanks to Python __call__ instance behaves like function
    def __call__(self, L=None, basis: str='monomial', n: int=1):
        if n is not None and n > 1:
            # Compute n-th powers of self.__L
            return power(n, self.__L if L is None else L, use_numba=True)
        else:
            # Compute polynomial of LazyLinearOp
            return lpoly._val(self, L, basis)

    def __add__(self, p):
        """Add two poly instances and return poly instance
        with monomial basis.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p1 + p1
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'chebyshev':
            coeffs1 = np.polynomial.chebyshev.cheb2poly(coeffs1)
        if p.basis == 'chebyshev':
            coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
        coeffs = np.polynomial.polynomial.polyadd(coeffs1, coeffs2)
        return lpoly(L=None, coeffs=coeffs, roots=None, basis='monomial')

    def polyadd(self, c):
        """Add coefficients c to `self.coeffs`.

        Args:
            c: 1d or 2d array
        """
        if self.__basis == 'monomial':
            self.coeffs = np.polynomial.polynomial.polyadd(self.coeffs, c)
            self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
        elif self.__basis == 'chebyshev':
            self.coeffs = np.polynomial.chebyshev.chebadd(self.coeffs, c)
            self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)

    def __sub__(self, p):
        """Subtract two poly instances and return poly instance
        with monomial basis.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p1 - p1
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'chebyshev':
            coeffs1 = np.polynomial.chebyshev.cheb2poly(coeffs1)
        if p.basis == 'chebyshev':
            coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
        coeffs = np.polynomial.polynomial.polysub(coeffs1, coeffs2)
        return lpoly(L=None, coeffs=coeffs, roots=None, basis='monomial')

    def polysub(self, c):
        """Subtract coefficients c to `self.coeffs`.

        Args:
            c: 1d or 2d array
        """
        if self.__basis == 'monomial':
            self.coeffs = np.polynomial.polynomial.polysub(self.coeffs, c)
            self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
        elif self.__basis == 'chebyshev':
            self.coeffs = np.polynomial.chebyshev.chebsub(self.coeffs, c)
            self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)

    def __mul__(self, p):
        """Multiply two poly instances.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p1 * p1
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'chebyshev':
            coeffs1 = np.polynomial.chebyshev.cheb2poly(coeffs1)
        if p.basis == 'chebyshev':
            coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
        coeffs = np.polynomial.polynomial.polymul(coeffs1, coeffs2)
        return lpoly(L=None, coeffs=coeffs, roots=None, basis='monomial')

    def polymul(self, c):
        """Multiply coefficients c by and to `self.coeffs`.

        Args:
            c: 1d or 2d array
        """
        self.coeffs = np.polynomial.polynomial.polymul(self.coeffs, c)
        self.roots = np.polynomial.polynomial.polyroots(self.coeffs)

    def __floordiv__(self, p):
        """Divide (floor division) two poly instances.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p1 // p1
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'chebyshev':
            coeffs1 = np.polynomial.chebyshev.cheb2poly(coeffs1)
        if p.basis == 'chebyshev':
            coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
        coeffs = np.polynomial.polynomial.polydiv(coeffs1, coeffs2)
        return lpoly(L=None, coeffs=coeffs[0], roots=None, basis='monomial')

    def __truediv__(self, p):
        """Divide (true division) two poly instances.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p1 / p1
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'chebyshev':
            coeffs1 = np.polynomial.chebyshev.cheb2poly(coeffs1)
        if p.basis == 'chebyshev':
            coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
        coeffs = np.polynomial.polynomial.polydiv(coeffs1, coeffs2)
        return lpoly(L=None, coeffs=coeffs, roots=None, basis='monomial')

    def polydiv(self, c, div: str='true'):
        """Divide coefficients c by and to `self.coeffs`.

        Args:
            c: 1d or 2d array
            div: str, optional default is 'true'
            div must be either 'true', 'floor' or 'modulo'.
        """
        if self.__basis == 'monomial':
            if div == 'true':
                # TODO
                self.coeffs = np.polynomial.polynomial.polydiv(self.coeffs, c)
            elif div == 'floor':
                self.coeffs = np.polynomial.polynomial.polydiv(self.coeffs, c)[0]
            elif div == 'modulo':
                self.coeffs = np.polynomial.polynomial.polydiv(self.coeffs, c)[1]
            self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
        elif self.__basis == 'chebyshev':
            if div == 'true':
                # TODO
                self.coeffs = np.polynomial.chebyshev.chebdiv(self.coeffs, c)
            elif div == 'floor':
                self.coeffs = np.polynomial.chebyshev.chebdiv(self.coeffs, c)[0]
            elif div == 'modulo':
                self.coeffs = np.polynomial.chebyshev.chebdiv(self.coeffs, c)[1]
            self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)

    def __mod__(self, p):
        """Divide two poly instances and keep the modulo.

        Args:
            p: poly instance

        Examples:
            >>> import lazylinop.wip.polynomial as p
            >>> p1 = p.lpoly(L=None, coeffs=[1.0, 1.0], basis='monomial')
            >>> p2 = p.lpoly(L=None, coeffs=[1.0, 1.0, 2.0], basis='monomial')
            >>> p3 = p1 % p2
        """
        coeffs1 = self.coeffs
        coeffs2 = p.coeffs
        if self.__basis == 'monomial':
            if p.basis == 'chebyshev':
                coeffs2 = np.polynomial.chebyshev.cheb2poly(coeffs2)
            coeffs = np.polynomial.polynomial.polydiv(coeffs1, coeffs2)[1]
            return lpoly(L=None, coeffs=coeffs, roots=None, basis='monomial')
        elif self.__basis == 'chebyshev':
            if p.basis == 'monomial':
                coeffs2 = np.polynomial.polynomial.poly2cheb(coeffs2)
            coeffs = np.polynomial.chebyshev.chebdiv(coeffs1, coeffs2)[1]
            return lpoly(L=None, coeffs=coeffs, roots=None, basis='chebyshev')
        else:
            return None

    def __eq__(self, p):
        """Check if two polynomial are equal.
        """
        return self.__basis == p.basis and np.allclose(self.coeffs, p.get_coeffs())

    def polyder(self, m: int=1, scl: float=1.0):
        """Constructs the m-th derivative of the polynomial c.
        
           References:
           See `NumPy, SciPy polyint <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyder.html>`_ for more details.
        """
        if self.__basis == 'monomial':
            self.coeffs = np.polynomial.polynomial.polyder(c, m, scl)
            self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
        elif self.__basis == 'chebyshev':
            self.coeffs = np.polynomial.chebyshev.chebder(c, m, scl)
            self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)
        else:
            pass

    def polyint(self, m: int=1, k: list=[], lbnd: float=0.0, scl: float=1.0):
        """Constructs the m-th integral of the polynomial c.

           References:
           See `NumPy, SciPy polyint <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyint.html>`_ for more details.
        """
        if self.__basis == 'monomial':
            self.coeff = np.polynomial.polynomial.polyint(c, m, k, lbnd, scl)
            self.roots = np.polynomial.polynomial.polyroots(self.coeffs)
        elif self.__basis == 'chebyshev':
            self.coeff = np.polynomial.chebyshev.chebint(c, m, k, lbnd, scl)
            self.roots = np.polynomial.chebyshev.chebroots(self.coeffs)
        else:
            pass


def chebval(c, L):
    """Constructs a Chebyshev polynomial of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[n] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the n-th polynomial.
    The k-th Chebyshev polynomial can be computed by recurrence:
    T_0(X)     = 1
    T_1(X)     = X
    T_{k+1}(X) = 2*X*T_k(X) - T_{k-1}(X)

    Args:
        c: 1d or 2d array
            List of coefficients [c_00, c_01, ..., c_0n]
                                   .     .          .
                                   .     .          .
                                   .     .          .
                                 [c_m0, c_m1, ..., c_mn].
            If the size of the list is n + 1 then the largest power of the polynomial is n.
            If the array is 2d (shape (m + 1, n + 1)), the function considers one polynomial
            per row (m + 1 polynomials in total).
            The shape of the output P(L) @ X is (L.shape[0], X.shape[1], m + 1).
            P(L) is equal to c_00 * Id + c_01 * L^1 + ... + c_0n * L^n.
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `Wikipedia <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.
        See also `Polynomial magic web page <https://francisbach.com/chebyshev-polynomials/>`_.
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebval.html>`_.
    """

    c = np.asarray(c)

    if c.ndim == 1:
        # only one polynomial
        C, D = 1, c.shape[0]
        c = c.reshape(C, D)
    else:
        # multiple polynomials
        C, D = c.shape

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size, C), dtype=x.dtype)
        T1x = np.empty(L.shape[0], dtype=x.dtype)
        T2x = np.empty(L.shape[0], dtype=x.dtype)
        # loop over the batch size
        for b in range(batch_size):
            # loop over the polynomials
            for p in range(C):
                T0x = np.multiply(c[p, 0], x[:, b])
                np.copyto(output[:, b, p], T0x)
                if D > 1:
                    # loop over the coefficients
                    for i in range(1, D):
                        if i == 1:
                            np.copyto(T1x, L @ x[:, b])
                            if c[p, i] == 0.0:
                                continue
                            else:
                                np.add(output[:, b, p], np.multiply(c[p, i], T1x), out=output[:, b, p])
                        else:
                            np.copyto(T2x, np.subtract(np.multiply(2.0, L @ T1x), T0x))
                            # Recurrence
                            np.copyto(T0x, T1x)
                            np.copyto(T1x, T2x)
                            if c[p, i] == 0.0:
                                continue
                            else:
                                np.add(output[:, b, p], np.multiply(c[p, i], T2x), out=output[:, b, p])
        if C == 1:
            return output[:, 0, 0] if is_1d else output[:, :, 0]
        else:
            return output

    return LazyLinearOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def chebvalfromroots(r, L):
    """Constructs a Chebyshev polynomial (from roots) of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[n] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the n-th polynomial.
    The k-th Chebyshev polynomial can be computed by recurrence:
    T_0(X)     = 1
    T_1(X)     = X
    T_{k+1}(X) = 2*X*T_k(X) - T_{k-1}(X)

    Args:
        r: 1d or 2d array
            List of roots [r_00, r_01, ..., r_0n]
                            .     .          .
                            .     .          .
                            .     .          .
                          [r_m0, r_m1, ..., r_mn].
            If the size of the list is n + 1 then the largest power of the polynomial is n.
            If the array is 2d (shape (m + 1, n + 1)), the function considers one polynomial
            per row (m + 1 polynomials in total).
            The shape of the output P(L) @ X is (L.shape[0], X.shape[1], m + 1).
            P(L) is equal to (L - r_00 * Id) * (L - r_01 * Id) * ... * (L - r_0n * Id).
            To convert roots to coefficients use `NumPy, SciPy chebfromroots function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebfromroots.html>`_.
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `Wikipedia <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.
        See also `Polynomial magic web page <https://francisbach.com/chebyshev-polynomials/>`_.
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebval.html>`_.
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebfromroots.html>`_.
        See also :py:func:`chebval`.
    """
    r = np.asarray(r)
    if r.ndim == 1:
        coeffs = np.polynomial.chebyshev.chebfromroots(r)
    else:
        x, y = r.shape
        coeffs = np.empty((x, y + 1), dtype=r.dtype)
        for i in range(x):
            coeffs[i, :] = np.polynomial.chebyshev.chebfromroots(r[i, :])
    return chebval(coeffs, L)


def chebadd(c1, c2, L):
    """Constructs a Chebyshev polynomial c1 + c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the addition of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] + c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy polyadd function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebadd.html>`_ for more details.
        See also :py:func:`chebval`.
    """
    c = np.polynomial.chebyshev.chebadd(c1, c2)
    return chebval(c, L)


def chebsub(c1, c2, L):
    """Constructs a Chebyshev polynomial c1 - c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the subtraction of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] - c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy chebsub function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebsub.html>`_ for more details.
        See also :py:func:`chebval`.
    """
    c = np.polynomial.chebyshev.chebsub(c1, c2)
    return chebval(c, L)


def chebmul(c1, c2, L):
    """Constructs a Chebyshev polynomial c1 * c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the multiplication of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] * c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy chebmul function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebmul.html>`_ for more details.
        See also :py:func:`chebval`.
    """
    c = np.polynomial.chebyshev.chebmul(c1, c2)
    return chebval(c, L)


def chebdiv(c1, c2, L):
    """Constructs a Chebysehv polynomial c1 / c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[n] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the multiplication of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] / c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy chebdiv function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.chebyshev.chebdiv.html>`_ for more details.
        See also :py:func:`chebval`.
    """
    c = np.polynomial.chebyshev.chebdiv(c1, c2)
    return chebval(c, L)


def polyval(c, L):
    """Constructs a polynomial of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.
    Computation of P(L) @ X uses Horner method.

    Args:
        c: 1d or 2d array
            List of coefficients [c_00, c_01, ..., c_0n]
                                   .     .          .
                                   .     .          .
                                   .     .          .
                                 [c_m0, c_m1, ..., c_mn].
            If the size of the list is n + 1 then the largest power of the polynomial is n.
            If the array is 2d (shape (m + 1, n + 1)), the function considers one polynomial
            per row (m + 1 polynomials in total).
            The shape of the output P(L) @ X is (L.shape[0], X.shape[1], m + 1).
            P(L) is equal to c_00 * Id + c_01 * L^1 + ... + c_0n * L^n.
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        See also :py:func:`polyvalfromroots`.
    """

    c = np.asarray(c)

    if c.ndim == 1:
        # only one polynomial
        C, D = 1, c.shape[0]
        c = c.reshape(C, D)
    else:
        # multiple polynomials
        C, D = c.shape

    def _matmat(L, x, c):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size, C), dtype=x.dtype)
        Lx = np.empty(L.shape[0], dtype=x.dtype)
        # loop over the batch size
        for b in range(batch_size):
            # loop over the polynomials
            for p in range(C):
                output[:, b, p] = np.multiply(c[p, 0], x[:, b])
                if D > 1:
                    # loop over the coefficients
                    for i in range(1, D):
                        if i == 1:
                            np.copyto(Lx, L @ x[:, b])
                        else:
                            np.copyto(Lx, L @ Lx)
                        if c[p, i] == 0.0:
                            continue
                        else:
                            np.add(output[:, b, p], np.multiply(c[p, i], Lx), out=output[:, b, p])
        if C == 1:
            return output[:, 0, 0] if is_1d else output[:, :, 0]
        else:
            return output

    return LazyLinearOp(
        shape=L.shape,
        matmat=lambda x: _matmat(L, x, c),
        rmatmat=lambda x: _matmat(L.T.conj(), x, c)
    )


def polyvalfromroots(r, L):
    """Constructs a polynomial (from roots) of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        r: 1d or 2d array
            List of roots [r_00, r_01, ..., r_0n]
                            .     .          .
                            .     .          .
                            .     .          .
                          [r_m0, r_m1, ..., r_mn].
            If the size of the list is n + 1 then the largest power of the polynomial is n.
            If the array is 2d (shape (m + 1, n + 1)), the function considers one polynomial
            per row (m + 1 polynomials in total).
            The shape of the output P(L) @ X is (L.shape[0], X.shape[1], m + 1).
            P(L) is equal to (L - r_00 * Id) * (L - r_01 * Id) * ... * (L - r_0n * Id).
            To convert roots to coefficients use `NumPy, SciPy polyfromroots function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyfromroots.html>`_.
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        See also :py:func:`polyval`.
    """

    if r.ndim == 1:
        # only one polynomial
        P, R = 1, r.shape[0]
        r = r.reshape(P, R)
    else:
        # multiple polynomials
        P, R = r.shape

    def _matmat(r, L, x):
        if L.shape[1] != x.shape[0]:
            raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        output = np.empty((L.shape[0], batch_size, P), dtype=x.dtype)
        Lx = np.empty(L.shape[0], dtype=x.dtype)
        # loop over the batch size (Dask ?)
        for b in range(batch_size):
            # loop over the polynomials
            for p in range(P):
                # loop over the roots
                if r[p, R - 1] == 0.0:
                    np.copyto(Lx, L @ x[:, b])
                else:
                    np.copyto(Lx, np.subtract(L @ x[:, b], np.multiply(r[p, R - 1], x[:, b])))
                if R > 1:
                    for i in range(1, R):
                        if r[p, R - 1 - i] == 0.0:
                            np.copyto(Lx, L @ Lx)
                        else:
                            np.copyto(Lx, np.subtract(L @ Lx, np.multiply(r[p, R - 1 - i], Lx)))
                np.copyto(output[:, b, p], Lx)
        if P == 1:
            return output[:, 0, 0] if is_1d else output[:, :, 0]
        else:
            return output

    return LazyLinearOp(
        shape=L.shape,
        matmat=lambda x: _matmat(r, L, x),
        rmatmat=lambda x: _matmat(r, L.T.conj(), x)
    )


def power(n, L, use_numba: bool=False):
    """Constructs power L^n of linear operator L as a lazy linear operator P(L).

    Args:
        n: int
            Raise the linear operator to degree n.
        L: 2d array
            Linear operator.
        use_numba: bool, optional
            If True, use prange from Numba (default is False)
            to compute batch in parallel.
            It is useful only and only if the batch size and
            the length of a are big enough.

    Returns:
        LazyLinearOp

    Raises:

    Examples:
        >>> from lazylinop.wip.polynomial import power
        >>> Op = power(3, eye(3, n=3, k=0))
        >>> x = np.full(3, 1.0)
        >>> np.allclose(Op @ x, x)
        True
        >>> Op = power(3, eye(3, n=3, k=1))
        >>> x = np.full(3, 1.0)
        >>> np.allclose(Op @ x, np.zeros(3, dtype=np.float_))
        True

    References:
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
    """

    def _matmat(n, L, x):

        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = int(not use_numba)
        nb.config.THREADING_LAYER = 'omp'
        if not use_numba:
            nb.config.DISABLE_JIT = 1

        def _1d(n, L, x):
            output = L @ x
            if n > 1:
                for n in range(1, n):
                    output[:] = L @ output[:]
            return output

        def _2d_no_numba(n, L, x):
            output = L @ x
            if n > 1:
                for n in range(1, n):
                    output[:, :] = L @ output[:, :]
            return output

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(n, L, x):
            batch_size = x.shape[1]
            output = np.empty((L.shape[0], batch_size), dtype=x.dtype)
            # loop over the batch size
            for b in prange(batch_size):
                output[:, b] = L @ x[: ,b]
                if n > 1:
                    for n in range(1, n):
                        output[:, b] = L @ output[:, b]
            return output

        if use_numba:
            return _1d(n, L, x) if x.ndim == 1 else _2d(n, L, x)
        else:
            return _1d(n, L, x) if x.ndim == 1 else _2d_no_numba(n, L, x)
    

    return LazyLinearOp(
        shape=L.shape,
        matmat=lambda x: _matmat(n, L, x),
        rmatmat=lambda x: _matmat(n, L.T.conj(), x)
    )


def polyadd(c1, c2, L):
    """Constructs a polynomial c1 + c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the addition of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] + c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        See also `NumPy, SciPy polyadd function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyadd.html>`_ for more details.
        See also :py:func:`polyval`.
    """
    c = np.polynomial.polynomial.polyadd(c1, c2)
    return polyval(c, L)


def polysub(c1, c2, L):
    """Constructs a polynomial c1 - c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the subtraction of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] - c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy polyadd function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polysub.html>`_ for more details.
        See also :py:func:`polyval`.
    """
    c = np.polynomial.polynomial.polysub(c1, c2)
    return polyval(c, L)


def polymul(c1, c2, L):
    """Constructs a polynomial c1 * c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the multiplication of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] * c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy, SciPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        See also `NumPy, SciPy polymul function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polymul.html>`_ for more details.
        See also :py:func:`polyval`.
    """
    c = np.polynomial.polynomial.polymul(c1, c2)
    return polyval(c, L)


def polydiv(c1, c2, L):
    """Constructs a polynomial c1 / c2 of linear operator L as a lazy linear operator P(L).
    Y = P(L) @ X returns a tensor. The first dimension is the result of P(L)[k] @ X[:, j]
    where j is the j-th column of X, the second dimension corresponds to the
    batch size while the third dimension corresponds to the k-th polynomial.

    Args:
        c1: 1d or 2d array
            List of coefficients of the first polynomial.
            If shape of c1 is (M1, N1) we have M1 polynomials
            and largest power is N1 - 1.
        c2: 1d or 2d array
            List of coefficients of the second polynomial.
            If shape of c2 is (M2, N2) we have M2 polynomials
            and largest power is N2 - 1.
            The coefficients corresponding to the multiplication of the two polynomials is
            c1[:min(M1, M2), :min(N1, N2)] / c2[:min(M1, M2), :min(N1, N2)].
        L: 2d array
            Linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.

    Examples:

    References:
        See also `NumPy polynomial class <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyval.html>`_.
        See also `NumPy, SciPy polydiv function <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polydiv.html>`_ for more details.
        See also :py:func:`polyval`.
    """
    c = np.polynomial.polynomial.polydiv(c1, c2)
    return polyval(c, L)


def polyder(c, m: int=1, scl: float=1.0, L=None):
    """Constructs the m-th derivative of the polynomial c
    as a lazy linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L is None

    References:
        See `NumPy, SciPy polyder <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyder.html>`_ for more details.
    """
    if L is None:
        raise ValueError("L is None.")
    return polyval(np.polynomial.polynomial.polyder(c, m, scl), L)


def polyint(c, m: int=1, k: list=[], lbnd: float=0.0, scl: float=1.0, L=None):
    """Constructs the m-th integral of the polynomial c
    as a lazy linear operator.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L is None

    References:
        See `NumPy, SciPy polyint <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyint.html>`_ for more details.
    """
    if L is None:
        raise ValueError("L is None.")
    return polyval(np.polynomial.polynomial.polyint(c, m, k, lbnd, scl), L)


def polycompanion(c):
    """Constructs the companion matrix of polynomial
    coefficients c as a lazy linear operator C.

    Args:
        c: 1d array
        List of coefficients [c_0, c_1, ..., c_n]
        If the size of the list is n + 1 then the largest power of the polynomial is n.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            c expects a 1d array.
        ValueError
            # of coefficients must be at least >= 2.
        ValueError
            The first coefficient c[0] must be != 0.

    Examples:

    References:
        See also `NumPy, SciPy polycompanion <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polycompanion.html>`_.
        See also `Companion matrix <https://en.wikipedia.org/wiki/Companion_matrix>`_.
    """

    if c.ndim != 1:
        raise ValueError("c expects a 1d array.")

    if c.shape[0] < 2:
        raise ValueError("# of coefficients must be at least >= 2.")
    if c[0] == 0.0:
        raise ValueError("The first coefficient c[0] must be != 0.")

    def _matmat(c, x, H):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        N = c.shape[0]
        if a.dtype.kind == 'c':
            y = np.empty((N - 1, batch_size), dtype=np.complex_)
        else:
            y = np.empty((N - 1, batch_size), dtype=(a[0] * x[0]).dtype)
        if H:
            # conjugate and transpose
            for b in range(batch_size):
                y[:, b] = np.divide(np.multiply(a[1: ], x[0, b]), -a[0])
                np.add(y[:(N - 2), b], x[1:(N - 1), b], out=y[:(N - 2), b])
        else:
            for b in range(batch_size):
                y[0, b] = np.divide(a[1:], -a[0]) @ x[:, b]
                y[1:(N - 1), b] = x[:(N - 2), b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(a.shape[0] - 1, a.shape[0] - 1),
        matmat=lambda x: _matmat(a, x, False),
        rmatmat=lambda x: _matmat(a, x, True)
    )


def polyvander(x, deg: int):
    r"""Constructs the Vandermonde matrix as a lazy linear operator V.
    The shape of the Vandermonde lazy linear operator is (x.shape[0], deg + 1).

    .. math::
        V = \begin{pmatrix}
        1 & x[0] & x[0]^2 & ... & x[0]^{deg}\\
        1 & x[1] & x[1]^2 & ... & x[1]^{deg}\\
        1 & x[2] & x[2]^2 & ... & x[2]^{deg}\\
        . & .    & .      & ... &   .       \\
        . & .    & .      & ... &   .       \\
        . & .    & .      & ... &   .       \\
        1 & x[n] & x[n]^2 & ... & x[n]^{deg}
        \end{pmatrix}

    Args:
        x: 1d array
        Array of points
        deg: int
        Degree (deg >= 0) of the Vandermonde matrix.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            deg expects an integer value >= 0.

    Examples:

    References:
        See also `NumPy, SciPy polyvander <https://docs.scipy.org/doc//numpy-1.9.3/reference/generated/numpy.polynomial.polynomial.polyvander.html>`_.
        See also `Vandermonde matrix <https://en.wikipedia.org/wiki/Vandermonde_matrix>`_.
    """
    if deg != int(deg) or deg < 0:
        raise ValueError("deg expects an integer value >= 0.")

    if x.ndim == 1:
        x = x.reshape(x.shape[0], 1)

    def _matmat(x, X, H):
        if X.ndim == 1:
            X = X.reshape(X.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = X.shape[1]
            is_1d = False

        y = np.empty(
            (deg + 1 if H else x.shape[0], batch_size),
            dtype=np.complex_ if x.dtype.kind == 'c' or X.dtype.kind == 'c' else (x[0] * X[0, 0]).dtype
        )
        if deg > 0:
            if H:
                # conjugate and transpose
                for b in range(batch_size):
                    for i in range(deg + 1):
                        y[i, b] = np.power(x[:, 0], np.full(x.shape[0], i)) @ X[:, b]
            else:
                for b in range(batch_size):
                    for i in range(x.shape[0]):
                        y[i, b] = np.power(np.full(deg + 1, x[i, 0]), np.arange(0, deg + 1)) @ X[:, b]
        else:
            if H:
                # conjugate and transpose
                for b in range(batch_size):
                    y[0, b] = np.sum(X[:, b])
            else:
                for b in range(batch_size):
                    for i in range(x.shape[0]):
                        y[i, b] = X[0, b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(x.shape[0], deg + 1),
        matmat=lambda X: _matmat(x, X, False),
        rmatmat=lambda X: _matmat(x, X, True)
    )
