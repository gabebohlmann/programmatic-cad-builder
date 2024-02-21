# Voxel Assembly Python Script

## TODO
1. Add build123d code for hook
1. Add argument to export function to specify .STEP or .STL

## Overview
This Python script leverages the CadQuery library to create and assemble 3D models of voxels. It includes functionality for creating individual voxels, a series of voxels with varying sizes, and for recursively assembling multiple voxels using a hook and socket system.

## Requirements
- Python 3 
   - Python 3.10 works well but there are dependency issues on Python > v3.10
- CadQuery library
- Build123d library
- ocp_vscode library

## Installation
1. Install VS Code
- https://code.visualstudio.com/download

1. Install OCP CAD Viewer extension for VS Code
- https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-cad-viewer


Install the required libraries using `pip`:

```bash
pip install cadquery
pip install build123d
pip install ocp_vscode
```

## Usage
1. Set the voxel parameters at the bottom of the script.
2. Execute the desired function calls to generate CAD models:
   - Single voxels
   - Series of voxels
   - Two-voxel assembly
   - Recursive voxel assembly
3. CAD models are exported as .STEP and/or .STL files.

## Functions
- `create_voxel`: Generates a single voxel.
- `export_assy`: Exports assemblies to .STEP and .STL.
- `create_voxels`: Generates a series of voxels.
- `connect_voxels`: Forms an assembly from two voxels.
- `chain_voxels_recursive`: Creates and connects multiple voxels in a chain.

## Parameters
- `s_i`: Inside side length of the hollow cube.
- `d_i`: Inside diameter of the plug cylinder.
- `t_b`: Wall thickness of the cube.
- `t_c`: Wall thickness of the cylinder.
- `h_c`: Height the cylinder extends from the cube's inside.

## Contributing
Please submit pull requests for contributions.
