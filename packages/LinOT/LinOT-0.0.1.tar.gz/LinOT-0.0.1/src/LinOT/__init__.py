import numpy as np
import scipy
import scipy.linalg
import scipy.interpolate
from . import auxiliary as aux


def LogW2(pi, pos0, pos1, baseLog=None):
    """Extract approximate logarithmic map from optimal coupling via
    barycentric projection for W2 metric

    Args:
        pi: optimal coupling in sparse.csr_array format
        pos0: postions of the first marginal masses
        pos1: positions of second marginal masses
        baseLog: logarithmic map on base space (optional, assumes R^d if None is supplied)

    Returns:
        v: approximate tangent vector
    """

    if baseLog is None:
        _baseLog = lambda x, y: y - x
    else:
        _baseLog = baseLog

    npts, dim = pos0.shape
    # reserve empty array for vector field
    v = np.zeros((npts, dim), dtype=np.double)

    # go through points in barycenter
    for j in range(npts):
        # check if current row is empty
        if pi.indptr[j + 1] == pi.indptr[j]:
            continue

        # extract masses in that row of the coupling (based on csr format)
        piRow = pi.data[pi.indptr[j]:pi.indptr[j + 1]]
        # normalize masses
        piRow = piRow / np.sum(piRow)
        # extract indices non-zero entries (based on csr format)
        piIndRow = pi.indices[pi.indptr[j]:pi.indptr[j + 1]]

        # need einsum for averaging along first ("zeroth") axis
        v[j, :] = np.einsum(_baseLog(pos0[j], pos1[piIndRow]), [0, 1], piRow, [0], [1])

    return v


def LogHK(pi, mu0, pos0, pos1, kappa=1., baseLog=None):
    """Extract approximate logarithmic map from optimal coupling via
    barycentric projection for HK metric

    Args:
        pi: optimal coupling in sparse.csr_array format
        mu0: masses of first marginal
        pos0: postions of the first marginal masses
        pos1: positions of second marginal masses
        kappa: length scale parameter for HK metric
        baseLog: logarithmic map on base space (optional, assumes R^d if None is supplied)

    Returns:
        v: approximate transport vector
        alpha: approximate mass change vector
        (perpendicular component not implemented at this point)
    """

    if baseLog is None:
        _baseLog = lambda x, y: y - x
    else:
        _baseLog = baseLog

    npts, dim = pos0.shape

    # first marginal and density
    pi0 = np.sum(pi, axis=1)
    u0 = pi0 / mu0

    # mass component
    alpha = 2 * (u0 - 1)

    # reserve empty array for vector field
    v = np.zeros((npts, dim), dtype=np.double)

    # go through points in barycenter
    for j in range(npts):
        # check if current row is empty
        if pi.indptr[j + 1] == pi.indptr[j]:
            continue

        # extract masses in that row of the coupling (based on csr format)
        piRow = pi.data[pi.indptr[j]:pi.indptr[j + 1]]
        # normalize masses
        piRow = piRow / np.sum(piRow)
        # extract indices non-zero entries (based on csr format)
        piIndRow = pi.indices[pi.indptr[j]:pi.indptr[j + 1]]
        log = _baseLog(pos0[j], pos1[piIndRow]).reshape([len(piIndRow),dim])
        logNorm = np.maximum(np.linalg.norm(log, axis=-1)/kappa, 1E-100)
        # need einsum for averaging along first ("zeroth") axis
        v[j, :] = u0[j] * np.einsum( "ik,i->k",\
        #    log, [0, 1], np.tan(logNorm / kappa) / logNorm * piRow, [0], [1])
            log, np.tan(logNorm) / logNorm * piRow)
    return v, alpha


def ExpW2(muRef, posRef, v, baseExp=None):
    """Exponential map for W2 metric.

    Args:
        muRef: masses of base point measure
        posRef: postions of base point measure
        v: vector field
        baseExp: exponential map on base space (optional, assumes R^d if None is supplied)

    Returns:
        muExp: masses of resulting measure
        posExp: positions of resulting measure
    """

    if baseExp is None:
        _baseExp = lambda x, y: x + y
    else:
        _baseExp = baseExp

    muExp = muRef.copy()
    posExp = _baseExp(posRef, v)

    return muExp, posExp


def ExpHK(muRef, posRef, v, alpha, kappa, baseExp=None):
    """Exponential map for HK metric: get target measure (ignoring "teleport contribution").

    Args:
        muRef: masses of base point measure
        posRef: postions of base point measure
        v: transport vector field
        alpha: mass change field
        kappa: HK length scale parameter
        baseExp: exponential map on base space (optional, assumes R^d if None is supplied)

    Returns:
        muExp: masses of resulting measure
        posExp: positions of resulting measure
    """
    if baseExp is None:
        _baseExp = lambda x, y: x + y
    else:
        _baseExp = baseExp

    # norm of all velocity vectors
    vNorm = np.linalg.norm(v, axis=-1)
    # normalized velocity vectors
    vDir = np.einsum(v, [0, 1], 1 / np.maximum(vNorm, 1E-100), [0], [0, 1])

    # fields a and b from exponential map proposition
    # a
    vNormScaled = vNorm / kappa
    # b
    alphaOffset = 0.5 * alpha + 1.

    # q^2 from exponential map prop
    relMField = vNormScaled ** 2 + alphaOffset ** 2
    # angle
    phiField = np.arctan2(vNormScaled, alphaOffset)
    # relative transport map
    TField = np.einsum(vDir, [0, 1], phiField * kappa, [0], [0, 1])

    muExp = muRef * relMField
    posExp = _baseExp(posRef, TField)
    return muExp, posExp


class LinW2Embedding:
    def __init__(self, muRef, posRef, baseExp=None):
        self.muRef = muRef
        self.muSqrt = np.sqrt(self.muRef)
        self.posRef = posRef
        if self.posRef.ndim == 1:
            self.dim = 1
            self.posRef = self.posRef.reshape((-1, 1))
        else:
            self.dim = self.posRef.shape[1]
        self.nPts = self.posRef.shape[0]

        self.samples = np.zeros((0, self.nPts * self.dim))
        self.mean = np.zeros((self.nPts * self.dim,))

        if baseExp is None:
            self.baseExp = lambda x, y: x + y
        else:
            self.baseExp = baseExp

        self.Exp = lambda tan: ExpW2(self.muRef, self.posRef, tan, self.baseExp)

    def standardizeRaw(self, v):
        dim = v.shape[-1]
        return v.reshape(-1, self.nPts, dim), alpha.reshape(-1, self.nPts)

    def addSamples(self, samples):
        samplesEucl = self.convertRawToEuclidean(samples)
        if samplesEucl.ndim == 1:
            # if only a single sample was supplied
            samplesEucl = samplesEucl.reshape((1,) + samplesEucl.shape)
        self.samples = np.concatenate((self.samples, samplesEucl))

    def convertRawToEuclidean(self, samples, shiftMean=True):
        if samples.ndim == 2:
            ## single sample
            result = np.einsum(samples, [0, 1], self.muSqrt, [0], [0, 1]).reshape((-1,))
            if shiftMean:
                result -= self.mean
        elif samples.ndim == 3:
            ## list of samples
            nsmp = samples.shape[0]
            result = np.einsum(samples, [0, 1, 2], self.muSqrt, [1], [0, 1, 2]).reshape((nsmp, -1))
            if shiftMean:
                result -= self.mean.reshape((1, -1))
        else:
            raise ValueError("wrong dimension")
        return result

    def getMeanRaw(self):
        return self.convertEuclideanToRaw(self.mean, shiftMean=False)

    def getMeanExp(self):
        return self.Exp(self.convertEuclideanToRaw(self.mean, shiftMean=False))

    def convertEuclideanToRaw(self, samples, shiftMean=True):
        if samples.ndim == 1:
            ## single sample
            result = samples.copy()
            if shiftMean:
                result += self.mean
            result = np.einsum(result.reshape((self.nPts, self.dim)), [0, 1], \
                               1 / self.muSqrt, [0], [0, 1])
        elif samples.ndim == 2:
            ## multiple samples
            result = samples.copy()
            if shiftMean:
                result += self.mean.reshape((1, -1))
            result = np.einsum(result.reshape((-1, self.nPts, self.dim)), [0, 1, 2], \
                               1 / self.muSqrt, [1], [0, 1, 2])
        else:
            raise ValueError("wrong dimension")
        return result

    def convertPCAToEuclidean(self, samples):
        if samples.ndim == 1:
            ## single sample
            nmodes = min(len(self.pca_vec), len(samples))
            result = np.einsum(self.pca_vec[:nmodes], [0, 1], samples[:nmodes], [0], [1])
        elif samples.ndim == 2:
            ## multiple samples
            nmodes = min(len(self.pca_vec), samples.shape[1])
            result = np.einsum(self.pca_vec[:nmodes], [0, 1], samples[:, :nmodes], [2, 0], [2, 1])
        else:
            raise ValueError("wrong dimension")
        return result

    def convertPCAToRaw(self, samples, shiftMean=True):
        return self.convertEuclideanToRaw(self.convertPCAToEuclidean(samples), shiftMean=shiftMean)

    def centerSamples(self):
        meanShift = np.mean(self.samples, axis=0)
        self.samples -= meanShift
        self.mean += meanShift

    def performPCA(self, keepDim=None):
        self.pca_var, self.pca_vec = aux.PCA(self.samples, keep=keepDim)
        self.pca_std = np.maximum(0, self.pca_var) ** 0.5
        self.pca_coords = np.einsum(self.samples, [0, 1], self.pca_vec, [2, 1], [0, 2])

    def expEuclidean(self, v, tSeq=None):
        if tSeq is None:
            vRaw = self.convertEuclideanToRaw(v)
            res = self.Exp(vRaw)
            return res
        else:
            result = []
            for t in tSeq:
                vRaw = self.convertEuclideanToRaw(t * v)
                res = self.Exp(vRaw)
                result.append(res)
            return result

    def expPCA(self, v, tSeq=None):
        if tSeq is None:
            vRaw = self.convertPCAToRaw(v)
            res = self.Exp(vRaw)
            return res
        else:
            result = []
            for t in tSeq:
                vRaw = self.convertPCAToRaw(t * v)
                res = self.Exp(vRaw)
                result.append(res)
            return result


class LinW2GaussEmbedding(LinW2Embedding):
    def __init__(self, covRef, meanRef):
        self.covRef = covRef
        self.meanRef = meanRef

        self.covRefSqrt = scipy.linalg.sqrtm(self.covRef)
        self.covRefSqrtInv = scipy.linalg.inv(self.covRefSqrt)

        self.dim = self.meanRef.shape[0]
        self.dimEucl = self.dim * self.dim + self.dim

        self.samples = np.zeros((0, self.dimEucl))
        self.mean = np.zeros((self.dimEucl,))
        self.Exp = lambda x: x

    def convertRawToEuclidean(self, samples, shiftMean=True):
        """covs is a single or a list of covariance matrices
        means is a single or a list of mean vectors"""
        covs, means = samples
        if covs.ndim == 2:
            ## single sample
            result = np.zeros((self.dimEucl,), dtype=np.double)
            mat = scipy.linalg.sqrtm( \
                self.covRefSqrt.dot(covs.dot(self.covRefSqrt))).dot( \
                self.covRefSqrtInv) - self.covRefSqrt
            result[:self.dim * self.dim] = mat.ravel()
            result[self.dim * self.dim:] = means
            if shiftMean:
                result -= self.mean
        elif covs.ndim == 3:
            ## list of samples
            nsmp = covs.shape[0]
            result = np.zeros((nsmp, self.dimEucl), dtype=np.double)
            for i, (cov, mean) in enumerate(zip(covs, means)):
                mat = scipy.linalg.sqrtm( \
                    self.covRefSqrt.dot(cov.dot(self.covRefSqrt))).dot( \
                    self.covRefSqrtInv) - self.covRefSqrt
                result[i, :self.dim * self.dim] = mat.ravel()
                result[i, self.dim * self.dim:] = mean

            if shiftMean:
                result -= self.mean.reshape((1, -1))
        else:
            raise ValueError("wrong dimension")
        return result

    def convertEuclideanToRaw(self, samples, shiftMean=True):
        if samples.ndim == 1:
            ## single sample
            vec = samples.copy()
            if shiftMean:
                vec += self.mean
            mat = vec[:self.dim * self.dim].reshape((self.dim, self.dim))
            cov = self.covRefSqrtInv.dot((mat + self.covRefSqrt).dot( \
                self.covRefSqrt.dot(mat + self.covRefSqrt)))
            mean = vec[self.dim * self.dim:]
            return cov, mean
        elif samples.ndim == 2:
            ## multiple samples
            nsmp = samples.shape[0]
            rescov = np.zeros((nsmp, self.dim, self.dim), dtype=np.double)
            resmean = np.zeros((nsmp, self.dim), dtype=np.double)
            for i, sample in enumerate(samples):
                vec = sample.copy()
                if shiftMean:
                    vec += self.mean
                mat = vec[:self.dim * self.dim].reshape((self.dim, self.dim))
                rescov[i] = self.covRefSqrtInv.dot((mat + self.covRefSqrt).dot( \
                    self.covRefSqrt.dot(mat + self.covRefSqrt)))
                resmean[i] = vec[self.dim * self.dim:]
            return rescov, resmean


        else:
            raise ValueError("wrong dimension")


class LinHKEmbedding(LinW2Embedding):
    def __init__(self, muRef, posRef, kappa, baseExp=None):
        LinW2Embedding.__init__(self, muRef, posRef, baseExp=baseExp)
        self.samples = np.zeros((0, self.nPts * (self.dim + 1)))
        self.mean = np.zeros((self.nPts * (self.dim + 1),))
        self.kappa = kappa
        self.Exp = lambda tan: ExpHK(self.muRef, self.posRef, \
                                     tan[0], tan[1], self.kappa, self.baseExp)

    def standardizeRaw(self, v, alpha):
        dim = v.shape[-1]
        return v.reshape(-1, self.nPts, dim), alpha.reshape(-1, self.nPts)

    def convertRawToEuclidean(self, samples, shiftMean=True):
        vs, alphas = samples
        if vs.ndim == 2:
            ## single sample
            samp = np.concatenate((vs, 0.5 * self.kappa * alphas.reshape((-1, 1))), axis=1)
            result = np.einsum(samp, [0, 1], self.muSqrt, [0], [0, 1]).reshape((-1,))
            if shiftMean:
                result -= self.mean
        elif vs.ndim == 3:
            ## list of samples
            nsmp = vs.shape[0]
            samp = np.concatenate((vs, 0.5 * self.kappa * alphas.reshape((nsmp, -1, 1))), axis=2)
            result = np.einsum(samp, [0, 1, 2], self.muSqrt, [1], [0, 1, 2]).reshape((nsmp, -1))
            if shiftMean:
                result -= self.mean.reshape((1, -1))
        else:
            raise ValueError("wrong dimension")
        return result

    def convertEuclideanToRaw(self, samples, shiftMean=True):
        if samples.ndim == 1:
            ## single sample
            result = samples.copy()
            if shiftMean:
                result += self.mean
            result = np.einsum(result.reshape((self.nPts, self.dim + 1)), [0, 1], \
                               1 / self.muSqrt, [0], [0, 1])
            v = result[:, :self.dim]
            alpha = result[:, -1] * 2 / self.kappa
        elif samples.ndim == 2:
            ## multiple samples
            result = samples.copy()
            if shiftMean:
                result += self.mean.reshape((1, -1))
            result = np.einsum(result.reshape((-1, self.nPts, self.dim + 1)), [0, 1, 2], \
                               1 / self.muSqrt, [1], [0, 1, 2])
            v = result[:, :, :self.dim]
            alpha = result[:, :, -1] * 2 / self.kappa
        else:
            raise ValueError("wrong dimension")
        return v, alpha


class LinSHKEmbedding(LinHKEmbedding):
    def __init__(self, muRef, posRef, kappa, baseExp=None):
        LinHKEmbedding.__init__(self, muRef, posRef, kappa, baseExp=baseExp)
        self.massRef = np.sum(self.muRef)
        self.Exp = lambda tan: ExpHK(self.muRef, self.posRef, \
                                     *(self.tanSHKToHK(*tan)), self.kappa, self.baseExp)

    def normalizeTan(self, v, alpha):
        """
        Normalize HK tangent vectors so that the exponential yields a probability measure.
        The mass of the initial exponential target is given by the L2 norm of the "compound
        vector (v/kappa, 1+alpha/2) by definition of the exp.

        Args:
            v: transport vector field
            alpha: mass change field

        Returns:
            vNorm, alphaNorm: Logarithmic components associated with the normalized measure
                                muExp/mass(muExp)
        """

        vNorm, alphaNorm = self.standardizeRaw(v, alpha)
        vNorm=vNorm.copy()
        alphaNorm=alphaNorm.copy()
        massesExp = np.einsum('ijk,j->i', (vNorm / self.kappa) ** 2, self.muRef) \
                    + np.einsum('ij,j->i', (1 + alphaNorm / 2) ** 2, self.muRef)
        massesExp /= self.massRef
        massesExp = np.sqrt(massesExp)
        vNorm /= massesExp.reshape(-1, 1, 1)
        alphaNorm = 2 * ((1 + alphaNorm / 2) / massesExp.reshape(-1, 1) - 1)
        return vNorm, alphaNorm

    def tanHKToSHK(self, v, alpha):
        """
        Normalizes and re-centers HK tangent vectors in order to obtain SHK tangent vectors
        yielding the same exponential measure.

        Args:
            v: transport vector field for HK metric
            alpha: mass change field for HK metric

        Returns:
            v, alpha: SHK tangent vectors with target muExp/mass(muExp)
        """
        vHK, alphaHK = self.standardizeRaw(v, alpha)
        hK2Scaled = -np.einsum('ij,j->i', alphaHK, self.muRef).reshape(-1, 1)
        sHKScaled = np.arccos(1 - hK2Scaled / 2)
        sHKScaled = np.maximum(sHKScaled, 1e-100)
        s = sHKScaled / np.sin(sHKScaled)
        return np.squeeze(vHK * s.reshape(-1, 1, 1)), np.squeeze((alphaHK + hK2Scaled) * s)

    def tanSHKToHK(self, v, alpha):
        """
        Shifts SHK tangent vectors to obtain HK tangent vectors with the same target measure
        through the exponential map.

        Args:
            v: transport vector field for SHK metric
            alpha: mass change field for SHK metric

        Returns:
            v, alpha: HK tangent vectors with the same target muExp
        """

        vSHK, alphaSHK = self.standardizeRaw(v, alpha)
        sHKScaled = np.sqrt(np.einsum('ijk,j->i', (vSHK / self.kappa) ** 2, self.muRef) \
                            + 0.25 * np.einsum('ij,j->i', alphaSHK ** 2, self.muRef))
        sHKScaled = np.maximum(sHKScaled, 1e-100).reshape(-1, 1)
        s = sHKScaled / np.sin(sHKScaled)
        hk2Scaled = 2 * (1 - np.cos(sHKScaled))
        return np.squeeze(vSHK / s.reshape(-1, 1, 1)), np.squeeze(alphaSHK / s - hk2Scaled)

    def addSamples(self, samples, fromHK=False):
        if fromHK:
            tmp = self.normalizeTan(*samples)
            tmp = self.tanHKToSHK(*tmp)
            LinHKEmbedding.addSamples(self, tmp)
        else:
            LinHKEmbedding.addSamples(self, samples)


class LinW2_1dEmbedding(LinW2Embedding):
    def __init__(self, nPts, interpolationMode="next"):
        self.nPts = nPts
        self.pos = np.linspace(0, 1, num=self.nPts, endpoint=False)
        self.samples = np.zeros((0, self.nPts))
        self.mean = np.zeros((self.nPts,))
        self.Exp = lambda x: x
        self.interpolationMode = interpolationMode

    def convertRawToEuclideanSingle(self, pos, mass, shiftMean=True):
        massCum = np.cumsum(mass)
        massCumHat = np.concatenate((np.array([0.]), massCum))
        posHat = np.concatenate((pos[[0]], pos))
        f = scipy.interpolate.interp1d(massCumHat, posHat, kind=self.interpolationMode, assume_sorted=True)
        return f(self.pos)

    def convertRawToEuclidean(self, samples, shiftMean=True):
        pos, mass = samples
        if pos.ndim == 1:
            ## single sample
            result = self.convertRawToEuclideanSingle(pos, mass, shiftMean=shiftMean)
            if shiftMean:
                result -= self.mean
        elif pos.ndim == 2:
            ## list of samples
            nsmp = pos.shape[0]
            result = np.zeros((nsmp, self.nPts), dtype=np.double)
            for i in range(nsmp):
                result[i] = self.convertRawToEuclideanSingle(pos[i], mass[i], shiftMean=shiftMean)
            if shiftMean:
                result -= self.mean.reshape((1, -1))
        else:
            raise ValueError("wrong dimension")
        return result

    def convertEuclideanToRaw(self, samples, shiftMean=True):
        if samples.ndim == 1:
            ## single sample
            pos = samples.copy()
            if shiftMean:
                pos += self.mean
            return pos, np.full((self.nPts,), fill_value=1. / self.nPts)
        elif samples.ndim == 2:
            ## multiple samples
            nsmp = samples.shape[0]
            pos = samples.copy()
            if shiftMean:
                pos += self.mean
            mass = np.full((nsmp, self.nPts), fill_value=1. / self.nPts)
            return pos, mass
        else:
            raise ValueError("wrong dimension")
            
    def addSamples(self,samples):
        if type(samples) == list or type(samples) == zip:
            new_samples=[]
            for x in samples:
                samplesEucl=self.convertRawToEuclidean(x)
                if samplesEucl.ndim==1:
                    # if only a single sample was supplied
                    samplesEucl=samplesEucl.reshape((1,)+samplesEucl.shape)
                new_samples.append(samplesEucl)
            new_samples = np.concatenate(new_samples)
            self.samples = np.concatenate((self.samples, new_samples))
        elif type(samples) == np.ndarray or type(samples) == tuple:
            samplesEucl=self.convertRawToEuclidean(samples)
            if samplesEucl.ndim == 1:
                # if only a single sample was supplied
                samplesEucl = samplesEucl.reshape((1,) + samplesEucl.shape)
            self.samples = np.concatenate((self.samples, samplesEucl))
        else:
            raise ValueError("wrong type")
