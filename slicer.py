import numpy as np
from stl import mesh


class PlanarSlicer:
    def __init__(self, stl_importer, layer_height=0.2):
        self.mesh = stl_importer.mesh
        self.layer_height = layer_height
        self.z_min = np.min(self.mesh.vectors[:, :, 2])
        self.z_max = np.max(self.mesh.vectors[:, :, 2])
        self.layers = []

    def slice(self):
        """Perform planar slicing along Z-axis"""
        current_z = self.z_min + self.layer_height / 2
        while current_z <= self.z_max:
            layer_contours = self._get_layer_contours(current_z)
            if layer_contours:
                self.layers.append((current_z, layer_contours))
            current_z += self.layer_height

    def _get_layer_contours(self, z):
        """Calculate intersection points for a given Z height"""
        contours = []
        for triangle in self.mesh.vectors:
            intersections = []

            # Check all 3 edges of the triangle
            for i in range(3):
                p1 = triangle[i]
                p2 = triangle[(i + 1) % 3]

                if (p1[2] - z) * (p2[2] - z) < 0:  # Edge crosses plane
                    t = (z - p1[2]) / (p2[2] - p1[2])
                    x = p1[0] + t * (p2[0] - p1[0])
                    y = p1[1] + t * (p2[1] - p1[1])
                    intersections.append((x, y))

            # Store pairs of intersection points
            if len(intersections) == 2:
                contours.append(intersections)

        return contours

    def export_contours(self, filename):
        """Export layer contours to file"""
        with open(filename, 'w') as f:
            for z, contours in self.layers:
                f.write(f"Layer Z={z:.3f}\n")
                for contour in contours:
                    f.write(f"  Segment: {contour[0]} -> {contour[1]}\n")
