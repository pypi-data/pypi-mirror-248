import numpy as np
import scipy.io as sciio


def PCA(dataMat, keep=None):
    nSamples, dim = dataMat.shape
    if dim < nSamples:
        if keep is None:
            keep = dim
        A = dataMat.transpose().dot(dataMat) / nSamples
        eigData = np.linalg.eigh(A)
        eigval = (eigData[0][-keep::])[::-1]
        eigvec = ((eigData[1][:, -keep::]).transpose())[::-1]
    else:
        if keep is None:
            keep = nSamples
        A = dataMat.dot(dataMat.transpose()) / nSamples
        eigData = np.linalg.eigh(A)
        eigval = (eigData[0][-keep::])[::-1]
        eigvec = ((eigData[1][:, -keep::]).transpose())[::-1]

        eigvec = np.einsum(eigvec, [0, 1], dataMat, [1, 2], [0, 2])
        # renormalize
        normList = np.maximum(np.linalg.norm(eigvec, axis=1), 1E-100)
        eigvec = np.einsum(eigvec, [0, 1], 1 / normList, [0], [0, 1])
    return eigval, eigvec


def rasterizePointCloud2dInt(mu, pos, shapeImg):
    """Similar as rasterizePointCloud but pos is assumed to be int valued. So write values of mu precisely into the right entries of the image."""
    img = np.zeros(shapeImg, dtype=np.double, order="C")

    # this accounts for multiplicities of indices correctly
    np.add.at(img, (np.clip(pos[:, 0], 0, shapeImg[0] - 1), np.clip(pos[:, 1], 0, shapeImg[1] - 1)), mu)
    return img


def rasterizePointCloud2d(mu, pos, shapeImg, extent=None):
    """Project point cloud with positions pos and weights mu to Cartesian grid of
    shape shapeImg. Use bi-linear interpolation for non-integer locations.
    extent=(x1,y1,x2,y2) specifies the boundaries of the box which is to be mapped
    to the image pixels
    """
    img = np.zeros(shapeImg, dtype=np.double, order="C")

    if extent is None:
        _extent = (0, shapeImg[0] - 1, 0, shapeImg[1] - 1)
    else:
        _extent = extent

    _pos = pos.copy()
    _pos[:, 0] = (_pos[:, 0] - _extent[0]) / (_extent[1] - _extent[0]) * (shapeImg[0] - 1)
    _pos[:, 1] = (_pos[:, 1] - _extent[2]) / (_extent[3] - _extent[2]) * (shapeImg[1] - 1)

    # now obtain weights for each corner
    posRel = _pos - _pos.astype(int)
    posInt = _pos.astype(int)

    # top left
    weight = (1 - posRel[:, 0]) * (1 - posRel[:, 1])
    posCorner = posInt
    img += rasterizePointCloud2dInt(mu * weight, posCorner, shapeImg)

    # bottom left
    weight = (posRel[:, 0]) * (1 - posRel[:, 1])
    posCorner = posInt + np.array([1, 0], dtype=int)
    img += rasterizePointCloud2dInt(mu * weight, posCorner, shapeImg)

    # top right
    weight = (1 - posRel[:, 0]) * (posRel[:, 1])
    posCorner = posInt + np.array([0, 1], dtype=int)
    img += rasterizePointCloud2dInt(mu * weight, posCorner, shapeImg)

    # bottom right
    weight = (posRel[:, 0]) * (posRel[:, 1])
    posCorner = posInt + np.array([1, 1], dtype=int)
    img += rasterizePointCloud2dInt(mu * weight, posCorner, shapeImg)

    return img


def importMeasure(fn, totalMass=None, keepZero=False):
    dat = np.array(sciio.loadmat(fn)["a"], dtype=np.double, order="C")
    mu, pos = processDensity_Grid(dat, totalMass=totalMass, keepZero=keepZero)
    return (dat, mu, pos, dat.shape)


def getPoslistNCube(shape, dtype=np.double):
    """Create list of positions in an n-dimensional cube of size shape."""
    ndim = len(shape)

    axGrids = [np.arange(i, dtype=dtype) for i in shape]
    prePos = np.array(np.meshgrid(*axGrids, indexing='ij'), dtype=dtype)
    # the first dimension of prepos is the dimension of the  posvector, the successive dimensions are in the cube
    # so need to move first axis to end, and then flatten
    pos = np.rollaxis(prePos, 0, ndim + 1)
    # flattening
    newshape = (-1, ndim)
    return (pos.reshape(newshape)).copy()


def processDensity_Grid(x, totalMass=None, constOffset=None, keepZero=True, zeroThresh=1E-14):
    # process actual density

    # copy, cast to double and reshape
    img = np.array(x, dtype=np.double, order="C").copy()
    shape = img.shape
    nPoints = np.prod(shape)
    dim = len(shape)
    img = img.reshape((nPoints))

    processDensity(img, totalMass=totalMass, constOffset=constOffset)

    # get grid pos information
    posList = getPoslistNCube(shape, dtype=int)
    posList = posList.reshape((nPoints, dim))

    # if desired, throw away points with zero mass
    if not keepZero:
        nonZeroPos = np.nonzero(img > zeroThresh)
        img = img[nonZeroPos]
        posList = posList[nonZeroPos]

        # if necessary, rescale mass once more
        processDensity(img, totalMass=totalMass, constOffset=None)

    return (img, posList)


def processDensity(x, totalMass=None, constOffset=None):
    # re-normalize and add offset if required
    if totalMass is not None:
        x[:] = totalMass * x / np.sum(x)
        if constOffset is not None:
            x[:] = x + constOffset
            x[:] = totalMass * x / np.sum(x)
    else:
        if constOffset is not None:
            x[:] = x + constOffset
            # x[:]=x/np.sum(x)


def kernelFlat(x,grid,sigma):
    dim=x.shape[-1]
    dists=np.linalg.norm(x.reshape((-1,1,dim))-grid.reshape(1,-1,dim),axis=-1)
    dists/=np.max(dists)
    return np.exp(-dists**2/(2*sigma**2))

def kernelSphere(x,grid,sigma,rad):
        return np.exp(np.maximum(np.einsum('ik,jk->ij',x/rad,grid/rad)/sigma,230.,dtype=np.float128))
        

def kde(posMu,mu,grid,sigma, kernel=kernelFlat):
    dens=np.einsum('ij,i->j',kernel(posMu,grid,sigma),mu)
    massDens=np.maximum(np.sum(dens),1e-100)
    massMu=np.sum(mu)
    return massMu*dens/massDens
