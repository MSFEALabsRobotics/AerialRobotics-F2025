![Uploading 1_W30TLUP9avQwyyLfwu7WYA.jpg…]()



# OpenCV HSV Color Filtering (Python)

This tutorial shows how to use **HSV color space** in OpenCV to detect and isolate specific colors.

---

## Code Example

```python
import cv2
import numpy as np

# Load image
img = cv2.imread("image.jpg")

# Convert from BGR (default in OpenCV) to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define a color range (example: detect blue)
lower_blue = np.array([100, 150, 50])   # H, S, V lower bound
upper_blue = np.array([140, 255, 255])  # H, S, V upper bound

# Create a mask (white where blue is found)
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Apply mask to original image
result = cv2.bitwise_and(img, img, mask=mask)

# Show results
cv2.imshow("Original", img)
cv2.imshow("HSV", hsv)
cv2.imshow("Mask (blue areas)", mask)
cv2.imshow("Result (only blue)", result)

cv2.waitKey(0)
cv2.destroyAllWindows()
```

---

## Explanation

- OpenCV loads images in **BGR** format by default.  
- HSV stands for:
  - **H (Hue)** → the color type (0–179 in OpenCV).  
  - **S (Saturation)** → intensity or purity of the color.  
  - **V (Value)** → brightness of the color.  

- `cv2.inRange(hsv, lower, upper)` creates a binary mask where white = pixels inside the range.  
- `cv2.bitwise_and(img, img, mask=mask)` applies the mask to the original image.

**Tip:** Adjust the `lower` and `upper` HSV values to detect different colors.

---
