# -*- coding: utf-8 -*-

import pyfr.backends.base as base

import numpy as np

class _Dummy2DBase(object):
    def __init__(self, nrow, ncol, initval=None, tags=set()):
        self._nrow = nrow
        self._ncol = ncol
        self._tags = tags

    def get(self):
        return None

    @property
    def nrow(self):
        return self._nrow

    @property
    def ncol(self):
        return self._ncol


class _DummyMatrix(_Dummy2DBase, base.Matrix):
    def set(self, arr):
        assert arr.shape == (self._nrow, self._ncol)


class _DummyConstMatrix(_Dummy2DBase, base.ConstMatrix):
    pass


class _DummySparseMatrix(_Dummy2DBase, base.SparseMatrix):
    pass


class _DummyMPIMatrix(_DummyMatrix, base.MPIMatrix):
    pass


class _DummyMatrixBank(base.MatrixBank):
    def __init__(self, nrow, ncol, nbanks, initval=None, tags=set()):
        mats = [_DummyMatrix(nrow, ncol, initval, tags) for i in xrange(nbanks)]
        super(_DummyMatrixBank, self).__init__(mats)


class _DummyView(_Dummy2DBase, base.View):
    pass


class _DummyMPIView(_DummyView, base.MPIView):
    pass


class _DummyKernel(base.Kernel):
    pass


class _DummyQueue(base.Queue):
    def __lshift__(self, iterable):
        pass

    def __mod__(self, iterable):
        pass

class DummyBackend(base.Backend):
    def matrix(self, *args, **kwargs):
        return _DummyMatrix(*args, **kwargs)

    def matrix_bank(self, *args, **kwargs):
        return _DummyMatrixBank(*args, **kwargs)

    def mpi_matrix(self, *args, **kwargs):
        return _DummyMPIMatrix(*args, **kwargs)

    def const_matrix(self, *args, **kwargs):
        return _DummyConstMatrix(*args, **kwargs)

    def sparse_matrix(self, *args, **kwargs):
        return _DummySparseMatrix(*args, **kwargs)

    def _is_sparse(self, mat, tags):
        if 'sparse' in tags:
            return True
        elif np.count_nonzero(mat) < 0.33*mat.size:
            return True
        else:
            return False

    def view(self, *args, **kwargs):
        return _DummyView(*args, **kwargs)

    def mpi_view(self, *args, **kwargs):
        return _DummyMPIView(*args, **kwargs)

    def kernel(self, name, *args, **kwargs):
        validateattr = '_validate_' + name

        # Check the kernel name
        if not hasattr(self, validateattr):
            raise PyFRInvalidKernelError("'{}' is not a valid kernel"\
                                         .format(name))

        # Call the validator method to check the arguments
        getattr(self, validateattr)(*args, **kwargs)

        return _DummyKernel()

    def queue(self, *args, **kwargs):
        return _DummyQueue(*args, **kwargs)

    def runall(self, seq):
        for q in seq:
            assert isinstance(q, _DummyQueue)

    def _validate_mul(self, a, b, out):
        assert a.nrow == out.nrow
        assert a.ncol == b.nrow
        assert b.ncol == out.ncol
        assert isinstance(out, (_DummyMatrix, _DummyMatrixBank))

    def _validate_ipadd(self, y, alpha, x):
        assert isinstance(out, (_DummyMatrix, _DummyMatrixBank))