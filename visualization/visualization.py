import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from analysis.participant_data import ParticipantData
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
        trial_number, placed_positions = self.placed_positions
        print(f"Plotting Trial Number: {trial_number}")

        for (x1, z1), (x2, z2), color in zip(positions, placed_positions, self.colors):
            self.ax.plot([x1, x2], [z1, z2], color=color, linestyle='--',linewidth=2) 
            self.ax.scatter(x1, z1, c=color, s=50)
            self.ax.scatter(x2, z2, marker='x', c=color, s=50)                  

        # Set title, axis labels, and axis limits
        self.ax.set_xlabel("X Coordinate")
        self.ax.set_ylabel("Z Coordinate")
        
        # Explicitly setting the axis limits
        self.ax.set_xlim(-3, 13)
        self.ax.set_ylim(-10, 3)
        
        # Set equal aspect ratio after setting axis limits
        self.ax.set_aspect('equal', adjustable='box')

        # Remove the box
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

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

class ParticipantVisualizer:
    def __init__(self, participant_id, data_frame):
        self.participant_id = participant_id
        self.data_frame = data_frame
        self.logdir = os.path.join(Config.get_output_subdir("radialPlots"), participant_id)
        self._init_output_dir()

    def _init_output_dir(self):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)

    def create_radial_plot(self):
        plot_data = []

        for trial in self.data_frame['trial_num'].unique():
            trial_data = self.data_frame[self.data_frame['trial_num'] == trial]
            for index, row in trial_data.iterrows():
                real_x = row['real_x']
                real_z = row['real_z']
                placed_x = row['placed_x']
                placed_z = row['placed_z']

                # Calculate the offset
                offset_x = placed_x - real_x
                offset_z = placed_z - real_z

                # Calculate the angle and distance
                angle = np.arctan2(offset_z, offset_x)
                distance = np.sqrt(offset_x ** 2 + offset_z ** 2)

                plot_data.append([trial, angle, distance])

        plot_df = pd.DataFrame(plot_data, columns=['trial', 'theta', 'r'])

        # Set up a grid of axes with a polar projection
        g = sns.FacetGrid(plot_df, col="trial", hue="trial",
                          subplot_kws=dict(projection='polar'), height=4.5,
                          sharex=False, sharey=False, despine=False)

        # Draw a scatterplot onto each axes in the grid
        g.map(sns.scatterplot, "theta", "r")

        # Ensure the radial limit is set to 12 meters
        for ax in g.axes.flat:
            ax.set_ylim(0, 12)

        # Save the plot
        output_path_single_trials = os.path.join(self.logdir, 'single_trials.png')
        g.savefig(output_path_single_trials)
        plt.close()

        print(f"Single trials plot saved to {output_path_single_trials}")

        # Create a combined plot for all trials
        plt.figure(figsize=(10, 10))
        ax = plt.subplot(111, polar=True)
        sns.scatterplot(data=plot_df, x='theta', y='r', hue='trial', ax=ax)
        ax.set_ylim(0, 12)
        
        output_path_across_trials = os.path.join(self.logdir, 'across_trials.png')
        plt.savefig(output_path_across_trials)
        plt.close()
        print(f"Across trials plot saved to {output_path_across_trials}")