import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def ShowImageArray(imgList,nCols,figWidth,figHeight,rowTitles=None,colTitles=None,\
        scaleMode="single",vmax=None,vmin=None,show=True):
    nImgs=len(imgList)
    if scaleMode=="single":
        _vmax=None
        _vmin=None
    elif scaleMode=="common":
        _vmax=np.max(imgList)
        _vmin=np.min(imgList)
    elif scaleMode=="explicit":
        _vmax=vmax
        _vmin=vmin
    nRows=((nImgs-1)//nCols)+1
    if rowTitles is None:
        rowTitles=[""]*nRows
    if colTitles is None:
        colTitles=[""]*nCols
        
    fig=plt.figure(figsize=(nCols*figWidth,nCols*figHeight))
    for i,img in enumerate(imgList):
        fig.add_subplot(nRows,nCols,i+1)
        if i<nCols:
            plt.title(colTitles[i])
        if i%nCols==0:
            plt.ylabel(rowTitles[i//nCols])
        plt.imshow(img,vmax=_vmax,vmin=_vmin)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    if show is None:
        return fig
    if show:
        plt.show()
    else:
        plt.close()
        return fig

def addEllipse(ax,xy,width,height,angle=0,**kwargs):
    e=matplotlib.patches.Ellipse(xy, width, height, angle, **kwargs)
    ax.add_artist(e)

def addEllipseMat(ax,xy,mat,**kwargs):
    eigval,eigvec=np.linalg.eigh(mat)
    phi=np.arctan2(eigvec[0,1],eigvec[0,0])/np.pi*180
    e=matplotlib.patches.Ellipse(xy, 2*eigval[0]**0.5, 2*eigval[1]**0.5, angle=phi, **kwargs)
    ax.add_artist(e)

def PCASpectrum(Embedding,nMax=None,normalize=False,ax=None,marker="+",**kwargs):
    if ax is None:
        clbl=plt.gca()
    else:
        clbl=ax
    if nMax is None:
        _nMax=Embedding.pca_var.shape[0]
    else:
        _nMax=nMax
    x=np.arange(_nMax)
    if normalize:
        y=Embedding.pca_var[:_nMax]/Embedding.pca_var[0]
    else:
        y=Embedding.pca_var[:_nMax]
    clbl.scatter(x,y,marker=marker,**kwargs)
    clbl.set_yscale("log")
    
def PCAPlot(Embedding,modes=[0,1],ax=None,marker="x",labels=None,**kwargs):
    if ax is None:
        clbl=plt.gca()
    else:
        clbl=ax
    clbl.scatter(Embedding.pca_coords[:,modes[0]],Embedding.pca_coords[:,modes[1]],marker=marker,**kwargs)
    if labels is not None:
        addLabels(Embedding.pca_coords[:,modes[0]],Embedding.pca_coords[:,modes[1]],labels,ax=clbl)

def addLabels(posX,posY,labels,ax=None):
    for label, coord1, coord2 in zip(labels,posX,posY):
        ax.annotate(label,(coord1,coord2)) 


def cumplot(pos,mass,ax=None,**kwargs):
    _kwargs={"where":"pre"}
    _kwargs={**_kwargs,**kwargs}
        
    if ax is None:
        plt.step(pos,np.cumsum(mass),**kwargs)
    else:
        ax.step(pos,np.cumsum(mass),**kwargs)
    

def histseqplot(Embedding,euclVec,ax=None,mean=True,range=[-1,1],num=7,cm=cm.viridis,**kwargs):
    _kwargs={"histtype":"step"}
    _kwargs={**_kwargs,**kwargs}
    if mean:
        offset=Embedding.mean
    else:
        offset=np.zeros_like(Embedding.mean)
    if ax is None:
        clbl=plt
    else:
        clbl=ax
    for j,t in enumerate(np.linspace(range[0],range[1],num=num)):
            clbl.hist(offset+t*euclVec,color=cm(j/(num-1)),**_kwargs)

