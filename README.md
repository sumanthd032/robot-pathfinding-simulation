# Autonomous Path-Finding Robot Simulation

This project simulates an autonomous robot navigating a grid with safe, risky, and normal zones. It uses Dijkstra’s algorithm to find the shortest path to a randomly placed target while avoiding risky zones.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Controls](#controls)
- [Contributing](#contributing)
- [License](#license)

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
