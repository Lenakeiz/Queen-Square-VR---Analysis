import os
import subprocess
import pandas as pd
# importing classes
from typing import List

from analysis.participant_data import ParticipantData
from analysis.data_loader import DataLoader
from visualization.visualization import ParticipantVisualizer
from load_data import process_data_groups

from config import Config

def visualize_data(combined_df):
    for participant_id in combined_df['participant_id'].unique():
        participant_df = combined_df[combined_df['participant_id'] == participant_id]
        group_category = participant_df['status'].iloc[0]
        root_directory = Config.get_output_subdir("visualization")
        visualizer = ParticipantVisualizer(participant_id, participant_df, root_directory, group_category)
        # plotting radial plots
        visualizer.create_radial_plots()
        visualizer.create_radial_plots_by_condition()

if __name__ == "__main__":

    # Run the load_data.py script
    process_data_groups()

    # Load the combined data from the output/extracted_data folder
    combined_data_path = os.path.join(Config.get_output_subdir('extracted_data'), 'qsvr_data.csv')
    combined_df = pd.read_csv(combined_data_path)
    
    # Visualize the data for all participants
    visualize_data(combined_df)



