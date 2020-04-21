from PIL import Image
import numpy as np
import random
from Sender import Sender
from Receiver import Receiver

img = Image.open("test.jpg")
img.show()

receiver = Receiver()
sender = Sender(receiver)

img_array = np.asarray(img)

sender.split_array(img_array)
sender.send_frames()

final_img = receiver.finalize_img()
final_img.show()