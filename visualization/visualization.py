import os
import matplotlib.pyplot as plt
from config import Config

class TrialVisualizer:
    def __init__(self, object_positions, placed_positions, trial_number, participant_id):
        self.object_positions = object_positions
        self.placed_positions = placed_positions
        self.trial_number = trial_number
        self.participant_id = participant_id
        self.logdir = os.path.join(Config.get_output_subdir("visualizations"), participant_id)
        self.colors = ['blue', 'gray', 'purple', 'orange']
        self._init_figure()

    def _init_figure(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        self.fig = fig
        self.ax = ax
        self.ax.set_title(f"ID:{self.participant_id} Trial {self.trial_number}")

    def _plot(self):
        # Draw the circle with specified diameter and center
        main_circle = plt.Circle((3, -4), 7/2, color='black', fill=False, linewidth=2)
        self.ax.add_artist(main_circle)
        
        # Draw the modified rectangle
        rectangle = plt.Polygon([[-1.5, 0.5], [-1.5, -9], [12, -9], [12, 0.5]], closed=True, edgecolor='black', linewidth=2, fill=False)
        self.ax.add_artist(rectangle)
        
        # Add two new circles with line color cyan
        circle1 = plt.Circle((1, 1), 0.5/2, color='cyan', fill=False, linewidth=2)
        self.ax.add_artist(circle1)
        
        circle2 = plt.Circle((-2, -1), 0.5/2, color='cyan', fill=False, linewidth=2)
        self.ax.add_artist(circle2)

        trial_number, positions = self.object_positions

        print(f"Trial Number: {trial_number}")

        for (x,z), color in zip(positions, self.colors):
            self.ax.scatter(x, z, c=color, s=50)

        trial_number, placed_positions = self.placed_positions
        for (x,z), color in zip(placed_positions, self.colors):
            self.ax.scatter(x, z, marker='x', c=color, s=50)         

        # Set title, axis labels, and axis limits
        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Z Coordinate")
        
        # Explicitly setting the axis limits
        self.ax.set_xlim(-3, 13)
        self.ax.set_ylim(-10, 3)
        
        # Set equal aspect ratio after setting axis limits
        self.ax.set_aspect('equal', adjustable='box')  

    def plot(self):
        self._plot()
        self._save()
        plt.close(self.fig)  # Close the figure to free up memory

    def _get_output_path(self):
        return os.path.join(self.logdir, f"trial_{self.trial_number}.png")

    def _get_output_dir(self):
        return os.path.dirname(self._get_output_path())

    def _save(self):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        self.fig.savefig(self._get_output_path())