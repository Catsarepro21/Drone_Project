# Autonomous Vision + FPV Quad

A hybrid carbon-fiber drone combining manual FPV controls with Raspberry Pi 5 onboard YOLO tracking and ArduPilot target following.
<img width="3000" height="2294" alt="circuit_image" src="https://github.com/user-attachments/assets/814ffa7c-f512-4c04-ae4e-5bf58a9150ad" />

[https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d](https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d))

## Try It

* **Wiring Diagram:** [Cirkit Designer View](https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d)
* **BOM & Weight Calc:** [Google Sheet Breakdown](https://docs.google.com/spreadsheets/d/1xU_NW1MB9JgXXCRr1vzQk_ZqJNn86JdCjggnNsJFE8U/edit?usp=sharing)

## Quick Start

1. Flash ArduPilot (Copter) onto the Cube Orange+ and calibrate the IMU/compass.
2. Boot the Raspberry Pi 5 and clone the onboard vision repository:
   ```bash
   git clone https://github.com/your-username/drone-vision.git && cd drone-vision
   ```
3. Connect the Pi 5 to TELEM2 and run the autonomous tracking script:
   ```bash
   python3 main.py --port /dev/ttyAMA0 --baud 921600
   ```

## Features

* Real-time target tracking via onboard YOLO inference running on a Raspberry Pi 5 over CSI.
* Automatic velocity and position command adjustments pushed to ArduPilot via MAVLink over serial (TELEM2).
* Dual HD video feed transmission (front GoPro Hero 6 & downward SJCAM) through Herelink v1.1.
* Dual power rail architecture designed to completely prevent Pi brownouts during heavy throttle spikes.
* Physical RC transmitter failsafe override to instantly revert from `GUIDED` mode to `POSHOLD` or `STABILIZE`.

## Local Simulation

1. Install [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim) (Linux environment recommended).
2. Follow the setup steps in the [Pegasus Simulator Installation Guide](https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html).
3. Run the simulation environment to test flight dynamics and CV tracking algorithms:
   ```bash
   python3 pegasus_sim.py --config quad_yolo.yaml
   ```

## How It Works

To solve the issue where high motor current draws caused voltage sags and browned out the Raspberry Pi 5 during intense maneuvers, we completely separated the avionics and drive power rails. A primary 4S LiPo supplies the ESCs and 2820 1000kV motors, while a secondary 3S LiPo feeds an iFlight PD100W regulator to deliver a clean, continuous 5V/5A over USB-C to the companion computer.

## Authors & Acknowledgements

* **Authors:** [Rehan](https://stardance.hackclub.com/@rehanhabbu), [Sahlameer](https://stardance.hackclub.com/@Sahlameer), [Faahim](https://stardance.hackclub.com/@Faahim)
* **Open Source Tools:** [ArduPilot](https://ardupilot.org/), [Pegasus Simulator](https://pegasussimulator.github.io/PegasusSimulator/)
