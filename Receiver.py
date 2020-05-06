import random
import numpy as np
from PIL import Image
import crcmod


class Receiver:
    control_method = 0
    intensity = 0.5
    broken_frames = []
    result = []
    frame = []
    shape = None

    def __init__(self, intensity):
        self.intensity = intensity

    # interference
    def interfere_frame(self, frame):
        # intensity of interference
        if random.random() < self.intensity:
            index = random.randint(0, frame.size - 1)
            frame[index] = random.randint(0, 255)
        return frame

    def parity_bit(self, frame):
        frame_sum = 0
        for i in range(0, frame.size - 1):
            frame_sum += frame[i]
        return frame_sum % 2

    def crc(self, array):
        crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)

        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, array.size - 1):
            line += str(array[i])

        # generate CRC based on string
        crc_result = hex(crc32_func(bytes(line, encoding='utf-8')))
        return crc_result

    # sending
    def receive_frame(self, frame, index):
        # copy received frame to avoid damaging original frame
        self.frame = frame.copy()
        self.frame = self.interfere_frame(self.frame)

        # generate control sum
        if (self.control_method == 0):
            control_sum = self.parity_bit(self.frame)
        elif (self.control_method == 1):
            control_sum = self.crc(self.frame)

        # check for control sum to be the same
        # with one stored in frame as last item
        if control_sum == self.frame[len(self.frame) - 1]:
            print("Frame ", index, " is good, continuing")
            # delete last item of frame if control sums match
            received_frame = np.delete(self.frame, len(self.frame) - 1)
            # accept received frame
            self.result.insert(index, received_frame)
            return True
        else:
            print("Frame ", index, " is broken, repeating transmission")
            # store index of broken frame
            self.broken_frames.append(index)
            return False

    def finalize_img(self):
        # reshape final array to its original shape
        final_img = np.reshape(self.result, self.shape).astype(np.uint8)
        return Image.fromarray(final_img)
