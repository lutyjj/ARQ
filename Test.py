import numpy as np
from PIL import Image
from Sender import Sender
from Receiver import Receiver

file = open("test_results.txt", "w")

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
    
    return receiver.numberOfAcceptedPackets, receiver.numberOfRejectedPackets, sender.ber()

times_to_repeat = 20
window_size = 4
packet_size = 4
probability = 0.01
while (window_size <= 16):
    while (packet_size <= 16):
        while (probability <= 0.5):
            for alg in range(3):
                for control_method in range(3):
                    file.write(f'Window size: {window_size} \n')
                    file.write(f'Packet size: {packet_size} \n')
                    file.write(f'Probability: {probability} \n')
                    file.write(f'Alg: {alg} \n')
                    file.write(f'Control method: {control_method} \n')

                    sum_accepted = 0
                    sum_rejected = 0
                    sum_ber = 0

                    for count in range(times_to_repeat):
                        accepted, rejected, ber = start_test(alg, control_method, probability, window_size, packet_size)
                        
                        if (count == 0):
                            sum_accepted = accepted
                        sum_rejected += rejected
                        sum_ber += ber

                    sum_rejected = sum_rejected / times_to_repeat
                    sum_ber = sum_ber / times_to_repeat

                    file.write(f'Accepted: {sum_accepted} \n')
                    file.write(f'Rejected: {sum_rejected} \n')
                    file.write(f'Ber: {sum_ber} \n\n')
            probability *= 2

        packet_size *= 2
        
    packet_size = 4
    probability = 0.01
    window_size *= 2

file.close()