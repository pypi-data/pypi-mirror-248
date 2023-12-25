import numpy as np
import pytest
from scipy.sparse import csc_matrix, csr_matrix

from cherab.inversion import _SVDBase, compute_svd


@pytest.mark.parametrize("use_gpu", [False])
def test_compute_svd(test_data, computed_svd, use_gpu):
    hmat = csc_matrix(np.eye(test_data.matrix.shape[1]))
    s, u, v = compute_svd(test_data.matrix, hmat, use_gpu=use_gpu)

    # compute svd by numpy
    u_np, s_np, vh_np = computed_svd

    # check singular values in the range of matrix rank
    rank = np.linalg.matrix_rank(test_data.matrix)
    np.testing.assert_allclose(s[:rank], s_np[:rank], rtol=0, atol=1.0e-10)

    # TODO: check u and v


def test_compute_svd_sparse(test_tomography_data):
    matrix = csr_matrix(test_tomography_data.matrix)
    hmat = csc_matrix(np.eye(matrix.shape[1]))
    s, u, v = compute_svd(matrix, hmat, use_gpu=False)

    # compute svd by numpy
    u_np, s_np, vh_np = np.linalg.svd(test_tomography_data.matrix, full_matrices=False)

    # check singular values in the range of matrix rank - 1
    rank = np.linalg.matrix_rank(test_tomography_data.matrix)
    np.testing.assert_allclose(s[:rank], s_np[: rank - 1], rtol=0, atol=1.0e-10)

    # TODO: check u and v


@pytest.fixture
def svdbase(test_data, computed_svd):
    u, s, vh = computed_svd
    return _SVDBase(s, u, vh.T, data=test_data.b)


@pytest.fixture
def lambdas():
    return np.logspace(-20, 2, num=500)


class TestSVDBase:
    def test__init(self, test_data, computed_svd):
        u, s, vh = computed_svd
        _SVDBase(s, u, vh.T, data=test_data.b)

    def test_w(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.w(beta)

    def test_rho(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.rho(beta)

    def test_eta(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.eta(beta)

    def test_eta_diff(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.eta_diff(beta)

    def test_residual_norm(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.residual_norm(beta)

    def test_regularization_norm(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.regularization_norm(beta)

    def test_inverted_solution(self, svdbase, lambdas):
        for beta in lambdas:
            svdbase.inverted_solution(beta)
