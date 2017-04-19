# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:57:10 2017

@author:Cangye@hotmail.com
"""

from __future__ import print_function, division
from sympy import *
import sympy as sp
from sympy.abc import n,m,a,b
from functools import wraps
from sympy import S, pi, I, Rational, Wild, cacheit, sympify
from sympy.core.function import Function, ArgumentIndexError
from sympy.core.power import Pow
from sympy.core.compatibility import range
from sympy.functions.combinatorial.factorials import factorial
from sympy.functions.elementary.trigonometric import sin, cos, csc, cot
from sympy.functions.elementary.complexes import Abs
from sympy.functions.elementary.miscellaneous import sqrt, root
from sympy.functions.elementary.complexes import re, im
from sympy.functions.special.gamma_functions import gamma
from sympy.functions.special.hyper import hyper
from sympy.polys.orthopolys import spherical_bessel_fn as fn



class BesselBase(Function):
    def __init__(self,*args):
        self.dn=1
    @property
    def order(self):
        """ The order of the bessel-type function. """
        return self.args[0]

    @property
    def argument(self):
        """ The argument of the bessel-type function. """
        return self.args[1]

    @classmethod
    def eval(cls, nu, z):
        return

    def fdiff(self, argindex=2):
        if argindex != 2:
            raise ArgumentIndexError(self, argindex)
        
        #print("============================")
        #print(self.order)
        
        if(self.order-m==0):
            a=(self.__class__(self.order+1, self.argument))
            return a
        elif(self.order-m==1):
            a=(self.__class__(self.order-1, self.argument))
            b=(self.__class__(self.order, self.argument))
            xx=self.argument
            return -((-m**2+xx**2)*a+xx*b)/xx**2
        elif(self.order-m==2):
            a=(self.__class__(self.order+1, self.argument))
            b=(self.__class__(self.order+1, self.argument))
            xx=self.argument
            return (a*(-3*m**2 + xx**2) - b*(xx - m**2*xx + xx**3 - 3*xx))/xx**3 
        
        return (self.__class__(self.order + 1, self.argument))

    def _eval_conjugate(self):
        z = self.argument
        if (z.is_real and z.is_negative) is False:
            return self.__class__(self.order.conjugate(), z.conjugate())

    def _eval_expand_func(self, **hints):
        nu, z, f = self.order, self.argument, self.__class__
        if nu.is_real:
            if (nu - 1).is_positive:
                return (-self._a*self._b*f(nu - 2, z)._eval_expand_func() +
                        2*self._a*(nu - 1)*f(nu - 1, z)._eval_expand_func()/z)
            elif (nu + 1).is_negative:
                return (2*self._b*(nu + 1)*f(nu + 1, z)._eval_expand_func()/z -
                        self._a*self._b*f(nu + 2, z)._eval_expand_func())
        return self

    def _eval_simplify(self, ratio, measure):
        from sympy.simplify.simplify import besselsimp
        return besselsimp(self)


class mybsl(BesselBase):

    _a = S.One
    _b = S.One

    @classmethod
    def eval(cls, nu, z):
        if z.is_zero:
            if nu.is_zero:
                return S.One
            elif (nu.is_integer and nu.is_zero is False) or re(nu).is_positive:
                return S.Zero
            elif re(nu).is_negative and not (nu.is_integer is True):
                return S.ComplexInfinity
            elif nu.is_imaginary:
                return S.NaN


        if z.could_extract_minus_sign():
            return (z)**nu*(-z)**(-nu)*besselj(nu, -z)
        if nu.is_integer:
            if nu.could_extract_minus_sign():
                return S(-1)**(-nu)*besselj(-nu, z)
            newz = z.extract_multiplicatively(I)
            if newz:  # NOTE we don't want to change the function if z==0
                return I**(nu)*besseli(nu, newz)

        # branch handling:
        from sympy import unpolarify, exp
        if nu.is_integer:
            newz = unpolarify(z)
            if newz != z:
                return besselj(nu, newz)
        else:
            newz, n = z.extract_branch_factor()
            if n != 0:
                return exp(2*n*pi*nu*I)*besselj(nu, newz)
        nnu = unpolarify(nu)
        if nu != nnu:
            return besselj(nnu, z)

    def _eval_rewrite_as_besseli(self, nu, z):
        from sympy import polar_lift, exp
        return exp(I*pi*nu/2)*besseli(nu, polar_lift(-I)*z)

    def _eval_rewrite_as_bessely(self, nu, z):
        if nu.is_integer is False:
            return csc(pi*nu)*bessely(-nu, z) - cot(pi*nu)*bessely(nu, z)

    def _eval_rewrite_as_jn(self, nu, z):
        return sqrt(2*z/pi)*jn(nu - S.Half, self.argument)

    def _eval_is_real(self):
        nu, z = self.args
        if nu.is_integer and z.is_real:
            return True

    def _sage_(self):
        import sage.all as sage
        return sage.bessel_J(self.args[0]._sage_(), self.args[1]._sage_())



class MyTensorMethod():
    def __init__(self, syms):
        self.symb=syms
    def grad(self,tens):
        self.coord(self.symb[0],self.symb[1],self.symb[2])
        retens = Matrix(tens.diff(self.symb[0]))
        ct = 1
        for sym in self.symb[1:]:
            retens = retens.row_insert(ct, tens.diff(sym))
            ct += 1
        retens = self.invA*retens
        retens = simplify(transpose(self.rot.inv())*retens)
        #reeye=ss.Matrix().
        return retens.transpose()
    def grad_2d(self,tens):
        self.coord(self.symb[0],self.symb[1],self.symb[2])
        retens = Matrix(tens.diff(self.symb[0]))
        ct = 1
        for sym in self.symb[1:]:
            retens = retens.row_insert(ct, tens.diff(sym))
            ct += 1
        retens = self.invA*retens
        retens = simplify(transpose(self.rot.inv())*retens)
        reeye=sp.zeros(3, 3)
        ssx=tens
        reeye[0,1]=-ssx[0,1]/self.symb[0]
        reeye[1,1]=ssx[0,0]/self.symb[0]
        return retens.transpose()+reeye
    def coord(self,x1,x2,x3):
        self.transmatrix=sp.Matrix([[x1*sp.cos(x2),x1*sp.sin(x2),x3]])
        self.A = sp.Matrix(self.transmatrix.diff(x1))
        self.A = self.A.row_insert(1, self.transmatrix.diff(x2))
        self.A = self.A.row_insert(2, self.transmatrix.diff(x3))
        self.invA = sp.simplify(self.A.inv())
        self.rot=sp.Matrix([[ sp.cos(x2), sp.sin(x2), 0],
                            [-sp.sin(x2), sp.cos(x2), 0],
                            [          0,          0, 1]])
    def curl(self,tens):
        ssx=tens
        ts = Matrix(tens.copy().diff(self.symb[0]))
        ct = 1
        for sym in self.symb[1:]:
            ts = ts.row_insert(ct, tens.copy().diff(sym))
            ts = ts.row_insert(ct, tens.copy().diff(sym))
            ct += 1
        re = Matrix([[-ts[2, 1]+ts[1, 2]/self.symb[0]]])
        re=re.row_insert(1, Matrix([[ts[2,0]-ts[0,2]]]))
        re=re.row_insert(2, Matrix([[-ts[1,0]/self.symb[0]+ts[0,1]+ssx[1]/self.symb[0]]]))
        return re.transpose()
    def div(self,tens):
        ts = Matrix(tens.copy().diff(self.symb[0]))
        ct = 1
        for sym in self.symb[1:]:
            ts = ts.row_insert(ct, tens.copy().diff(sym))
            ct += 1
        return ts[0,0]+ts[1,1]/self.symb[0]+ts[2,2]+tens[0]/self.symb[0]
    def div_2d(self,tens):
        ts = Matrix(tens.diff(self.symb[0]))
        ct = 1
        for sym in self.symb[1:]:
            ts = ts.row_insert(ct, tens.diff(sym))
            ct += 1
        ois=Matrix([[1][1/self.symb[0]][1]])
        tsi=ts*ois

        vectx=ois[0,0]+(tens[0,0]-tens[1,1])/self.symb[0]
        vecty=ois[1,0]+(tens[0,1]+tens[1,0])/self.symb[0]
        vectz=ois[2,0]+(tens[2,0])/self.symb[0]
        return Matrix([[vectx,vecty,vectz]])


        
class Formula():
    def get_vect(self):
        k=symbols("k")
        bl=mybsl(m,self.cod[0]*k)
        Y=exp(I*m*self.cod[1])*bl
        Y=exp(I*m*self.cod[1])*bl
        Y=exp(I*m*self.cod[1])*bl
        
        T=self.ms.curl(Matrix([[0,0,Y.copy()/k]]))
        S=self.ms.grad(Matrix([[Y.copy()]]))/k
        R=Matrix([[0,0,-Y.copy()]])
        vt=Function("vt")(self.cod[2])
        vs=Function("vs")(self.cod[2])
        vr=Function("vr")(self.cod[2])
        self.v=[vt,vs,vr]
        
        vect=T*self.v[0]+S*self.v[1]+R*self.v[2]
        return vect
    def __init__(self):
        x1,x2,x3,k,r=symbols("r,o,z,k,r")
        self.cod=[x1,x2,x3]
        self.syms=self.cod
        self.ms=MyTensorMethod(self.cod)
        

    def get_formlua(self,fom):
        k=symbols("k")
        vect=self.get_vect()

        defi=sp.simplify(fom/exp(I*m*self.cod[1])*k*self.cod[0])
        func=[]
        func.append(simplify(defi[0].diff(mybsl(m,self.cod[0]*k))/I))
        func.append(simplify(defi[1].diff(mybsl(m,self.cod[0]*k))/I))
        func.append(simplify(defi[2].diff(mybsl(m,self.cod[0]*k))/k/self.cod[0]))

        nm=len(vect)
        nm2=len(vect)*2
        mat=sp.zeros(len(vect)*2,len(vect)*2)
        for itry in range(nm):
            for itrx in range(nm):
                mat[itry,itrx]=func[itry].diff(self.v[itrx])
        for itry in range(nm):
            for itrx in range(nm):
                mat[itry,itrx]=mat[itry,itrx]+func[itry].diff(self.v[itrx].diff(self.cod[2]))
        for itry in range(3,nm2-1):
            for itrx in range(3,nm2-1):
                mat[itry,itrx]=mat[itry,itrx]+func[itry-3].diff(self.v[itrx-3].diff(self.cod[2]).diff(self.cod[2]))
        egv=simplify(mat.eigenvects())
        mtE=Matrix(egv[0][2][0].transpose())
        for itr in range(1,nm2-1):
            mtE=mtE.row_insert(itr,egv[itr][2][0].transpose())
        file=open("formula.txt","w")
        file.write(latex(simplify(mat)))
        file.write("\n\n")
        file.write(latex(simplify(mtE)))
        pprint(simplify(mat))
        pprint(simplify(mtE))
    def get_method(self):
        return self.ms
       

omega=symbols("\omega")
test=Formula()
vect=test.get_vect()
ms=test.get_method()
#Define the formula
formula=ms.curl(ms.curl(vect))+vect*omega
test.get_formlua(formula)

