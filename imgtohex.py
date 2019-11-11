

import binascii
import argparse

def imgToHex(filename):
    with open(filename, 'rb') as f:
        content = f.read()
    return content

def hexToImg(content, fname):
    with open(fname, 'wb') as f:
        f.write(content)

def main(upload_path):
    st = imgToHex(upload_path)
    print(st)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ChirpSDK Example',
        epilog='Sends a random chirp payload, then continuously listens for chirps'
    )
    parser.add_argument('-i', help='Path to image')
    args = parser.parse_args()
    main(args.i)