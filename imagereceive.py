# ------------------------------------------------------------------------
#
#  This file is part of the Chirp Python SDK.
#  For full information on usage and licensing, see https://chirp.io/
#
#  Copyright (c) 2011-2019, Asio Ltd.
#  All rights reserved.
#
# ------------------------------------------------------------------------

import argparse
import sys
import time
import codecs
import datetime

from imgtohex import hexToImg

from chirpsdk import ChirpSDK, CallbackSet, CHIRP_SDK_STATE

STARTMSG = codecs.encode(b'IMGBEG','hex-codec')
ENDMSG = codecs.encode(b'IMGEND','hex-codec')

class Callbacks(CallbackSet):

    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        print('State changed from {} to {}'.format(
            CHIRP_SDK_STATE.get(previous_state),
            CHIRP_SDK_STATE.get(current_state)))

    def on_sending(self, payload, channel):
        pass

    def on_sent(self, payload, channel):
        pass

    def on_receiving(self, channel):
        """ Called when a chirp frontdoor is detected """
        print('Receiving data [ch{ch}]'.format(ch=channel))

    def on_received(self, payload, channel):
        """
        Called when an entire chirp has been received.
        Note: A length of 0 indicates a failed decode.
        """
        #print("payload:")
        #print(list(payload))
        #print("startmsg:")
        #print(list(STARTMSG))
        #print("endmsg:")
        #print(list(ENDMSG))

        global REC_IMG
        global IMG_PARTS

        if payload is None:
            print('Decode failed!')
        elif list(payload) == list(STARTMSG):
            REC_IMG = True
            print("Image detected")
        elif list(payload) == list(ENDMSG):
            REC_IMG = False
            print("Image received")
            binary = parts_to_imgbin(IMG_PARTS)
            saveimg(binary)
        else:
            print('Received package: {data} [ch{ch}]'.format(
                data=list(payload), ch=channel))
            if REC_IMG:
                print('Appending to image parts...')
                IMG_PARTS.append(payload)
            
def parts_to_imgbin(parts):
    return b''.join(parts)

def timestring():
    return datetime.datetime.now().strftime('%Y%m%d-%H-%M-%S')

def saveimg(binary):
    fname = timestring()
    hexToImg(binary, fname+'.png')

def main(block_name, input_device, output_device,
         block_size, sample_rate):

    # Initialise ChirpSDK
    sdk = ChirpSDK(block=block_name)
    print(str(sdk))
    print('Protocol: {protocol} [v{version}]'.format(
        protocol=sdk.protocol_name,
        version=sdk.protocol_version))
    print(sdk.audio.query_devices())

    # Configure audio
    sdk.audio.input_device = input_device
    sdk.audio.output_device = output_device
    sdk.audio.block_size = block_size
    sdk.input_sample_rate = sample_rate
    sdk.output_sample_rate = sample_rate

    # GLOBALS
    global IMG_PARTS
    global REC_IMG

    IMG_PARTS = []
    REC_IMG = False

    # Set callback functions
    sdk.set_callbacks(Callbacks())

    sdk.start(send=False, receive=True)

    try:
        # Process audio streams
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Exiting')

    sdk.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ChirpSDK Example',
        epilog='Sends a random chirp payload, then continuously listens for chirps'
    )
    parser.add_argument('-c', help='The configuration block [name] in your ~/.chirprc file (optional)')
    parser.add_argument('-i', type=int, default=None, help='Input device index (optional)')
    parser.add_argument('-o', type=int, default=None, help='Output device index (optional)')
    parser.add_argument('-b', type=int, default=0, help='Block size (optional)')
    parser.add_argument('-s', type=int, default=44100, help='Sample rate (optional)')
    args = parser.parse_args()

    main(args.c, args.i, args.o, args.b, args.s)
