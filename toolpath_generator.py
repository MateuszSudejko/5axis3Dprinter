class ToolpathGenerator:
    def __init__(self, slicer):
        self.slicer = slicer
        self.toolpaths = []

    def generate_toolpaths(self):
        """Generate toolpaths from slice contours"""
        for z, contours in self.slicer.layers:
            layer_path = []

            # Connect segments to form continuous paths
            if contours:
                # Start with first segment
                current_point = contours[0][0]
                layer_path.append(current_point)

                # Process all segments
                remaining_segments = contours.copy()
                while remaining_segments:
                    # Find closest segment to current point
                    closest_idx, closest_end = self._find_closest_segment(current_point, remaining_segments)

                    if closest_idx is not None:
                        segment = remaining_segments.pop(closest_idx)
                        # Add the segment in correct orientation
                        if closest_end == 0:
                            # Add segment in forward direction
                            layer_path.append(segment[1])
                            current_point = segment[1]
                        else:
                            # Add segment in reverse direction
                            layer_path.append(segment[0])
                            current_point = segment[0]
                    else:
                        # No more connected segments, start a new path if segments remain
                        if remaining_segments:
                            current_point = remaining_segments[0][0]
                            layer_path.append(current_point)

            self.toolpaths.append((z, layer_path))
        return self.toolpaths

    def _find_closest_segment(self, point, segments, threshold=1e-6):
        """Find segment with endpoint closest to given point"""
        closest_idx = None
        closest_end = None
        min_dist = float('inf')

        for i, segment in enumerate(segments):
            # Check first endpoint
            dist0 = self._distance(point, segment[0])
            if dist0 < min_dist:
                min_dist = dist0
                closest_idx = i
                closest_end = 0

            # Check second endpoint
            dist1 = self._distance(point, segment[1])
            if dist1 < min_dist:
                min_dist = dist1
                closest_idx = i
                closest_end = 1

        # Return None if no segment is close enough
        if min_dist > threshold:
            return None, None

        return closest_idx, closest_end

    def _distance(self, p1, p2):
        """Calculate Euclidean distance between two points"""
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
