# WSL Setup Guide

---

## 🖥️ Install WSL
```bash
wsl --install --no-distribution
```

---

## 📂 Create a New Folder
```bash
mkdir "C:\WSL\MyNewImage"
```

---

## 📦 Import the Tar Image
```bash
wsl --import MyNewImage "FolderPath" "ImagePath"
```

**Example:**
```bash
wsl --import MyNewImage "C:\WSL\MyNewImage" "C:\Users\samer\Documents\AUB\AerialRobotics\mywsl.tar"
```

Check available images:
```bash
wsl --list
```

---

# 🚁 Using Blocks AirSim Environment

## 🔽 Install DirectX Runtime
Download and install from:  
[Microsoft DirectX Runtime](https://www.microsoft.com/en-us/download/details.aspx?id=35)

---

## 📥 Download AirSim Blocks
Get the latest release from:  
[AirSim Releases](https://github.com/microsoft/airsim/releases)

---

## ⚙️ Configure Settings
After running Blocks for the first time, it will create an AirSim settings file in:
```
Documents\AirSim
```

1. Replace this file with the `settings.json` provided in the GitHub repository.  
2. **Inside the settings file**, replace `WINDOWSIP` and `WSLIP` with their correct values.

---

## 🌐 Network Setup
1. **Windows Terminal (not Linux):**  
   Run `ifconfig` to get the **Windows IPv4 Ethernet WSL address**.

2. **WSL (Linux Terminal):**  
   Run:
   ```bash
   ip address show
   ```
   or
   ```bash
   ifconfig
   ```
   to get the **WSL image IP**.

3. Replace both IPs in the following command:

```bash
~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f airsim-copter --console --map   -A "--sim-address=WINDOWSIPV4 --sim-port-in=9002 --sim-port-out=9003"   --out udp:127.0.0.1:14550
```

---

## ▶️ Starting the System
1. Start **AirSim Blocks** in Windows.  
2. Open a new terminal in **WSL (SITL)** and run:

```bash
~/ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f airsim-copter --console --map   -A "--sim-address=172.29.160.1 --sim-port-in=9002 --sim-port-out=9003"   --out udp:127.0.0.1:14550
```

---

## 📝 Code Editing & Python Scripts

### ✏️ Creating Scripts
- Use **nano** to create/edit a script in WSL:  
  ```bash
  nano scriptname.py
  ```
  - `Ctrl+O` → Save file  
  - `Ctrl+X` → Exit  

- Use **VS Code** (if installed on Windows):  
  ```bash
  code .
  ```
  This will open the editor in the current directory.

---

### 📂 Cloning from GitHub
```bash
git clone repositoryaddress
```

---

### ▶️ Running Example Scripts
Run your Hello World scripts separately:
```bash
python3 HelloWorld_AirsimCamera.py
python3 HelloWorld_SITL.py
```

---

## ⚠️ Troubleshooting: Drone Not Arming
If the drone is not arming in SITL, adjust these parameters:

1. In the SITL GUI → go to **Parameters** → **Editor**  
2. Set:
   - `ARMING_CHECK = 0`
   - `EK3_GPS_CHECK = 0`
3. Click **Write** to save settings.

---
