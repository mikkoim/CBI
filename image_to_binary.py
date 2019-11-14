import argparse
import skimage.io
import numpy as np

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

def savehex(outname, s):
    with open(outname + '.txt', 'w') as f:
        f.write(s)

def main(imgpath, outpath):
    BW = read_image(imgpath)
    h = BW2hex(BW)
    savehex(outpath, h)
    skimage.io.imsave(outpath+'.png',BW*255)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates binary array from image')
    parser.add_argument('-i', help='Path to image')
    parser.add_argument('-o', help='output filename')
    args = parser.parse_args()
    main(args.i, args.o)