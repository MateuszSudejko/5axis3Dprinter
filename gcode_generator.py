class GcodeGenerator:
    def __init__(self, kinematics_paths, feed_rate=1000, extrusion_multiplier=1.0):
        self.paths = kinematics_paths
        self.feed_rate = feed_rate
        self.extrusion_multiplier = extrusion_multiplier
        self.gcode = []

    def generate_gcode(self):
        """Generate G-code from 5-axis toolpaths"""
        # Add header
        self.gcode.append("; 5-Axis G-code generated for 3D printer")
        self.gcode.append("G21 ; Set units to millimeters")
        self.gcode.append("G90 ; Use absolute coordinates")
        self.gcode.append("M82 ; Use absolute distances for extrusion")
        self.gcode.append("G28 ; Home all axes")
        self.gcode.append(f"M104 S200 ; Set extruder temperature")
        self.gcode.append(f"M109 S200 ; Wait for extruder temperature")
        self.gcode.append(f"M140 S60 ; Set bed temperature")
        self.gcode.append(f"M190 S60 ; Wait for bed temperature")

        # Process each layer
        e_position = 0.0  # Track extrusion amount

        for z, commands in self.paths:
            self.gcode.append(f"; Layer at Z={z:.3f}")

            # Move to starting position of layer
            if commands:
                first_pos = commands[0]
                self.gcode.append(
                    f"G0 X{first_pos['X']:.3f} Y{first_pos['Y']:.3f} Z{z + 0.5:.3f} A{first_pos['A']:.3f} B{first_pos['B']:.3f} F{self.feed_rate}")
                self.gcode.append(f"G0 Z{z:.3f}")

            # Process each point in the layer
            prev_pos = None
            for pos in commands:
                if prev_pos:
                    # Calculate extrusion amount based on distance
                    dist = self._calculate_distance(prev_pos, pos)
                    e_position += dist * self.extrusion_multiplier

                    # Generate G1 command with all 5 axes
                    self.gcode.append(f"G1 X{pos['X']:.3f} Y{pos['Y']:.3f} Z{pos['Z']:.3f} "
                                      f"A{pos['A']:.3f} B{pos['B']:.3f} "
                                      f"E{e_position:.4f} F{self.feed_rate}")
                prev_pos = pos

            # Retract and move up after layer
            e_position -= 1.0  # Retraction
            self.gcode.append(f"G1 E{e_position:.4f} F1800 ; Retract")
            self.gcode.append(f"G0 Z{z + 0.5:.3f} ; Move up")

        # Add footer
        self.gcode.append("G0 X0 Y0 ; Move to origin")
        self.gcode.append("M104 S0 ; Turn off extruder")
        self.gcode.append("M140 S0 ; Turn off bed")
        self.gcode.append("M84 ; Disable motors")

        return self.gcode

    def save_gcode(self, filename):
        """Save G-code to file"""
        with open(filename, 'w') as f:
            for line in self.gcode:
                f.write(line + '\n')

    def _calculate_distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return ((p1['X'] - p2['X']) ** 2 + (p1['Y'] - p2['Y']) ** 2 + (p1['Z'] - p2['Z']) ** 2) ** 0.5
