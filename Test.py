import numpy as np
from PIL import Image
from Sender import Sender
from Receiver import Receiver


def start_test(chosen_algorithm, control_method, probability, windows_size, packet_size, model, P01, P10):
    img = Image.open("test.jpg")

    receiver = Receiver()
    sender = Sender(receiver, control_method, windows_size, packet_size)
    sender.set_ts_interference(probability, model, P01, P10)

    img_array = np.asarray(img)
    sender.data_to_binary(img_array)
    sender.split_array()

    sender.send_frames(chosen_algorithm)

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

    final_img = receiver.finalize_img()
    return receiver.numberOfAcceptedPackets, receiver.numberOfRejectedPackets, ber

def run_test():
    file = open("test_results.txt", "w")
    times_to_repeat = 10
    window_size = 4
    packet_size = window_size
    probability = 0.01
    P01 = 0.01
    P10 = 0.01
    while (window_size <= 16):
        while (probability <= 0.5):
            for alg in range(3):
                for control_method in range(3):
                    model = 0
                    file.write(f'Model: {model} \n')
                    file.write(f'Window size: {window_size} \n')
                    file.write(f'Packet size: {packet_size} \n')
                    file.write(f'Probability: {probability} \n')
                    file.write(f'Alg: {alg} \n')
                    file.write(f'Control method: {control_method} \n')

                    sum_accepted = 0
                    sum_rejected = 0
                    sum_ber = 0

                    for count in range(times_to_repeat):
                        accepted, rejected, ber = start_test(alg, control_method, probability, window_size, packet_size,
                                                                model,0,0)

                        if (count == 0):
                            sum_accepted = accepted
                        sum_rejected += rejected
                        sum_ber += ber

                    sum_rejected = sum_rejected / times_to_repeat
                    sum_ber = sum_ber / times_to_repeat

                    file.write(f'Accepted: {sum_accepted} \n')
                    file.write(f'Rejected: {sum_rejected} \n')
                    file.write(f'Ber: {sum_ber} \n\n')

                    model = 1
                    while (P01 <= 0.5):
                        file.write(f'Model: {model} \n')
                        file.write(f'Window size: {window_size} \n')
                        file.write(f'Packet size: {packet_size} \n')
                        file.write(f'Probability: {probability} \n')
                        file.write(f'P01: {P01} \n')
                        file.write(f'P10: {P10} \n')
                        file.write(f'Alg: {alg} \n')
                        file.write(f'Control method: {control_method} \n')

                        sum_accepted = 0
                        sum_rejected = 0
                        sum_ber = 0

                        for count in range(times_to_repeat):
                            accepted, rejected, ber = start_test(alg, control_method, probability, window_size, packet_size,
                                                                    model, P01, P10)

                            if (count == 0):
                                sum_accepted = accepted
                            sum_rejected += rejected
                            sum_ber += ber

                        sum_rejected = sum_rejected / times_to_repeat
                        sum_ber = sum_ber / times_to_repeat

                        file.write(f'Accepted: {sum_accepted} \n')
                        file.write(f'Rejected: {sum_rejected} \n')
                        file.write(f'Ber: {sum_ber} \n\n')
                        P01 *= 2
                probability *= 2
                P01 = 0.01
                P10 *= 2

            packet_size *= 2

        packet_size = 4
        probability = 0.01
        P01 = 0.01
        P10 = 0.01
        window_size *= 2

    file.close()