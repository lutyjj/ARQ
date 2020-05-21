import numpy as np
import crcmod as crcmod
import hashlib

from TransmissionChannel import TransmissionChannel


class Sender:
    control_method = 0
    window_size: int = 4
    counter = 0
    bitList = []
    packets = []
    shape = None

    def __init__(self, receiver, control_method, window_size, packet_size):
        self.control_method = control_method
        self.window_size = window_size
        self.packet_size = packet_size
        self.ts = TransmissionChannel(receiver)

    def set_ts_interference(self, probability):
        self.ts.probability = probability

    def data_to_binary(self, array):
        # store shape of original array
        self.shape = array.shape
        # create binary list from numpy array
        self.bitList = np.unpackbits(array)

    def parity_bit(self, array):
        frame_sum = 0
        for i in range(0, len(array)):
            frame_sum += array[i]
        return frame_sum % 2

    def crc(self, array):
        crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)

        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, len(array)):
            line += str(array[i])

        # generate CRC based on string
        crc_result = hex(crc32_func(bytes(line, encoding='utf-8')))
        return crc_result

    def MD5(self, array):
        # generate string of ints without last item (control sum)
        line = ''
        for i in range(0, len(array)):
            line += str(array[i])
        text_utf8 = line.encode("utf-8")
        hash_result = hashlib.md5(text_utf8)
        hex_result = hash_result.hexdigest()

        return hex_result

    def split_array(self):
        packet = []
        counter = 0

        for bit in self.bitList:
            packet.append(bit)

            counter += 1
            if counter == self.packet_size:
                # store eight-bit packets
                self.packets.append(packet)
                packet = []
                counter = 0

        # generate control sum for each packet
        if self.control_method == 0:
            for packet in self.packets:
                bit = self.parity_bit(packet)
                packet.append(bit)
        elif self.control_method == 1:
            for packet in self.packets:
                bit = self.crc(packet)
                packet.append(bit)
        elif self.control_method == 2:
            for packet in self.packets:
                bit = self.MD5(packet)
                packet.append(bit)

    def send_frames(self, chosen_algorithm):
        # send original shape and control method
        self.ts.init_connection(self.shape, self.control_method, len(self.packets))

        # Stop-and-wait ARQ
        if chosen_algorithm == 0:
            i = 0
            while i < len(self.packets):
                # Receive ACK
                ACK = self.ts.pass_frame(self.packets[i], i)
                # if ACK is good - proceed to next frame
                # otherwise - repeat transmission
                if ACK:
                    i += 1

        # Selective-Repeat
        if chosen_algorithm == 1:
            ACK = []
            for i in range(0, len(self.packets)):
                ACK.append(False)

            i = 0
            window_end = i + self.window_size

            while i < len(self.packets):
                slide = 0
                NACK = False
                # receive ACK from window
                for j in range(i, window_end):
                    if j == len(self.packets):
                        break

                    if not ACK[j]:
                        ACK[j] = self.ts.pass_frame(self.packets[j], j)

                        # check if the entire window has been sent correctly
                        if ACK[j] == True and NACK == False:
                            slide += 1
                        else:
                            NACK = True
                    else:
                        pass

                # slide window by the window_size if NACK hasn't appear
                if not NACK:
                    if (window_end + self.window_size) >= len(self.packets):
                        window_end = len(self.packets)
                    else:
                        window_end += self.window_size
                    i += self.window_size

                # otherwise - slide by value of slide counter
                else:
                    if (window_end + self.window_size) >= len(self.packets):
                        window_end = len(self.packets)
                    else:

                        window_end += slide
                    i += slide

        # Go-Back

        if chosen_algorithm == 2:
            ACK = []
            for i in range(0, len(self.packets)):
                ACK.append(False)

            i = 0
            window_start = i
            window_end = i + self.window_size
            while i < len(self.packets):
                while i < window_end and i < len(self.packets):
                    ACK[i] = self.ts.pass_frame(self.packets[i], i)

                    if ACK[window_start]:
                        window_end += 1
                        window_start += 1
                    else:
                        if window_end > len(self.packets):
                            window_end = len(self.packets)
                            for k in range(window_start + 1, window_end):
                                if ACK[k]:
                                    i = window_start - 1
                                break

                    i += 1

                    pass
                pass

                if i == window_end:
                    i = window_start
                pass
            pass
