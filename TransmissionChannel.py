import random


class TransmissionChannel:
    model = 0
    probability = 0.1
    errorCounter = 0
    totalErrors = 0
    gilbertState = 0
    noisePropS0 = 0.3
    noisePropS1 = 0.3
    P01 = 0.3
    P00 = 1 - 0.3
    P10 = 0.3
    P11 = 1 - 0.3

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
    def addGilbertNoiseBit(self, bit):
        if self.gilbertState == 0:          #losowanie stanu modelu Gilberta
            if random.random() < self.P01:
                self.gilbertState = 1
        elif self.gilbertState == 1:
            if random.random() < self.P10:
                self.gilbertState = 0

        if self.gilbertState == 0:               #zamiana bitu na przeciwny z prawdopodobienstwem dla danego stanu modelu
            bit = self.flip_bit(bit, self.noisePropS0)
        elif self.gilbertState == 1:
            bit = self.flip_bit(bit, self.noisePropS1)

        return bit

    def addGilbertNoise(self, packet):
        self.errorCounter = 0
        noised = []
        for bit in packet:
            noised.append(self.addGilbertNoiseBit(bit))

        return noised


    # def BER        #BIT ERROR RATE
    def ber(self, bits_count):
        return (self.totalErrors / bits_count) * 100