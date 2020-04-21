import random
import numpy as np
from PIL import Image

class Receiver:
    probability = 0.05
    broken_frames = []
    result = []
    shape = None

    def __init__(self):
        pass


    # interference
    def interfere_array(self, array):
        # probability of interference
        if random.random() < self.probability:
            # don't interfere parity bit
            index = random.randint(0, array.size - 2)
            array[index] = random.randint(0, 255)
        return array


    # sending
    def receive_frame(self, array, index):
        array = self.interfere_array(array)

        frame_sum = 0
        # generate parity bit
        for i in range(len(array) - 1):
            frame_sum += array[i]
        received_bit = frame_sum % 2

        # check for parity bit to be the same
        # with one stored in frame as last item
        if received_bit == array[len(array) - 1]:
            print("Frame ", index, " is good, continuing")
            # delete last item if bits match
            received_frame = np.delete(array, len(array) - 1)
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