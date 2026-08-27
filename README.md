
# Autonomous + FPV Drone project! 

A dual-mode quadcopter engineered to bridge manual FPV piloting with companion controlled autonomous movement. The drone switches between raw pilot input and onboard computer-vision navigation, allowing an autonomous tracking loop to guide flight trajectories while preserving manual pilot override.

## System Architecture

The drone operates on a dual-layer architecture separating real-time flight dynamics from high-level perception and path planning:

* **Flight Controller (ArduPilot):** Handles motor mixing, sensor fusion (IMU, barometer, GPS), stabilization, and failsafe routines. Runs low-level PID loops to execute position and velocity targets.
* **Companion Computer (Raspberry Pi):** Interfaces with an onboard camera feed to run lightweight YOLO object detection models in real time. It calculates target bounding-box offsets, translates pixel errors into velocity vectors, and streams `SET_POSITION_TARGET_LOCAL_NED` commands via MAVLink over UART.
* **FPV & Manual Override:** Uses an analog/digital video transmission system for direct pilot viewing and a 2.4GHz/900MHz RC receiver link that can interrupt autonomous mode (`GUIDED`) and revert to manual control (`STABILIZE` / `ACRO` / `POSHOLD`) instantly.


## Hardware Stack

| Subsystem | Component / Specification |
| :--- | :--- |
| **Airframe** | Custom lightweight carbon fiber quadcopter frame |
| **Compute Engine** | Raspberry Pi (Vision processing & high-level mission logic) |
| **Flight Control** | ArduPilot-compatible flight controller |
| **Sensors** | Onboard CSI/USB Camera, IMU, Barometer, GPS/Compass module |
| **Communication** | Serial/UART MAVLink bridge (Pi to FCU), RC receiver, FPV VTX |

# Authors

- [Rehan](https://stardance.hackclub.com/@rehanhabbu)
- [Sahlameer](https://stardance.hackclub.com/@Sahlameer)
- [Faahim](https://stardance.hackclub.com/@Faahim)


# Running Simulations with Isaac Sim, Pegasus, and ArduPilot SITL

This guide covers setting up, configuring, and running an autonomous multirotor simulation by bridging NVIDIA Isaac Sim on Windows with ArduPilot SITL inside WSL2.

---

## 1. Prerequisites (WSL2 & ArduPilot Setup)


## Note: May require an NVIDIA GPU with driver 560.94 for legacy support
## Note: Right Now this is for the default IRIS drone, will be updated when custom drone CAD is complete.

### Install and Configure WSL2
Open PowerShell as Administrator and install Ubuntu 22.04:
```powershell
wsl --install -d Ubuntu-22.04
```
Restart your computer if prompted, then launch the Ubuntu 22.04 terminal.

### Install ArduPilot SITL
Run the following inside your WSL terminal:
```bash
cd ~
git clone --recurse-submodules [https://github.com/ArduPilot/ardupilot.git](https://github.com/ArduPilot/ardupilot.git)
cd ardupilot
```

### Install Build Prerequisites
```bash
Tools/environment_install/install-prereqs-ubuntu.sh -y
```
Reload your environment variables:
```bash
. ~/.profile
```

### Build SITL for QuadCopter
```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py -w --clean
```
*(Press Ctrl + C once the build finishes and the MAVProxy prompt appears).*

---

## 2. Install Isaac Sim and Pegasus Simulator 5.1.0

1. [Download and Extract IssacSim 5.1.0](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/installation/download.html).
2. [Download and Extract Pegasus 5.1.0](https://github.com/PegasusSimulator/PegasusSimulator/releases/tag/v5.1.0).
3. Copy the extracted `PegasusSimulator` folder and paste it into your extracted `isaac-sim-standalone-5.1.0-windows-x86_64` directory.
4. Launch Isaac Sim by running `isaac-sim.bat`.
5. Add Pegasus Simulator to extensions:
   - Go to **Window** -> **Extensions**.
   - Click the settings icon (gear / three lines) next to the search bar.
   - Click the **+** icon to add a new extension search path.
   - Add the path to `PegasusSimulator/extensions` (e.g., `C:\Users\<username>\Downloads\isaac-sim-standalone-5.1.0-windows-x86_64\PegasusSimulator\extensions`).
   - Return to the Extensions list and search for **Pegasus**.
   - Toggle the Pegasus Simulator extension to enabled and check **Autoload**.

---

## 3. Configure the WSL2-to-Windows Network Bridge

### Patch ArduPilotPlugin.py
Open PowerShell and find the plugin file:
```powershell
$plugin = (Get-ChildItem -Path "$env:LOCALAPPDATA\ov\data\exts\v2\pegasus.simulator-*" -Recurse -Filter "ArduPilotPlugin.py").FullName
notepad $plugin
```

In `__init__`, change `self.fdm_address` to listen on all interfaces:
```python
self.fdm_address = '0.0.0.0'
```

In `receive_servo_packet()`, verify client IP auto-detection is present:
```python
data, (client_addr, client_out) = self.motor_control_sock.recvfrom(self.SERVO_PACKET_SIZE)
if self.fcu_address is None or self.fcu_port_out is None:
    self.fcu_address = client_addr
    self.fcu_port_out = client_out
```
Save (Ctrl + S) and close Notepad.

### Allow Inbound Simulation Ports in Windows Firewall
Run in PowerShell as Administrator:
```powershell
New-NetFirewallRule -DisplayName "Isaac Sim Pegasus Inbound" -Direction Inbound -LocalPort 9002,9003,14550 -Protocol UDP -Action Allow
```

---

## 4. Running the Simulation

Always follow this startup sequence:

### Step A: Start Isaac Sim & Load Vehicle (Windows)
1. Start Isaac Sim via `isaac-sim.bat`.
2. Go to **File** -> **New Stage**.
3. In the Pegasus Simulator tab (bottom-right panel):
   - Click **Load Scene** (e.g., Default Environment).
   - Set the vehicle dropdown to **Iris** and click **Load Vehicle**.
4. Click the **Play** button on the left toolbar to start the physics loop and listen on port 9002.

### Step B: Start ArduPilot SITL (WSL Ubuntu)
Get your current Windows virtual gateway IP:
```bash
grep nameserver /etc/resolv.conf | awk '{print $2}'
```

Start SITL (replace `172.30.32.1` with the IP returned above if different):
```bash
cd ~/ardupilot/ArduCopter
sim_vehicle.py -v ArduCopter -f json:172.30.32.1 --out=udp:172.30.32.1:14550 --console --map
```

---

## 5. Vehicle Configuration & Flight Commands

### One-Time Motor Configuration (In MAVProxy Terminal)
Run once to configure the quadrotor frame layout:
```text
param set FRAME_CLASS 1
param set FRAME_TYPE 1
```

### Arming and Autonomous Takeoff
Wait until the MAVProxy console shows `pre-arm good` and `GPS: OK`(Might take a while), then run:
```text
mode GUIDED
arm throttle
takeoff 5
```

### In-Flight Command Reference

| Action | MAVProxy Command |
| :--- | :--- |
| **Move Relative (X, Y, Z in meters)** | `position 10 0 0` *(moves 10m forward)* |
| **Change Hover Altitude** | `altitude 15` |
| **Return to Launch & Land** | `mode RTL` |
| **Immediate Vertical Land** | `mode LAND` |
| **Emergency Motor Stop** | `disarm` |
