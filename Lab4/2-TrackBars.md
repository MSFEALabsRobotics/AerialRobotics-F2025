


# OpenCV Trackbar Thresholding Demo (Python)

This tutorial shows how to use a **trackbar (slider)** in OpenCV to interactively change the threshold value in real time.

---

## Code Example

```python
import cv2

def nothing(x):
    pass

# Load image
img = cv2.imread("image.jpg", 0)  # grayscale

# Create a window
cv2.namedWindow("Trackbar Demo")

# Add a trackbar (name, window, initial value, max value, callback)
cv2.createTrackbar("Thresh", "Trackbar Demo", 128, 255, nothing)

while True:
    # Get current position of the trackbar
    t = cv2.getTrackbarPos("Thresh", "Trackbar Demo")

    # Apply threshold with the trackbar value
    _, th = cv2.threshold(img, t, 255, cv2.THRESH_BINARY)

    # Show the result
    cv2.imshow("Trackbar Demo", th)

    # Break on ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
```

---

## Explanation

- `cv2.createTrackbar(name, window, initial, max, callback)` creates the slider.  
- `cv2.getTrackbarPos(name, window)` returns the current slider value.  
- We use that value (`t`) as the **threshold** for `cv2.threshold`.  
- Press **ESC** to quit the loop.

This way, you can adjust the threshold live and see how the binary image changes.
