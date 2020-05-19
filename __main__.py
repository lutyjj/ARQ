from PIL import Image
import numpy as np
from Sender import Sender
from Receiver import Receiver

print('Choose ARQ protocol:')
print('0. Stop-and-Wait')
print('1. Selective-Repeat')
print('2. Go-Back')
chosen_algorithm = int(input())

print('Choose error-detecting method:')
print('0. Parity bit (default)')
print('1. CRC')
print('2. MD-5')
control_method = int(input())

print('Enter interference intensity (float, 0 < x < 1): ')
intensity = float(input())
print('Enter window size: ')
windows_size = int(input())
print('Enter packet size: ')
packet_size = int(input())

img = Image.open("test.jpg")
img.show()
receiver = Receiver(intensity)
sender = Sender(receiver, control_method, windows_size, packet_size)

img_array = np.asarray(img)
sender.data_to_binary(img_array)
sender.split_array()

print('Starting transmission:')
sender.send_frames(chosen_algorithm)
receiver.printStatistics()
final_img = receiver.finalize_img()
final_img.show()