<img width="368" height="410" alt="image" src="https://github.com/user-attachments/assets/b4904a0f-5f04-4be8-ace8-a22d9b12bfb1" />


# Python Demo: Class & Time

## 1. Minimal Python Class

```python
class Robot:
    def __init__(self, name):
        self.name = name       # variable inside the class
        self.battery = 100     # another variable (default)

    def greet(self):
        return f"Hello, I am {self.name}. Battery at {self.battery}%."

def demo():
    r = Robot("OctoBot")
    print(r.greet())

if __name__ == "__main__":
    demo()
```

### Output
```
Hello, I am OctoBot. Battery at 100%.
```

---

## 2. Working with Time in Python

The built-in `time` module helps with measuring and pausing execution.

```python
import time

# Get current time in seconds since Epoch
now = time.time()
print("Current time (seconds since 1970):", now)

# Convert to human-readable format
print("Readable time:", time.ctime(now))

# Pause program for 2 seconds
print("Waiting...")
time.sleep(2)
print("Done waiting!")

# Measure how long a task takes
start = time.time()
for i in range(5):
    print(i)
    time.sleep(0.5)  # simulate work
end = time.time()
print("Elapsed time:", end - start, "seconds")
```

### Key Functions
- `time.time()` → current timestamp (float, seconds since 1970).  
- `time.ctime()` → human-readable time string.  
- `time.sleep(x)` → pause execution for `x` seconds.  
- Difference of two `time.time()` calls → elapsed duration.  

---
