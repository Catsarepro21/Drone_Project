# Autonomous Vision + FPV Quad

A hybrid carbon-fiber drone combining manual FPV controls with Raspberry Pi 5 onboard YOLO tracking and ArduPilot target following.
<img width="3000" height="2294" alt="circuit_image" src="https://github.com/user-attachments/assets/814ffa7c-f512-4c04-ae4e-5bf58a9150ad" />

[https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d](https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d))
<img width="2463" height="1316" alt="1 (1)" src="https://github.com/user-attachments/assets/9f4f4043-a559-46b1-b459-15c97b5c67fb" />


## Try It

* **Wiring Diagram:** [Cirkit Designer View](https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d)
* **BOM & Weight Calc:** [Google Sheet Breakdown](https://docs.google.com/spreadsheets/d/1xU_NW1MB9JgXXCRr1vzQk_ZqJNn86JdCjggnNsJFE8U/edit?usp=sharing)
## Quick Start

1. **Flash Flight Controller:** Upload ArduPilot (Copter firmware) onto the Cube Orange+ and calibrate IMU/compass.
2. **Setup Companion Computer:** Clone this repository onto the onboard Raspberry Pi 5 (8GB):
   ```bash
   git clone [https://github.com/Catsarepro21/Drone_Project.git](https://github.com/Catsarepro21/Drone_Project.git)
   cd Drone_Project

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

Has both a FPV and an Autonomous mode powered by different controllers. To solve the issue where high motor current draws caused voltage sags and browned out the Raspberry Pi 5 during intense maneuvers, we completely separated the avionics and drive power rails. A primary 4S LiPo supplies the ESCs and 2820 1000kV motors, while a secondary 3S LiPo feeds an iFlight PD100W regulator to deliver a clean, continuous 5V/5A over USB-C to the companion computer.

## Authors & Acknowledgements

* **Authors:** [Rehan](https://stardance.hackclub.com/@rehanhabbu), [Sahlameer](https://stardance.hackclub.com/@Sahlameer), [Faahim](https://stardance.hackclub.com/@Faahim)
* **Open Source Tools:** [ArduPilot](https://ardupilot.org/), [Pegasus Simulator](https://pegasussimulator.github.io/PegasusSimulator/)


BOM:
| Quantity | Component Category | Item Name / Model | Est. Price (USD) | Purchase Link | Notes | Buy | Have |
|---:|:---|:---|:---|:---|:---|:---|:---|
| 1 | Flight Controller | CubePilot Cube Orange+ | $279.00 | [Link](https://www.getfpv.com/cubepilot-the-cube-orange.html) | Primary flight controller & autopilot | True | False |
| 1 | Flight Controller(Alternate) | CubePilot Cube Orange+ | $235.00 | [Link](https://ebay.com/used) | | True | False |
| 1 | Companion Computer | Raspberry Pi 5 - 8gb | $175.00 | [Link](https://www.canakit.com/raspberry-pi-5-8gb.html) | High-level vision processing & MAVLink control | False | True |
| 1 | Pi Front Camera Module | Sony IMX708 | $34.95 | [Link](https://www.canakit.com/raspberry-pi-camera-module-3.html) | Low-latency FPV / target tracking camera | True | False |
| 1 | Pi Down Camera Module | Arducam 5MP OV5647 | $28.99 | [Link](https://www.arducam.com/arducam-ultra-wide-angle-fisheye-5mp-ov5647-camera-for-raspberry-pi.html) | 220HFOV for Downward Facing Cam Detection | True | False |
| 1 | Streaming Cam Front | Go-Pro Hero 6 | $199.51 | [Link](https://www.walmart.com/ip/GoPro-HERO6-Black-4K-Action-Video-Camera/970674173) | 135FOV for streaming to controller | False | True |
| 1 | Streaming Cam Down | SJCAM SJ4000 | $55.99 | [Link](https://www.amazon.com/dp/B09GB1LN8V) | 170HFOV for streamign to controller | True | False |
| 1 | Air Unit / Telemetry | CubePilot HereLink HD Air Unit V1.1 | $851.58 | [Link](https://www.readymaderc.com/products/details/proficnc-herelink-air-unit) | HD video & MAVLink control link | False | True |
| 1 | GPS / Compass | Micro M10 GPS | $27.99 | [Link](https://holybro.com/products/micro-m10-gps?variant=42981482922173) | High-precision DroneCAN GPS/Mag - With Case and IST8310 | True | False |
| 1 | Main Battery | OVONIC 4S LiPo Battery 14.8V 6500mAh | $55.99 | [Link](https://www.amazon.com/dp/B0CP5GJM78) | 14.8V main power supply (NOTE: This is a 2-pack) | True | False |
| 3 | Electronics Battery | 3S 5000mAh 50C LiPo | $37.99 | [Link](https://hrb-power.com/products/11-1v-5000mah-6000mah-50c-trx) | Battery to power Auton Electronic Components | False | True |
| 1 | Power Distribution Board | Matek Systems PDB XT60 W | $0.99 | [Link](https://www.aliexpress.us/item/3256806070552817.html) | PDB for battery to ESC Transfer | True | False |
| 4 | ESC/s | BLHeli_S Series ESC 80A | $14.39 | [Link](https://www.aliexpress.us/item/3256811813844941.html) | Used to turn the Brushless motors, Rated for 80+ Amps ONLY | True | False |
| 4 | Brushless Motors | Skywalker 2820 SL motor -- 1000KV | $39.99 | [Link](https://www.hobbywingdirect.com/products/skywalker-2820-sl-motor?variant=41165095370867) | Quadcopter propulsion motors - ≤1000KV ONLY | True | False |
| 1 | Switch | XT60 Anti-Spark Electronic Switch | $9.17 | [Link](https://www.aliexpress.us/item/3256811379155381.html) | ONLY FOR AUTON ELECTRONICS | True | False |
| 1 | Power Module | Cube Power Brick Mini | $34.00 | [Link](https://nwblue.com/products/power-brick-mini?variant=42739874463897) | Current sensing & Cube power input | True | False |
| 1 | XT60 Splitter + USB | STRIX XT60 Power Hub with USB | $8.39 | [Link](https://www.aircraftpaintmasks.com/product/strix-xt60-power-hub-with-usb) | For Splitting xt60 and for usb power | True | False |
| 1 | XT60 USB converter | IFlight PD100W Adapter | $21.73 | [Link](https://www.aliexpress.us/item/3256808471582717.html) | For stable power to Go-Pro and Rpi-5 | True | False |
| 1 | XT60 USB converter | XT60 Plug to USB 5V Charger Converter Module Adapter | $9.99 | [Link](https://www.amazon.com/dp/B09BKWR4PP) | Power Source for SJ4k | True | False |
| 1 | Voltage Regulators | MATEK BEC12S-PRO | $14.08 | [Link](https://www.aliexpress.us/item/3256811890826612.html) | Clean voltage step-down for Herelink HD Air Unit | True | False |
| 1 | Ground Station | CubePilot HereLink Controller | $3,699.00 | [Link](https://irlock.com/collections/herelink) | Ground control transmitter & HD receiver | False | True |
| 1 | Propellers CCW | HQProp 12x4.5 CCW Propeller 2 PCS | $7.60 | [Link](https://www.readymaderc.com/products/details/85966-hq-prop-12x4-5-ccw) | HQProp 12x4.5 CCW Propeller 2 PCS -- 12in heavy lift | True | False |
| 1 | Propellers CW | HQProp 12x4.5 CW Pusher Propeller 2PCS | $3.80 | [Link](https://www.readymaderc.com/products/details/85965-hq-prop-12x4-5-cw) | HQProp 12x4.5 CW Propeller 2 PCS -- 12in heavy lift | True | False |
| 1 | Lock Nuts | Uxcell Nylon Insert Hex Lock Nuts | $6.60 | [Link](https://www.harfington.com/products/p-1794642?variant=48267773640953) | For Bushless motor threads so the props dont fall of in flight | True | False |
| 1 | Quad Copter Frame | Flyroun New F680 all carbon fiber | $65.27 | [Link](https://www.aliexpress.us/item/3256811746043574.html) | The Backbone of the Drone | True | False |
| 1 | AI Accelerator for PI | Ai Hat+ 26TOPS | $109.00 | [Link](https://www.microcenter.com/product/687348/product) | Maybe get it type item - if budget wills --For Extra Neural Processing | False | False |
| 1 | RGB Strip | 5V SK6812 RGB COB/FOB LED Strip Addressable | $7.18 | [Link](https://www.aliexpress.us/item/2255799861654620.html) | 🥀 144leds/m 0.5 black pcb ip67 waterproof | True | False |
| 1 | RGB Enclosure | Black 1m Aluminum enclosure with diffuser | $20.00 | [Link](https://www.amazon.com/dp/B07KBYQ3JR) | | True | False |

