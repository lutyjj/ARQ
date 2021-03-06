import random


class TransmissionChannel:
    model = 0
    probability = 0.1
    gilbertState = 0
    P01 = 0.3
    P10 = 0.3

    def __init__(self, receiver):
        self.receiver = receiver

    # Send all meta-data to receiver
    def init_metadata(self, shape, control_method, packets_count):
        self.receiver.shape = shape
        self.receiver.init_result_list(packets_count)
        self.receiver.control_method = control_method

    # Pass frame to receiver
    def pass_frame(self, frame, index):
        if self.model == 0:
            frame = self.bsc(frame)
        if self.model == 1:
            frame = self.addGilbertNoise(frame)
        ack = self.receiver.receive_frame(frame, index)

        # Return ACK
        return ack

    # BSC - binary symmetric channel symulation
    def bsc(self, frame):
        noised = []
        for bit in frame:
            noised.append(self.flip_bit(bit, self.probability))

        return noised

    # Flip bit with certain probability
    def flip_bit(self, bit, probability):
        if random.random() < probability:
            if bit == 0:
                bit = 1
            else:
                bit = 0

        return bit

    # def Gilbert
    def addGilbertNoiseBit(self, bit):
        if self.gilbertState == 0:  # losowanie stanu modelu Gilberta
            if random.random() < self.P01:
                self.gilbertState = 1
        elif self.gilbertState == 1:
            if random.random() < self.P10:
                self.gilbertState = 0

        if self.gilbertState == 0:  # zamiana bitu na przeciwny z prawdopodobienstwem dla danego stanu modelu
            bit = self.flip_bit(bit, self.probability)
        elif self.gilbertState == 1:
            bit = self.flip_bit(bit, self.probability)

        return bit

    def addGilbertNoise(self, packet):
        noised = []
        for bit in packet:
            noised.append(self.addGilbertNoiseBit(bit))

        return noised
