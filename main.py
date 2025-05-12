from stl_importer import STLImporter
from stl_validator import STLValidator
import argparse


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='STL Import and Validation for 5-Axis 3D Printing')
    parser.add_argument('filename', help='Path to the STL file')
    args = parser.parse_args()

    # Create importer and load STL
    importer = STLImporter(args.filename)
    if not importer.load_stl():
        print("Failed to load STL file. Exiting.")
        return

    # Print mesh statistics
    stats = importer.get_mesh_stats()
    print("\nMesh Statistics:")
    print(f"  Facets: {stats['facet_count']}")
    print(f"  Vertices: {stats['vertex_count']}")
    print(f"  Dimensions:")
    print(f"    X: {stats['dimensions']['x'][0]:.2f} to {stats['dimensions']['x'][1]:.2f}")
    print(f"    Y: {stats['dimensions']['y'][0]:.2f} to {stats['dimensions']['y'][1]:.2f}")
    print(f"    Z: {stats['dimensions']['z'][0]:.2f} to {stats['dimensions']['z'][1]:.2f}")
    print(f"  Volume: {stats['volume']:.2f} cubic units")

    # Validate the mesh
    validator = STLValidator(importer)
    is_valid = validator.validate_mesh()

    # Final result
    if is_valid:
        print("\nSTL file is valid and ready for slicing.")
    else:
        print("\nSTL file has validation issues that may affect printing.")


if __name__ == "__main__":
    main()
