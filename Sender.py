import numpy as np
import crcmod as crcmod


class Sender:
    control_method = 0
    window_size = 4
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

        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, array.size):
            line += str(array[i])

        # generate CRC based on string
        crc_result = hex(crc32_func(bytes(line, encoding='utf-8')))
        return crc_result

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

                # generate control sum
                if (self.control_method == 0):
                    bit = self.parity_bit(pix_arr)
                elif (self.control_method == 1):
                    bit = self.crc(pix_arr)

                # create temporary array to append control sum
                new_pix_arr = np.append(pix_arr, bit)
                # append array to final array
                tmp_arr.append(new_pix_arr)

        # make splitted array (frames) sender's data
        self.data = tmp_arr

    def send_frames(self, chosen_algorithm):
        # send original shape and control method
        self.receiver.shape = self.shape
        self.receiver.control_method = self.control_method

        # Stop-and-wait ARQ
        if chosen_algorithm == 0:
            i = 0
            while i < len(self.data):
                # Receive ACK
                ACK = self.receiver.receive_frame(self.data[i], i)
                # if ACK is good - proceed to next frame
                # otherwise - repeat transmission
                if ACK:
                    i += 1

        # Selective-Repeat
        if chosen_algorithm == 1:
            ACK = []
            for i in range(0, len(self.data)):
                ACK.append(False)

            i = 0
            window_end = i + self.window_size

            while i < len(self.data):
                slide = 0
                NACK = False
                for j in range(i, window_end):
                    if j == len(self.data):
                        break

                    if not ACK[j]:
                        ACK[j] = self.receiver.receive_frame(self.data[j], j)
                        if ACK[j] == True and NACK == False:
                            slide += 1
                        else:
                            NACK = True
                    else:
                        pass

                if not NACK:
                    if (window_end + self.window_size) >= len(self.data):
                        window_end = len(self.data)
                    else:
                        window_end += self.window_size
                    i += self.window_size

                else:
                    if(window_end + self.window_size) >= len(self.data):
                        window_end = len(self.data)
                    else:
                        window_end += slide
                    i += slide









