# Autonomous Path-Finding Robot Simulation

This project simulates an autonomous robot navigating a grid with safe, risky, and normal zones. It uses Dijkstra’s algorithm to find the shortest path to a randomly placed target while avoiding risky zones.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Controls](#controls)

## Features

- **Random Grid Generation**: The simulation generates a random grid with three types of zones: normal, safe, and risky.
- **Pathfinding Algorithm**: The robot utilizes Dijkstra’s algorithm to find the shortest path to a target while avoiding risky zones.
- **User Interaction**: Start the simulation and reconstruct the maze using buttons on the interface.
- **Dynamic Target**: The target position changes randomly when the maze is reconstructed.

## Installation

1. Ensure you have Python installed on your system. This project was developed using Python 3.x.
2. Install the required libraries:
   ```bash
   pip install pygame

## How It Works

1. **Grid Generation**: 
   - The simulation creates a grid composed of various zones: 
     - **Normal Zones**: Areas where the robot can move freely.
     - **Safe Zones**: Areas that are safe for the robot to traverse.
     - **Risky Zones**: Areas that should be avoided by the robot due to potential hazards.

2. **Robot Initialization**:
   - The robot starts at the top-left corner of the grid and is assigned a randomly generated target position within the grid.

3. **Pathfinding with Dijkstra's Algorithm**:
   - When the simulation starts, Dijkstra’s algorithm calculates the shortest path from the robot's starting position to the target position, taking into account the types of zones. 
   - The algorithm avoids risky zones to ensure safe navigation.

4. **User Interaction**:
   - The user can start the simulation by clicking the **Start Button**. If the robot successfully reaches the target, the simulation displays the path length and a success message.
   - If the robot encounters a scenario where no valid path exists, a message is displayed, prompting the user to reconstruct the maze with a new target.

5. **Dynamic Target**:
   - When the user clicks the **Reconstruct Button**, the simulation generates a new grid and target position, allowing the robot to attempt navigation again.


## Usage

1. **Clone this repository**:
   ```bash
   git clone https://github.com/sumanthd032/robot-pathfinding-simulation.git
   cd robot-pathfinding-simulation

2. **Run the simulation**:
    python main.py
