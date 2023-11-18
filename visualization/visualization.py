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
        self._init_figure()

    def _init_figure(self):
        fig, ax = plt.subplots(figsize=(8, 8))
        self.fig = fig
        self.ax = ax
        self.ax.set_title(f"ID:{self.participant_id} Trial {self.trial_number}")

    def _plot(self):
        raise NotImplementedError

    def _save(self):
        raise NotImplementedError

    def plot(self):
        self._plot()
        self._save()

    def _get_output_path(self):
        return os.path.join(self.logdir, f"trial_{self.trial_number}.png")

    def _get_output_dir(self):
        return os.path.dirname(self._get_output_path())

    def _save(self):
        if not os.path.exists(self.logdir):
            os.makedirs(self.logdir)
        self.fig.savefig(self._get_output_path())