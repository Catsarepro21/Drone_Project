# Autonomous Vision + FPV Quad

Building a carbon-fiber quad that does both: manual FPV flights and autonomous target following. We have a Pi 5 running onboard YOLO to track targets, and it sends position targets to a Cube Orange running ArduPilot. We also added the ability to control manually via FPV

BOM & weight calculations live here: https://docs.google.com/spreadsheets/d/1xU_NW1MB9JgXXCRr1vzQk_ZqJNn86JdCjggnNsJFE8U/edit?usp=sharing
Wiring Diagram: https://app.cirkitdesigner.com/project/11a8d37d-fc97-4505-8930-f4c5d81e814d

### What does what

- **Cube Orange+ (ArduPilot):** Handles the raw flight stabilization, motor mixing, and compass/GPS telemetry. It accepts velocity commands from the Pi over serial.
- **Raspberry Pi 5 (8GB):** Captures CSI video, processes YOLO inference onboard, and pushes MAVLink setpoints over UART to TELEM2.
- **Herelink v1.1:** Feeds twin HDMI streams (forward GoPro 6, downward SJCAM) back to the ground unit. Total overkill for this drone, but we already have it lying around so we're using it.
- **Failsafe override:** Mapped a physical switch on the Herelink RC to instantly kick the flight controller from GUIDED mode back into POSHOLD or STABILIZE.

### Power setup

We had to split the battery rails completely because the motors will brown out the Pi during heavy throttle punches:

1. **4S LiPo (Motors):** Feeds into the Cube Power Brick Mini, through the PDB, out to four 80A BLHeli_S ESCs running 2820 1000kV motors.
2. **3S LiPo (Avionics):** Runs through an anti-spark switch into an XT60 hub. An iFlight PD100W drops this to a clean 5V/5A USB-C line for the Pi 5. A Matek BEC steps down to 12V for the Herelink air unit, while the auxiliary USB port powers the action cameras.

### Parts list

- **Frame:** Carbon fiber quadcopter frame
- **Flight Controller:** CubePilot Cube Orange+ (ArduPilot)
- **Companion Board:** Raspberry Pi 5 (8GB)
- **Drive:** 4x 2820 1000kV motors, 4x 80A BLHeli_S ESCs
- **Batteries:** 4S LiPo for motors, 3S LiPo for avionics
- **CV Cameras:** Sony IMX708 (front CSI-1), Arducam OV5647 fisheye (downward CSI-0)
- **Pilot Cameras:** GoPro Hero 6 (front HDMI-1), SJCAM SJ4000 (downward HDMI-2)
- **Sensors & Radio:** Holybro Micro M10 GPS/Mag, CubePilot Herelink Air Unit v1.1

### Simulation

Running flight dynamics and vision tests inside NVIDIA Isaac Sim via Pegasus. Setup notes here: https://pegasussimulator.github.io/PegasusSimulator/source/setup/installation.html (Not well on windows).

### Authors
- Rehan (https://stardance.hackclub.com/@rehanhabbu)
- Sahlameer (https://stardance.hackclub.com/@Sahlameer)
- Faahim (https://stardance.hackclub.com/@Faahim)
