import numpy as np
from PIL import Image
from Sender import parity_bit, crc, md5


class Receiver:
    def __init__(self):
        self.control_method = 0
        self.broken_frames = []
        self.result = []
        self.frame = []
        self.shape = None
        self.numberOfRejectedPackets = 0
        self.numberOfAcceptedPackets = 0
        self.numberOfSentPackets = 0

    def init_result_list(self, packets_count):
        for i in range(0, packets_count):
            self.result.append(0)

    # sending
    def receive_frame(self, frame, index):
        # copy received frame to avoid damaging original frame
        self.frame = frame.copy()

        # generate control sum
        if self.control_method == 0:
            control_sum = parity_bit(self.frame, len(self.frame) - 1)
        elif self.control_method == 1:
            control_sum = crc(self.frame, len(self.frame) - 1)
        elif self.control_method == 2:
            control_sum = md5(self.frame, len(self.frame) - 1)

        self.numberOfSentPackets += 1
        # check for control sum to be the same
        # with one stored in frame as last item
        if control_sum == self.frame[len(self.frame) - 1]:
            print("Frame ", index, " is good, continuing")
            self.numberOfAcceptedPackets += 1
            # delete last item of frame if control sums match
            received_frame = np.delete(self.frame, len(self.frame) - 1)
            # accept received frame
            self.result[index] = received_frame
            return True
        else:
            print("Frame ", index, " is broken, repeating transmission")
            self.numberOfRejectedPackets += 1
            # store index of broken frame
            self.broken_frames.append(index)
            return False

    def print_statistics(self):
        print('Number of sent packets: ', self.numberOfSentPackets)
        print('Number of accepted packets: ', self.numberOfAcceptedPackets)
        print('Number of rejected packets: ', self.numberOfRejectedPackets)

    def finalize_img(self):
        # reshape final array to its original shape
        self.result = np.packbits(np.array(self.result, dtype=int))
        final_img = np.reshape(self.result, self.shape).astype(np.uint8)
        return Image.fromarray(final_img)
