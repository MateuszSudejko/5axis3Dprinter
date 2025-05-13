import math


class InverseKinematics:
    def __init__(self, oriented_paths):
        self.oriented_paths = oriented_paths
        self.gcode_paths = []

    def calculate_axis_positions(self):
        """Map toolpath points with orientations to 5-axis positions"""
        for z, path, orientations in self.oriented_paths:
            layer_commands = []

            for i, (point, orientation) in enumerate(zip(path, orientations)):
                x, y = point
                ix, iy, iz = orientation

                # For MVP, set A and B to 0 (vertical orientation)
                # In future versions, calculate A and B from orientation vector
                a_angle = 0
                b_angle = 0

                # Create position dictionary with all 5 axes
                position = {
                    'X': float(x),
                    'Y': float(y),
                    'Z': float(z),
                    'A': float(a_angle),
                    'B': float(b_angle)
                }

                layer_commands.append(position)

            self.gcode_paths.append((z, layer_commands))

        return self.gcode_paths
