import numpy as np
import matplotlib.pyplot as plt


def visualize_slices(slices, max_layers=5):
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = plt.cm.viridis_r(np.linspace(0, 1, min(max_layers, len(slices))))

    # Track which layers have been added to legend
    legend_added = set()

    for i, (z, segments) in enumerate(slices[:max_layers]):
        for j, segment in enumerate(segments):
            # Extract x and y coordinates from the segment points
            x = [segment[0][0], segment[1][0]]
            y = [segment[0][1], segment[1][1]]

            # Add to legend only once per layer
            if i not in legend_added:
                ax.plot(x, y, color=colors[i], label=f'Layer {i + 1} (Z={z:.2f})')
                legend_added.add(i)
            else:
                ax.plot(x, y, color=colors[i])

    ax.set_title('Slice Contours Visualization')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.grid(True)
    ax.legend()
    ax.axis('equal')
    plt.show()
