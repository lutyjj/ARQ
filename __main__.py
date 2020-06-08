import numpy as np
from PIL import Image
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

print('Choose discrete channel model:')
print('0. Binary Symmetric Channel')
print("1. Gilbert's Model")
model = int(input())

print('Enter interference probability (float, 0 < x < 1): ')
probability = float(input())
print('Enter window size: ')
windows_size = int(input())
print('Enter packet size: ')
packet_size = int(input())

img = Image.open("test.jpg")
scaled_img = img.resize((640, 640))
scaled_img.show()

receiver = Receiver()
sender = Sender(receiver, control_method, windows_size, packet_size)
sender.set_ts_interference(probability, model)

img_array = np.asarray(img)
sender.data_to_binary(img_array)
sender.split_array()

print('Starting transmission:')
sender.send_frames(chosen_algorithm)
receiver.print_statistics()

print(f'BER: {sender.ber()} %')

final_img = receiver.finalize_img()
scaled_final_img = final_img.resize((640, 640))
scaled_final_img.show()
