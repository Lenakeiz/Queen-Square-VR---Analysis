import os
import subprocess
import pandas as pd
# importing classes
from typing import List

from analysis.participant_data import ParticipantData
from analysis.data_loader import DataLoader
from visualization.visualization import ParticipantVisualizer, TrialVisualizer
from load_data import process_data_groups

from config import Config

def visualize_data(combined_df):
    for participant_id in combined_df['participant_id'].unique():
        participant_df = combined_df[combined_df['participant_id'] == participant_id]
        group_category = participant_df['status'].iloc[0]
        root_directory = Config.get_output_subdir("visualization")
        visualizer = ParticipantVisualizer(participant_id, participant_df, root_directory, group_category)
        
        # Plotting radial plots
        visualizer.create_radial_plots()
        visualizer.create_radial_plots_by_condition()
        
        # Visualize individual trials using TrialVisualizer
        visualize_individual_trials(participant_df, participant_id, root_directory, group_category)

def visualize_individual_trials(participant_df, participant_id, root_directory, group_category):
    for trial_num in participant_df['trial_num'].unique():
        trial_df = participant_df[participant_df['trial_num'] == trial_num]
        
        object_positions = [(row['real_x'], row['real_z']) for _, row in trial_df.iterrows()]
        placed_positions = [(row['placed_x'], row['placed_z']) for _, row in trial_df.iterrows()]
        
        visualizer = TrialVisualizer((trial_num, object_positions), (trial_num, placed_positions), trial_num, participant_id, root_directory, group_category)
        visualizer.plot()

if __name__ == "__main__":

    # Run the load_data.py script
    process_data_groups()

    # Load the combined data from the output/extracted_data folder
    combined_data_path = os.path.join(Config.get_output_subdir('extracted_data'), 'qsvr_data.csv')
    combined_df = pd.read_csv(combined_data_path)
    
    # Visualize the data for all participants
    visualize_data(combined_df)



