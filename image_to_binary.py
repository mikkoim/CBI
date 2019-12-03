import argparse
import skimage.io
import numpy as np
import os

from skimage import data
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from skimage.transform import resize

from bitstring import BitArray

def read_image(imgpath, size):
    I = skimage.io.imread(imgpath)

    G = rgb2gray(I) # Grayscale
    R = resize(G, (size,size), anti_aliasing=True, mode='constant')

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


#%% Santerin funktiot

def imgToBitArr(m):
    rows = []
    for row in range(len(m)):
        converted = convert(m[row])
        rows.append(converted)
    return (rows)


def convert(list):
    s = [str(i) for i in list]
    res = hex(int("".join(s), 2))
    return (res[2:])


def bitArrToImg(n):
    rowWidth = 0
    image = []

    # binääriksi ja selvitetään levein rivi
    for row in range(len(n)):
        arr = [int(digit) for digit in bin(int(n[row], 16))[2:]]
        image.append(arr)
        rowWidth = max([rowWidth, len(arr)])

    # nollia rivin eteen
    for row in image:
        while len(row) < rowWidth:
            row.insert(0, 0)
    return image

#%%

def main(inpath, outpath, size):
    _, in_ext = os.path.splitext(inpath)

    if in_ext == '.txt':
        hex = readhex(inpath)
        BW = hex2BW(hex)
        skimage.io.imsave(outpath+'.png',BW*255)

    else:
        BW = read_image(inpath, size)
        h = BW2hex(BW)
        savehex(outpath, h)
        skimage.io.imsave(outpath+'.png',BW*255)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Creates binary array from image')
    parser.add_argument('-i', help='Path to input image/text')
    parser.add_argument('-o', help='output filename')
    parser.add_argument('-s', help='Size of one side', default=64, type=int)
    args = parser.parse_args()
    main(args.i, args.o, args.s)