import random
import numpy as np
from PIL import Image
import crcmod

class Receiver:
    intensity = 0.5
    broken_frames = []
    result = []
    shape = None
    frame = []
    control_method = 0


    def __init__(self, intensity):
        self.intensity = intensity


    # interference
    def interfere_array(self, array):
        # probability of interference
        if random.random() < self.intensity:
            index = random.randint(0, array.size - 1)
            array[index] = random.randint(0, 255)
        return array


    def parity_bit(self, array):
        frame_sum = 0
        for i in range(0, array.size - 1):
            frame_sum += array[i]
        return frame_sum % 2


    def crc(self, array):
        crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)
        
        line = ''
        for i in range(0, array.size - 1):
            line+=str(array[i])
        crcres = hex(crc32_func(bytes(line, encoding='utf-8')))    
        return crcres


    # sending
    def receive_frame(self, frame, index):
        self.frame = frame.copy()
        self.frame = self.interfere_array(self.frame)

        if (self.control_method == 0):
            received_bit = self.parity_bit(self.frame)
        elif (self.control_method == 1):
            received_bit = self.crc(self.frame)
        # check for parity bit to be the same
        # with one stored in frame as last item
        if received_bit == self.frame[len(self.frame) - 1]:
            print("Frame ", index, " is good, continuing")
            # delete last item if bits match
            received_frame = np.delete(self.frame, len(self.frame) - 1)
            # accept received frame
            self.result.append(received_frame)
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