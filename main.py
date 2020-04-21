from PIL import Image
import numpy
import random

img = Image.open("test.jpg")
img.show()


# parity bit generator
def parity_bit(self):
    frame_sum = 0
    for i in range(0, self.size):
        frame_sum += self[i]
    return frame_sum % 2


probability = 0.05


# interference
def interfere_array(self):
    # probability of interference
    if random.random() < probability:
        # don't interfere parity bit
        index = random.randint(0, self.size - 2)
        self[index] = random.randint(0, 255)
    return self


# split into sub-arrays
def split_array(self):
    tmp_arr = []
    for i in range(len(self)):
        arr = self[i]
        for j in range(len(arr)):
            # for each array of individual pixels
            pix_arr = arr[j]
            # generate parity bit
            bit = parity_bit(pix_arr)
            # temporary array to append parity bit
            new_pix_arr = numpy.append(pix_arr, bit)
            # append array to final array
            tmp_arr.append(new_pix_arr)
    return tmp_arr


broken_frames = []


# sending
def receive_frame(self, index):
    self = interfere_array(self)

    frame_sum = 0
    # generate parity bit
    for i in range(len(self) - 1):
        frame_sum += self[i]
    received_bit = frame_sum % 2

    # checking for parity
    if received_bit == self[len(self) - 1]:
        print("Frame ", index, " is good, continuing")
    else:
        print("Frame ", index, " is broken, repeating transmission")
        receive_frame(self, index)

    # remove parity bit from received array and return it
    return numpy.delete(self, len(self) - 1)


img_array = numpy.asarray(img)
shape = img_array.shape
splt_array = split_array(img_array)

# array to store received frames
result = []
# start transmission
for x in range(len(splt_array)):
    result = numpy.append(result, receive_frame(splt_array[x], x))

# reshape final array to original (4, 4, 3) shape
result = numpy.reshape(result, shape).astype(numpy.uint8)
# convert to image
result = Image.fromarray(result)
result.show()
