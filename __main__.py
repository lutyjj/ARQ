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
if model == 1:
    print('Enter interference probability transition from 0 to 1 (float, 0 < x < 1): ')
    P01 = float(input())
    print('Enter interference probability transition from 1 to 0  (float, 0 < x < 1): ')
    P10 = float(input())
else:
    P01 = 0
    P10 = 0
    pass

print('Enter window size: ')
windows_size = int(input())
print('Enter packet size: ')
packet_size = int(input())

img = Image.open("test.jpg")
scaled_img = img.resize((640, 640))
scaled_img.show()

receiver = Receiver()
sender = Sender(receiver, control_method, windows_size, packet_size)
sender.set_ts_interference(probability, model, P01, P10)

img_array = np.asarray(img)
sender.data_to_binary(img_array)
sender.split_array()

print('Starting transmission:')
sender.send_frames(chosen_algorithm)
receiver.print_statistics()

error_counter = 0
ber = 0
for j in range(0, len(receiver.result)):
    final_pack = receiver.result[j].astype(np.uint8)
    start_pack = sender.packets[j]
    for i in range(0, packet_size):
        if start_pack[i] != final_pack[i]:
            error_counter += 1
    j += 1
ber = error_counter/(len(receiver.result)*packet_size)*100
print('BER: ', ber, '%')

final_img = receiver.finalize_img()
scaled_final_img = final_img.resize((640, 640))
scaled_final_img.show()
