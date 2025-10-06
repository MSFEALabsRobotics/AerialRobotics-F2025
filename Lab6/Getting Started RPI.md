# 🛩️ Setting up Raspberry Pi for AirSim

This guide explains how to prepare a **Raspberry Pi (Lite or Desktop)** to connect with **AirSim** and process image or MAVLink data.

---

## 1️⃣ Download Required Tools

### 🧰 Raspberry Pi Imager
Download and install the official imager from:  
🔗 [https://www.raspberrypi.com/software/](https://www.raspberrypi.com/software/)

### 💿 Raspberry Pi OS Image
Choose either:
- **Raspberry Pi OS Lite** (for headless setup)
- **Raspberry Pi OS with Desktop** (if you prefer GUI setup)  
🔗 [https://www.raspberrypi.com/software/operating-systems/](https://www.raspberrypi.com/software/operating-systems/)

---

## 2️⃣ Flash the SD Card

1. Open **Raspberry Pi Imager**  
2. Select the OS and the SD card  
4. Click **Write** to flash the image  
5. Insert the SD card into the Pi

---

## 3️⃣ First Boot

1. Connect:
   - HDMI display  
   - Keyboard
   - Power supply  
2. Boot up and open terminal  
3. Run configuration:
   ```bash
   sudo raspi-config
   ```
   - Set Wi-Fi country as US and connect to network  
   - Enable **SSH** (used for remote connection)  

---

## 4️⃣ Basic Setup Commands

Update and install Python essentials:
```bash
sudo apt update
sudo apt install python3-pip python3-numpy python3-msgpack python3-setuptools python3-wheel -y
```

---

## 5️⃣ Install Python Packages for AirSim

```bash
pip install numpy msgpack-rpc-python tornado backports.ssl_match_hostname --break-system-packages
pip install --no-build-isolation airsim --break-system-packages
sudo apt install -y libgl1 libglib2.0-0
```

---

## 6️⃣ Optional: pymavlink for MAVLink Communication

```bash
pip3 install pymavlink --break-system-packages
```

---

## 7️⃣ Allow Windows ↔ Pi Network Communication

On **Windows**, open Command Prompt as Administrator and run:

### 🔹 Allow ICMP Ping
```bash
netsh advfirewall firewall add rule name="Allow ICMPv4 In" protocol=icmpv4:8,any dir=in action=allow
```

### 🔹 Optional Port Forwarding for MAVLink (14550) and AirSim Ports (9002, 9003)
Replace `172.29.168.136` with your **WSL/Windows IP**:
```bash
netsh interface portproxy add v4tov4 listenport=14550 listenaddress=0.0.0.0 connectport=14550 connectaddress=172.29.168.136
netsh interface portproxy add v4tov4 listenport=9002 listenaddress=0.0.0.0 connectport=9002 connectaddress=172.29.168.136
netsh interface portproxy add v4tov4 listenport=9003 listenaddress=0.0.0.0 connectport=9003 connectaddress=172.29.168.136
netsh interface portproxy show all
netsh advfirewall firewall add rule name="WSL MAVLink" dir=in action=allow protocol=UDP localport=14550,9002,9003
```

---

## 8️⃣ Test AirSim Python Connection

Create a simple test file Hello Airsim Frame.py


---

