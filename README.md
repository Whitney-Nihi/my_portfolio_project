# 3D Raycasting Game

## Project Description
This project is focused on creating a simple 3D game using **raycasting**, similar to early games like *Wolfenstein 3D*. The game will feature a basic player-controlled camera, walls, textures, and enemies as the development progresses.

The primary goal is to explore and implement key aspects of 3D rendering using the **SDL2** library, while applying raycasting techniques to simulate 3D environments.

## Features
- Create a window using **SDL2**
- Implement raycasting to render 3D walls from a 2D map
- Rotate the camera using keyboard inputs
- Move the player (camera) using `W`, `A`, `S`, `D` keys
- Handle player-wall collisions to prevent walking through walls
- Parse the map from a file and dynamically generate it
- Implement textures for walls, floors, and ceilings
- Optional features: rain, shadows, enemies, and weapons

## Project Structure
- **Walls**: Create a window using **SDL2** and render walls based on a 2D grid.
- **Orientation**: Render walls with different colors based on their orientation (NORTH/SOUTH and EAST/WEST).
- **Rotation**: Allow the player to rotate the camera using the keyboard.
- **Movement**: Implement movement using the `W`, `A`, `S`, `D` keys.
- **Collision Handling**: Prevent the player from walking through walls.

## Requirements
- **SDL2**: The project uses **SDL2** to create windows and handle input.
- **C++**: The project is written in **Python**.

