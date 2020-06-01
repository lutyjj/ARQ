import numpy as np
from PIL import Image
from Sender import Sender
from Receiver import Receiver


def start_test(chosen_algorithm, control_method, probability, windows_size, packet_size):
    img = Image.open("test.jpg")

    receiver = Receiver()
    sender = Sender(receiver, control_method, windows_size, packet_size)
    sender.set_ts_interference(probability)

    img_array = np.asarray(img)
    sender.data_to_binary(img_array)
    sender.split_array()

    sender.send_frames(chosen_algorithm)
    final_img = receiver.finalize_img()


window_size = 4
packet_size = 4
probability = 0.01
while (window_size <= 32):
    while (packet_size <= 32):
        while (probability <= 0.5):
            for alg in range(3):
                for control_method in range(3):
                    print(f'Window size: {window_size}')
                    print(f'Packet size: {packet_size}')
                    print(f'Probability: {probability}')
                    print(f'Alg: {alg}')
                    print(f'Control method: {control_method}')

                    start_test(alg, control_method, probability, window_size, packet_size)

                    print("\n")
            probability *= 2

        packet_size *= 2
        
    packet_size = 4
    probability = 0.01
    window_size *= 2
