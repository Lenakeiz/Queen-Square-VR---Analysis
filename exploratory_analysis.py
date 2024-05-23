import os

from typing import List

from analysis.participant_data import ParticipantData
from analysis.data_loader import DataLoader
from visualization.visualization import ParticipantVisualizer

from config import Config

def visualize_data(participant_data_list):
    for participant_data in participant_data_list:
        participant_id = participant_data.participant_id
        data_frame = participant_data.data
        visualizer = ParticipantVisualizer(participant_id, data_frame)
        # plotting radial plots
        visualizer.create_radial_plots()
        visualizer.create_radial_plots_by_condition()

if __name__ == "__main__":
    positive_data = DataLoader(Config.get_input_subdir('positive'),data_group='positive')
    positive_data.save_extracted_data()
    visualize_data(positive_data.get_data())

    negative_data = DataLoader(Config.get_input_subdir('negative'), data_group='negative')
    negative_data.save_extracted_data()
    visualize_data(negative_data.get_data())



