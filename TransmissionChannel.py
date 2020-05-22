import random


class TransmissionChannel:
    probability = 0.1

    def __init__(self, receiver):
        self.receiver = receiver
    
    # Send all meta-data to receiver
    def init_metadata(self, shape, control_method, packets_count):
        self.receiver.shape = shape
        self.receiver.init_result_list(packets_count)
        self.receiver.control_method = control_method

    # Pass frame to receiver
    def pass_frame(self, frame, index):
        frame = self.bsc(frame)
        
        # Return ACK
        return self.receiver.receive_frame(frame, index)

    # BSC - binary symmetric channel symulation
    def bsc(self, frame):
        noised = []
        for bit in frame:
            noised.append(self.flip_bit(bit, self.probability))

        return noised

    # Flip bit with certain probability
    def flip_bit(self, bit, probability):
        if random.random() < probability:
            bit = 1 if bit == 0 else 1
            
        return bit

    # def Gilbert
    # def BER             #BIT ERROR RATE
