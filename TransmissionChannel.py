import random


class TransmissionChannel:
    def __init__(self, intensity):
        self.intensity = intensity

    frame = []

    # interference
    def interfere_frame(self, frame):
        # intensity of interference
        if random.random() < self.intensity:
            index = random.randint(0, len(frame) - 1)
            frame[index] = random.randint(0, 1)
        return frame


   # def BSC(self, frame):





   # def Gilbert

  #  def BER             #BIT ERROR RATE