from analysis.xmlanalyzer import XMLAnalyzer
from visualization.visualization import TrialVisualizer
from config import Config

# visualizing data from the example data folder

if __name__ == "__main__":

    participant_id = "1"

    xmlanalyzer = XMLAnalyzer(participant_id, "./example-data")
    trial_data = xmlanalyzer.extract_all_object_data()

    root_directory = Config.get_output_subdir("visualization")
    group_category = "example-data"

    for trial in trial_data:
        trial_num, trial_type, object_data = trial
        object_positions = [(real_x, real_z) for _, real_x, real_z, _, _, _, _ in object_data]
        placed_positions = [(placed_x, placed_z) for _, _, _, placed_x, placed_z, _, _ in object_data]

        visualizer = TrialVisualizer((trial_num, object_positions), (trial_num, placed_positions), trial_num, participant_id, root_directory, group_category)
        visualizer.plot()
