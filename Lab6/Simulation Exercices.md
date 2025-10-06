# 🧠 Aerial Robotics – Raspberry Pi Exercises

These exercises are designed to integrate **AirSim**, **YOLO**, and **edge computing** on the **Raspberry Pi** platform.

Each task focuses on using onboard computation for perception and control in simulated or real-world drone applications.

---

## 🚁 Exercise 1 — Tree Navigation and Orbiting

### Objective
While computing directly on your **Raspberry Pi**, write a program that will:

1. Connect to the drone in the **LandscapeMountains** environment.
2. Navigate to a specific **GPS coordinate** corresponding to a tree.
3. Upon arrival, **detect the tree** using onboard computer vision.
4. Perform a **circular motion** around the tree, simulating a drone that is spraying or filming it.

### Deliverables
- Python script that performs the full navigation and orbiting behavior.
- A short description of how the tree was detected.
- A recorded flight path or log confirming the circular trajectory.

---

## 🧍‍♂️ Exercise 2 — Pose-Based Drone Commands

### Objective
While computing on the **Raspberry Pi**, use **YOLO pose detection** to control the drone using **body poses** as commands.

The system should be able to recognize and react to at least the following actions:

| Pose | Command |
|------|----------|
| Arms raised | Take off |
| Arms down | Land |
| One arm stretched horizontally | Perform a 360° turn |
| Specific gesture or stance | Servo (follow the person while maintaining distance) |

### Deliverables
- Python script integrating YOLO pose detection and drone control.
- A brief explanation of how each pose was mapped to its corresponding command.
- Demonstration video or simulation log showing pose-driven flight.

---

**Notes:**
- All processing must be performed on the Raspberry Pi (edge computing).  
- The exercises can be executed in **AirSim simulation** or with a **real drone testbed**.  
- Focus on perception, decision, and control — not on manual intervention.

---

