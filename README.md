# 🤖 Reception Bot — ROS2 Gazebo Simulation

A fully simulated **autonomous reception robot** built with ROS2 Humble and Gazebo Classic. The robot navigates an industrial office environment, detects visitors using a camera, scans surroundings with a LiDAR, builds a map using SLAM, and autonomously navigates to predefined waypoints such as the reception desk, waiting area, and meeting room.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Hardware Design](#hardware-design)
- [Package Structure](#package-structure)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [SLAM Mapping](#slam-mapping)
- [Autonomous Navigation](#autonomous-navigation)
- [Simulation Environment](#simulation-environment)
- [Sensors](#sensors)
- [Real Robot Deployment](#real-robot-deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🧩 Project Overview

The **Reception Bot** is a differential-drive mobile robot designed to operate in office and industrial environments. It is capable of:

- Autonomously navigating to reception, waiting, and meeting areas
- Building a real-time map of its environment using SLAM
- Detecting obstacles and planning collision-free paths
- Streaming live camera feed for visitor interaction
- Scanning the environment with a 360° LiDAR sensor

This project covers the **complete robotics stack** — from URDF modeling and Gazebo simulation to SLAM and Nav2-based autonomous navigation — making it a strong foundation for deploying a real physical reception robot.

---

## ✨ Features

- ✅ Full URDF/Xacro robot model with base, torso, head, wheels, LiDAR, and camera
- ✅ Gazebo Classic simulation with industrial office world
- ✅ Differential drive plugin for realistic wheel control
- ✅ 360° LiDAR sensor (simulated RPLIDAR A2)
- ✅ RGB Camera sensor on robot head
- ✅ SLAM Toolbox integration for real-time mapping
- ✅ Nav2 navigation stack for autonomous waypoint navigation
- ✅ RViz2 visualization for map, robot model, laser scan, and path
- ✅ Programmatic goal sending to named waypoints
- ✅ Industrial office environment with walls, desk, chairs, dividers, and pillars

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│              Reception Bot Stack                │
│                                                 │
│  URDF/Xacro ──► Gazebo Simulation              │
│       │               │                         │
│       │         ┌─────┴──────┐                 │
│       │         │  Sensors   │                  │
│       │    LiDAR/scan   Camera/image_raw        │
│       │         │                               │
│       ▼         ▼                               │
│  robot_state_publisher                          │
│       │         │                               │
│       │    SLAM Toolbox ──► /map topic          │
│       │         │                               │
│       └────►  Nav2  ◄─── Goal Poses            │
│              │                                  │
│         cmd_vel ──► Differential Drive          │
└─────────────────────────────────────────────────┘
```

---

## 🔧 Hardware Design

This simulation is designed to mirror a real physical robot with the following specifications:

### Chassis
| Property | Value |
|---|---|
| Base dimensions | 600mm × 400mm × 300mm |
| Material | Aluminium 6061 (3mm sheet) |
| Total weight | ~10 kg |

### Drive System
| Component | Specification |
|---|---|
| Drive wheels | 200mm diameter rubber wheels |
| Motors | 12V DC Geared Motor, 150–200 RPM, 25 kg·cm torque |
| Encoder | 500 PPR quadrature encoder |
| Motor driver | Cytron MDD10A (10A per channel) |
| Caster wheel | 50mm ball caster (front support) |

### Power System
| Component | Specification |
|---|---|
| Battery | 24V 20Ah LiFePO4 |
| BMS | 24V 20A Battery Management System |
| Voltage regulators | 24V→12V and 12V→5V DC-DC buck converters |
| Estimated runtime | ~1.3 hours continuous operation |

### Sensors
| Sensor | Model | Purpose |
|---|---|---|
| LiDAR | RPLIDAR A2 (simulated) | SLAM + obstacle detection |
| Camera | Intel RealSense D435 (simulated) | Visitor detection + tracking |

### Computing
| Option | Model | Use Case |
|---|---|---|
| Recommended | NVIDIA Jetson Nano 4GB | Navigation + camera AI |
| Budget | Raspberry Pi 4 8GB | Basic navigation |
| High performance | Intel NUC i5/i7 | Full stack smoothly |

---

## 📁 Package Structure

```
reception_bot/
├── urdf/
│   └── reception_bot.urdf.xacro     # Full robot description
├── worlds/
│   └── office_world.world           # Gazebo industrial environment
├── launch/
│   ├── gazebo.launch.py             # Spawn robot in Gazebo
│   ├── slam.launch.py               # Start SLAM mapping
│   └── navigation.launch.py         # Start Nav2 navigation
├── config/
│   ├── slam_params.yaml             # SLAM Toolbox parameters
│   └── nav2_params.yaml             # Nav2 stack parameters
├── maps/
│   ├── office_map.pgm               # Saved occupancy grid map
│   └── office_map.yaml              # Map metadata
├── scripts/
│   └── goal_sender.py               # Autonomous waypoint navigation
├── rviz/
│   └── reception_bot.rviz           # RViz2 configuration
├── CMakeLists.txt
└── package.xml
```

---

## 📦 Dependencies

- ROS2 Humble Hawksbill
- Gazebo Classic 11
- `ros-humble-gazebo-ros-pkgs`
- `ros-humble-gazebo-plugins`
- `ros-humble-slam-toolbox`
- `ros-humble-nav2-bringup`
- `ros-humble-robot-state-publisher`
- `ros-humble-joint-state-publisher`
- `ros-humble-xacro`
- `ros-humble-image-transport`
- `ros-humble-cv-bridge`

---

## ⚙️ Installation

### 1. Install ROS2 Humble
Follow the official guide: https://docs.ros.org/en/humble/Installation.html

### 2. Install dependencies

```bash
sudo apt update
sudo apt install -y \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-plugins \
  ros-humble-slam-toolbox \
  ros-humble-nav2-bringup \
  ros-humble-robot-state-publisher \
  ros-humble-joint-state-publisher \
  ros-humble-xacro \
  ros-humble-image-transport \
  ros-humble-cv-bridge \
  python3-colcon-common-extensions
```

### 3. Clone and build

```bash
mkdir -p ~/reception_ws/src
cd ~/reception_ws/src
git clone https://github.com/YOUR_USERNAME/reception_bot.git
cd ~/reception_ws
colcon build --symlink-install
source install/setup.bash
```

### 4. Add to bashrc (optional but recommended)

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/reception_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 🚀 Usage

### Step 1 — Launch Gazebo Simulation

```bash
ros2 launch reception_bot gazebo.launch.py
```

This opens Gazebo with the office world and spawns the reception bot.

### Step 2 — Launch SLAM for Mapping

Open a new terminal:

```bash
source ~/reception_ws/install/setup.bash
ros2 launch reception_bot slam.launch.py
```

### Step 3 — Teleoperate to Build the Map

Open another terminal:

```bash
source ~/reception_ws/install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args --remap cmd_vel:=/reception_bot/cmd_vel
```

Drive the robot around the entire office environment using keyboard controls:
- `i` — move forward
- `,` — move backward
- `j` — turn left
- `l` — turn right
- `k` — stop

---

## 🗺️ SLAM Mapping

Once you have driven around the full office and the map looks complete in RViz2, save it:

```bash
mkdir -p ~/reception_ws/src/reception_bot/maps
ros2 run nav2_map_server map_saver_cli \
  -f ~/reception_ws/src/reception_bot/maps/office_map
```

This saves two files:
- `office_map.pgm` — the occupancy grid image
- `office_map.yaml` — map resolution and origin metadata

---

## 🧭 Autonomous Navigation

### Step 1 — Launch Gazebo

```bash
ros2 launch reception_bot gazebo.launch.py
```

### Step 2 — Launch Nav2 with saved map

```bash
ros2 launch reception_bot navigation.launch.py \
  map:=$HOME/reception_ws/src/reception_bot/maps/office_map.yaml
```

### Step 3 — Set Initial Pose in RViz2

1. Open RViz2
2. Click **2D Pose Estimate**
3. Click on the map where the robot is and drag to set orientation

### Step 4 — Send Navigation Goals

**Option A — RViz2:** Click **Nav2 Goal** and click destination on map

**Option B — Programmatically:**

```bash
python3 ~/reception_ws/src/reception_bot/scripts/goal_sender.py
```

### Predefined Waypoints

| Location | X | Y | Yaw |
|---|---|---|---|
| Reception desk | 0.0 | 6.0 | 180° |
| Waiting area | -6.0 | 6.0 | 0° |
| Meeting room | 7.0 | -5.0 | 90° |
| Home | 0.0 | 0.0 | 0° |

---

## 🏢 Simulation Environment

The Gazebo world (`office_world.world`) contains a realistic industrial office layout:

| Object | Description |
|---|---|
| Outer walls | 20m × 20m enclosed office space |
| Reception desk | Large wooden desk at y=7 |
| Office dividers | Partition walls dividing work areas |
| Waiting table | Table with chairs in waiting area |
| Pillars | Two structural pillars |
| Ground plane | Flat textured floor |

---

## 📡 Sensors

### LiDAR (`/reception_bot/scan`)
- Type: `sensor_msgs/LaserScan`
- Range: 0.15m – 12.0m
- Scan angle: 360°
- Update rate: 10 Hz
- Used for: SLAM mapping + obstacle avoidance

### Camera (`/reception_bot/front_camera/image_raw`)
- Type: `sensor_msgs/Image`
- Resolution: 640 × 480
- Update rate: 30 FPS
- FOV: 80°
- Used for: Visitor detection + person tracking

### Odometry (`/reception_bot/odom`)
- Type: `nav_msgs/Odometry`
- Source: Differential drive plugin
- Used for: Localization + SLAM

---

## 🔄 Real Robot Deployment

Since the full ROS2 stack is used in simulation, deploying to a real robot requires only swapping the Gazebo driver nodes with real hardware drivers:

```bash
# Replace gazebo.launch.py with real_robot.launch.py containing:

# RPLIDAR A2
ros2 run rplidar_ros rplidar_node \
  --ros-args -p serial_port:=/dev/ttyUSB0

# Intel RealSense Camera
ros2 launch realsense2_camera rs_launch.py

# Motor controller via serial/CAN bridge
ros2 run ros2_serial serial_node
```

The SLAM and Navigation launch files remain **completely unchanged** when moving from simulation to real hardware — this is the key advantage of ROS2.

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 👤 Author

**Gohar**
- GitHub: https://github.com/Mechtech-Juniors
  

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Nav2 Navigation Stack](https://navigation.ros.org/)
- [SLAM Toolbox](https://github.com/SteveMacenski/slam_toolbox)
- [Gazebo Classic](http://gazebosim.org/)
- [Open Source Robotics Foundation](https://www.openrobotics.org/)
