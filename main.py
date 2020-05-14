from PIL import Image
import numpy as np
import random
from Sender import Sender
from Receiver import Receiver


print('Choose ARQ protcol:')
print('0. Stop-and-Wait')
print('1. Selective-Repeat')
print('2. Go-Back')
chosen_algorithm = int(input())

print('Choose error-detecting method:')
print('0. Parity bit (default)')
print('1. CRC')
control_method = int(input())

print('Enter interference intensity (float, 0 < x < 1): ')
intensity = float(input())

img = Image.open("test.jpg")
img.show()

receiver = Receiver(intensity)
sender = Sender(receiver, control_method)

img_array = np.asarray(img)
sender.split_array(img_array)

print('Starting transmission:')
sender.send_frames(chosen_algorithm)

final_img = receiver.finalize_img()
final_img.show()