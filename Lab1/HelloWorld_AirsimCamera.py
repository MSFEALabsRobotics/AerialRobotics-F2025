import airsim
import cv2
import numpy as np

# Replace with Windows host IP
client = airsim.MultirotorClient(ip="WINDOWSIP")
client.confirmConnection()

# Get image from front-center camera
responses = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
])

img1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
img_rgba = img1d.reshape(responses[0].height, responses[0].width, 3)

cv2.imshow("AirSim Camera", img_rgba)
cv2.waitKey(0)
