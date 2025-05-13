from stl_importer import STLImporter
from stl_validator import STLValidator
from slicer import PlanarSlicer
import argparse
from visualizer import visualize_slices
from toolpath_generator import ToolpathGenerator
from orientation_calculator import OrientationCalculator
from kinematics import InverseKinematics
from gcode_generator import GcodeGenerator


def main():
    parser = argparse.ArgumentParser(description='5-Axis Slicer - Phase 1')
    parser.add_argument('filename', help='Path to STL file')
    parser.add_argument('--layer-height', type=float, default=0.2,
                       help='Layer height in mm')
    parser.add_argument('--output', default='slices.txt',
                       help='Output filename for slices')
    args = parser.parse_args()

    # STL Import & Validation
    importer = STLImporter(args.filename)
    if not importer.load_stl():
        return

    validator = STLValidator(importer)
    if not validator.validate_mesh():
        return

    # Planar Slicing
    try:
        slicer = PlanarSlicer(importer, args.layer_height)
        slicer.slice()
        slicer.export_contours(args.output)
        print(f"\nSuccessfully generated {len(slicer.layers)} layers")
        print(f"Slice data saved to {args.output}")
    except Exception as e:
        print(f"\nSlicing failed: {e}")

    visualize_slices(slicer.layers)

    # Generate toolpaths
    toolpath_gen = ToolpathGenerator(slicer)
    toolpaths = toolpath_gen.generate_toolpaths()
    print(f"Generated toolpaths for {len(toolpaths)} layers")

    # Calculate nozzle orientations
    orientation_calc = OrientationCalculator(importer, toolpaths)
    oriented_paths = orientation_calc.calculate_orientations()

    # Calculate 5-axis positions
    kinematics = InverseKinematics(oriented_paths)
    gcode_paths = kinematics.calculate_axis_positions()

    # Generate G-code
    gcode_gen = GcodeGenerator(gcode_paths)
    gcode = gcode_gen.generate_gcode()
    gcode_file = args.filename.replace('.stl', '.gcode')
    gcode_gen.save_gcode(gcode_file)
    print(f"G-code saved to {gcode_file}")

if __name__ == "__main__":
    main()
