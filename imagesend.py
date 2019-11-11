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

from imgtohex import imgToHex


from chirpsdk import ChirpSDK, CallbackSet, CHIRP_SDK_STATE


class Callbacks(CallbackSet):

    def on_state_changed(self, previous_state, current_state):
        """ Called when the SDK's state has changed """
        print('State changed from {} to {}'.format(
            CHIRP_SDK_STATE.get(previous_state),
            CHIRP_SDK_STATE.get(current_state)))

    def on_sending(self, payload, channel):
        """ Called when a chirp has started to be transmitted """
        print('Sending: {data} [ch{ch}]'.format(
            data=list(payload), ch=channel))

    def on_sent(self, payload, channel):
        """ Called when the entire chirp has been sent """
        print('Sent: {data} [ch{ch}]'.format(
            data=list(payload), ch=channel))

    def on_receiving(self, channel):
        pass

    def on_received(self, payload, channel):
        pass

def split_payload(payload):
    if len(payload) < 32:
        return payload
    else:
        n = 32
        parts = [payload[i:i+n] for i in range(0, len(payload), n)]

    return parts

def main(block_name, input_device, output_device,
         block_size, sample_rate, filename):

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

    # Set callback functions
    sdk.set_callbacks(Callbacks())

    # Generate random payload and send
    payload = imgToHex(filename)
    parts = split_payload(payload)

    # Send payload
    sdk.start(send=True, receive=False)

    startmessage = codecs.encode(b'IMGBEG','hex-codec')
    endmessage = codecs.encode(b'IMGEND','hex-codec')
    
    print("\n\n#############")
    print("Total parts: {p}, ~{s} seconds".format(
        p=len(parts),
        s=len(parts)*5))
    print("#############\n\n")

    sdk.send([1],blocking=True)
    sdk.send(startmessage, blocking=True)
    print(list(startmessage))
    time.sleep(0.5)
    for part in parts:
        sdk.send(part, blocking=True)
        time.sleep(0.1)
    sdk.send(endmessage, blocking=True)

    time.sleep(1)
    print("Stopping...")

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
    parser.add_argument('-p', type=str, help='Payload')
    args = parser.parse_args()

    main(args.c, args.i, args.o, args.b, args.s, args.p)
