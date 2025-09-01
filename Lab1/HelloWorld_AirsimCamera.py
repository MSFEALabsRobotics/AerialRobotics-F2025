import airsim
import cv2
import numpy as np

client = airsim.MultirotorClient(ip="WINDOWSIP", port=5000)
client.confirmConnection()

while True:
    responses = client.simGetImages([
        airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
    ])
    img1d = np.frombuffer(responses[0].image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(responses[0].height, responses[0].width, 3)
    cv2.imshow("AirSim Frame", img_rgb)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
