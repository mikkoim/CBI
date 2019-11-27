import argparse
import skimage.io
import numpy as np
import os

from skimage import data
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from skimage.transform import resize

from bitstring import BitArray

def read_image(imgpath):
    I = skimage.io.imread(imgpath)

    G = rgb2gray(I) # Grayscale
    R = resize(G, (64,64), anti_aliasing=True, mode='constant')

    # Binarize image
    thresh = threshold_otsu(R)
    L = R > thresh
    BW = L*1 

    return BW

def BW2hex(BW):
    Bvec = BW.ravel()
    Bchars = list(map(lambda x: str(x), Bvec))  
    bs = ''.join(Bchars)
    b = BitArray(bin=bs)
    return b.hex

def hex2BW(st):
    b = BitArray(hex=st)
    bs = b.bin
    ba = np.array(list(map(lambda x: int(x), bs)))

    BW = np.resize(ba, (64,64))
    return BW

def savehex(outname, s):
    with open(outname + '.txt', 'w') as f:
        f.write(s)

def readhex(inpath):
    with open(inpath, 'r') as f:
        st = f.read()
    return st

def main(inpath, outpath):
    _, in_ext = os.path.splitext(inpath)

    if in_ext == '.txt':
        hex = readhex(inpath)
        BW = hex2BW(hex)
        skimage.io.imsave(outpath+'.png',BW*255)

    else:
        BW = read_image(inpath)
        h = BW2hex(BW)
        savehex(outpath, h)
        skimage.io.imsave(outpath+'.png',BW*255)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates binary array from image')
    parser.add_argument('-i', help='Path to input image/text')
    parser.add_argument('-o', help='output filename')
    args = parser.parse_args()
    main(args.i, args.o)