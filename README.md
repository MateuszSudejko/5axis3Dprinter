# 5 axis 3D printer
## Phase 1: Core MVP (Essential Functionality)
1. STL Import & Validation	- Use existing STL parser. Basic mesh validation (no watertight checks). Skip advanced repair or orientation logic.
2. Planar Slicing	- Implement basic planar slicing (Z-axis layers). Export slice contours.	Use traditional slicing; skip curved/conformal layers.
3. Basic Toolpath Generation	- Generate perimeters and infill for planar layers. Assign fixed nozzle orientation (e.g., always vertical).	No surface-normal-based orientation or segmentation.
4. Simplified Inverse Kinematics	- Hardcode rotational axes (e.g., A/B rotations fixed at 0°). Map (X, Y, Z) to linear axes only.	Ignore collisions; assume rotations are safe.
5. G-code Generation	- Output linear moves (G1) with X/Y/Z positions. Add placeholder commands for rotations (e.g., A0 B0).
## Phase 2: Enable Basic 5-Axis Functionality
1. Dynamic Nozzle Orientation	- Compute surface normals for toolpath points. Map normals to rotational axes (A/B).
2. Kinematics Integration	- Implement inverse kinematics for printer’s geometry (e.g., rotary vs. tilting axes). Convert nozzle orientation (I, J, K) to A/B angles.
3. Basic G-code with Rotations	- Replace placeholders with real A/B axis commands. Add linear interpolation for simultaneous motion (G1 X Y Z A B).
## Phase 3: Post-MVP Enhancements
1. Collision Avoidance	Add checks for toolhead/buildplate collisions during rotations.
2. Non-Planar Slicing	Implement curved/conformal layers.
3. Extrusion & Speed Control	Calibrate E-steps, retraction, and feedrate.
4. Path Optimization	Minimize travel moves and redundant rotations.
