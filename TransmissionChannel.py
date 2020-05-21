import random


class TransmissionChannel:
    probability = 0.1

    def __init__(self, receiver):
        self.receiver = receiver

    def init_connection(self, shape, control_method, packets_count):
        self.receiver.shape = shape
        self.receiver.init_result_list(packets_count)
        self.receiver.control_method = control_method

    def pass_frame(self, frame, index):
        frame = self.bsc(frame)
        return self.receiver.receive_frame(frame, index)

    def bsc_bit(self, bit, probability):
        if self.draw(probability):
            if bit == 0:
                bit = 1
            else:
                bit = 0
        return bit

    def bsc(self, frame):
        noised = []
        for bit in frame:
            noised.append(self.bsc_bit(bit, self.probability))
        return noised

    def draw(self, probability):
        seed = random.random()
        if seed <= probability:
            return True
        else:
            return False

# def Gilbert

#  def BER             #BIT ERROR RATE
