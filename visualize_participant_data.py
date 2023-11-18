from analysis.xmlanalyzer import XMLAnalyzer
from visualization.visualization import TrialVisualizer

if __name__ == "__main__":

    participant_id = "1"

    xmlanalyzer = XMLAnalyzer(participant_id, "./example-data")
    object_positions = xmlanalyzer.extract_all_object_positions()
    placed_positions = xmlanalyzer.extract_all_placed_positions()

    if len(object_positions) != len(placed_positions):
        raise ValueError("The dimensions of object_positions and placed_positions are not the same. Please check imported data.")
    
    for trial_num, (object_positions, placed_positions) in enumerate(zip(object_positions, placed_positions), 1):
        visualizer = TrialVisualizer(object_positions, placed_positions, trial_num, participant_id)
        visualizer.plot()
