import random


class TransmissionChannel:

    def __init__(self, intensity):
        self.intensity = intensity

    frame = []
    prop = 0.2
    # interference
    def interfere_frame(self, frame):
        # intensity of interference
        if random.random() < self.intensity:
            index = random.randint(0, len(frame) - 1)
            frame[index] = random.randint(0, 1)
        return frame

    def bsc_bit(self, bit, prop):
            if(self.draw(prop)):
                if(bit == '0'):
                    bit = '1'
                else:
                    bit = '0'
            return bit

    def bsc(self, frame):
        noised = []
        for bit in frame:
            noised.append(self.bsc_bit(bit, self.prop))
        return noised

    def draw(self, propability):
        seed = random.random()
        if(seed <= propability):
            return True
        else:
            return False






   # def Gilbert

  #  def BER             #BIT ERROR RATE