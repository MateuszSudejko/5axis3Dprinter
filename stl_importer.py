import numpy as np
from stl import mesh
import os


class STLImporter:
    def __init__(self, filename):
        self.filename = filename
        self.mesh = None
        self.vertices = None
        self.facets = None
        self.normals = None

    def load_stl(self):
        """Load an STL file and extract its geometric data"""
        if not os.path.exists(self.filename):
            print(f"File not found: {self.filename}")
            return False

        try:
            self.mesh = mesh.Mesh.from_file(self.filename)

            # Extract vertices, facets and normals
            self.vertices = self.mesh.vectors.reshape(-1, 3)
            self.vertices = np.unique(self.vertices, axis=0)
            self.facets = self.mesh.vectors
            self.normals = self.mesh.normals

            print(f"Loaded STL with {len(self.facets)} facets and {len(self.vertices)} unique vertices")
            return True
        except Exception as e:
            print(f"Error loading STL file: {e}")
            return False

    def get_mesh_stats(self):
        """Return basic statistics about the loaded mesh"""
        if self.mesh is None:
            return None

        stats = {
            "facet_count": len(self.facets),
            "vertex_count": len(self.vertices),
            "dimensions": {
                "x": [float(self.vertices[:, 0].min()), float(self.vertices[:, 0].max())],
                "y": [float(self.vertices[:, 1].min()), float(self.vertices[:, 1].max())],
                "z": [float(self.vertices[:, 2].min()), float(self.vertices[:, 2].max())]
            },
            "volume": float(self.mesh.get_mass_properties()[0])
        }
        return stats
