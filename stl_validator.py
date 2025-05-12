import numpy as np


class STLValidator:
    def __init__(self, importer):
        self.importer = importer
        self.validation_results = {}

    def validate_mesh(self):
        """Run all validation checks on the mesh"""
        if self.importer.mesh is None:
            print("No mesh loaded. Cannot validate.")
            return False

        # Run all validation checks
        self.validation_results["has_facets"] = self._check_has_facets()
        self.validation_results["has_valid_normals"] = self._check_normals()
        self.validation_results["is_manifold"] = self._check_manifold()

        # Overall validation result
        is_valid = all(self.validation_results.values())

        # Print validation summary
        self._print_validation_summary()

        return is_valid

    def _check_has_facets(self):
        """Check if the mesh has any facets"""
        if len(self.importer.facets) == 0:
            print("Validation failed: Mesh has no facets")
            return False
        return True

    def _check_normals(self):
        """Check if normals are valid (non-zero)"""
        if np.any(np.all(self.importer.normals == 0, axis=1)):
            print("Validation failed: Mesh has zero-length normals")
            return False
        return True

    def _check_manifold(self):
        """Basic check for manifold geometry (simplified)"""
        # This is a simplified check - a proper check would be more complex
        # For MVP, we're just checking if the mesh has a positive volume
        if self.importer.get_mesh_stats()["volume"] <= 0:
            print("Validation failed: Mesh appears to have zero or negative volume")
            return False
        return True

    def _print_validation_summary(self):
        """Print a summary of validation results"""
        print("\nSTL Validation Summary:")
        for check, result in self.validation_results.items():
            status = "PASS" if result else "FAIL"
            print(f"  {check}: {status}")
