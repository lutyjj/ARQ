import numpy as np
import crcmod as crcmod

class Sender:
    data = []
    shape = None


    def __init__(self, receiver, control_method):
        self.receiver = receiver
        self.control_method = control_method


    def parity_bit(self, array):
        frame_sum = 0
        for i in range(0, array.size):
            frame_sum += array[i]
        return frame_sum % 2


    def crc(self, array):
        crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)
        line = ''
        for i in range(0, array.size):
            line+=str(array[i])
        crcres = hex(crc32_func(bytes(line, encoding='utf-8')))
        return crcres


    def split_array(self, array):
        # store shape of original array
        self.shape = array.shape
        # temporary array to store splitted parts
        tmp_arr = []
        for i in range(len(array)):
            arr = array[i]
            for j in range(len(arr)):
                # for each array of individual pixels
                pix_arr = arr[j]
                if (self.control_method == 0):
                    # generate parity bit
                    bit = self.parity_bit(pix_arr)
                elif (self.control_method == 1):
                    bit = self.crc(pix_arr)
                # temporary array to append parity bit
                new_pix_arr = np.append(pix_arr, bit)
                # append array to final array
                tmp_arr.append(new_pix_arr)

        self.data = tmp_arr


    def send_frames(self):
        # send original shape
        self.receiver.shape = self.shape
        self.receiver.control_method = self.control_method
        # Stop-and-wait ARQ
        i = 0
        while i < len(self.data):
             # Receive ACK
            ACK = self.receiver.receive_frame(self.data[i], i)
            # if ACK is good - proceed to next frame
            # otherwise - repeat transmission
            if ACK:
                i += 1
