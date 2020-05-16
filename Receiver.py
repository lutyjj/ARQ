import random
import numpy as np
from PIL import Image
import crcmod
import hashlib
from TransmissionChannel import TransmissionChannel


class Receiver:
    control_method = 0
    intensity = 0.5
    broken_frames = []
    result = []
    result2 = []
    frame = []
    shape = None
    numberOfRejectedPackets = 0
    numberOfAcceptedPackets = 0
    numberOfSentPackets = 0
    ts = TransmissionChannel(intensity)

    def __init__(self, intensity):
        self.intensity = intensity

    def parity_bit(self, frame):
        frame_sum = 0
        for i in range(0, len(frame) - 1):
            frame_sum += frame[i]
        return frame_sum % 2

    def crc(self, array):
        crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)

        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, len(array) - 1):
            line += str(array[i])

        # generate CRC based on string
        crc_result = hex(crc32_func(bytes(line, encoding='utf-8')))
        return crc_result

    def MD5(self, array):
        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, len(array) - 1):
            line += str(array[i])
        textUtf8 = line.encode("utf-8")
        hash = hashlib.md5(textUtf8)
        hexa = hash.hexdigest()

        return hexa

    # sending
    def receive_frame(self, frame, index):
        # copy received frame to avoid damaging original frame
        self.frame = frame.copy()
        # self.frame = self.interfere_frame(self.frame)
        self.frame = self.ts.interfere_frame(self.frame)

        # generate control sum
        if (self.control_method == 0):
            control_sum = self.parity_bit(self.frame)
        elif (self.control_method == 1):
            control_sum = self.crc(self.frame)
        elif (self.control_method == 2):
            control_sum = self.MD5(self.frame)

        self.numberOfSentPackets += 1
        # check for control sum to be the same
        # with one stored in frame as last item
        if control_sum == self.frame[len(self.frame) - 1]:
            print("Frame ", index, " is good, continuing")
            self.numberOfAcceptedPackets += 1
            # delete last item of frame if control sums match
            received_frame = np.delete(self.frame, len(self.frame) - 1)
            # accept received frame
            self.result.insert(index, received_frame)
            return True
        else:
            print("Frame ", index, " is broken, repeating transmission")
            self.numberOfRejectedPackets += 1
            # store index of broken frame
            self.broken_frames.append(index)
            return False


    def printStatistics(self):
        print('Number of sent packets: ', self.numberOfSentPackets)
        print('Number of accepted packets: ', self.numberOfAcceptedPackets)
        print('Number of rejected packets: ', self.numberOfRejectedPackets)

    def finalize_img(self):
        # reshape final array to its original shape
        self.result = np.packbits(np.array(self.result, dtype=int))
        final_img = np.reshape(self.result, self.shape).astype(np.uint8)
        return Image.fromarray(final_img)
