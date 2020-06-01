import random


class TransmissionChannel:
    probability = 0.1
    errorCounter = 0
    totalErrors = 0

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
        ack = self.receiver.receive_frame(frame, index)

        if ack == True:
            self.totalErrors += self.errorCounter

        # Return ACK
        return ack

    # BSC - binary symmetric channel symulation
    def bsc(self, frame):
        noised = []
        self.errorCounter = 0
        for bit in frame:
            noised.append(self.flip_bit(bit, self.probability))

        return noised

    # Flip bit with certain probability
    def flip_bit(self, bit, probability):
        if random.random() < probability:
            self.errorCounter += 1
            if bit == 0:
                bit = 1
            else:
                bit = 0
            
        return bit

    # def Gilbert
    # def BER             #BIT ERROR RATE
    def ber(self, bits_count):
        return (self.totalErrors / bits_count) * 100