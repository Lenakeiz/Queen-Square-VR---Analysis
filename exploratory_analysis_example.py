import pandas as pd
import numpy as np
from visualization.visualization import ParticipantVisualizer

if __name__ == "__main__":
    TESTDATA = [
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 1.0, "trial_num": 1},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 2.0, "trial_num": 1},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 3.0, "trial_num": 1},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 4.0, "trial_num": 1},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 2.0, "placed_z": 0.0, "trial_num": 2},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 2.0, "trial_num": 2},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": -2.0, "placed_z": 0.0, "trial_num": 2},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": -2.0, "trial_num": 2},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 1.0, "trial_num": 3},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 2.0, "trial_num": 3},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": -1.0, "trial_num": 3},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": -2.0, "trial_num": 3},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 2.0, "placed_z": 0.0, "trial_num": 4},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": 2.0, "trial_num": 4},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": -2.0, "placed_z": 0.0, "trial_num": 4},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 0.0, "placed_z": -4.0, "trial_num": 4},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi/6), "placed_z": 4.0 * np.sin(np.pi/6), "trial_num": 5},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi/6), "placed_z": 4.0 * np.sin(np.pi/6), "trial_num": 5},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(-np.pi/6), "placed_z": 4.0 * np.sin(-np.pi/6), "trial_num": 5},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(-np.pi/6), "placed_z": 4.0 * np.sin(-np.pi/6), "trial_num": 5},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*5/6), "placed_z": 4.0 * np.sin(np.pi*5/6), "trial_num": 6},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*5/6), "placed_z": 4.0 * np.sin(np.pi*5/6), "trial_num": 6},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*7/6), "placed_z": 4.0 * np.sin(np.pi*7/6), "trial_num": 6},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*7/6), "placed_z": 4.0 * np.sin(np.pi*7/6), "trial_num": 6},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*4/6), "placed_z": 4.0 * np.sin(np.pi*4/6), "trial_num": 7},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*5/6), "placed_z": 4.0 * np.sin(np.pi*5/6), "trial_num": 7},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*4/3), "placed_z": 4.0 * np.sin(np.pi*4/3), "trial_num": 7},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*13/12), "placed_z": 4.0 * np.sin(np.pi*13/12), "trial_num": 7},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi/2), "placed_z": 4.0 * np.sin(np.pi/2), "trial_num": 8},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*13/12), "placed_z": 4.0 * np.sin(np.pi*13/12), "trial_num": 8},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(np.pi*0), "placed_z": 4.0 * np.sin(np.pi*0), "trial_num": 8},
        {"real_x": 0.0, "real_z": 0.0, "placed_x": 4.0 * np.cos(-np.pi/2), "placed_z": 4.0 * np.sin(-np.pi/2), "trial_num": 8}
    ]

    df = pd.DataFrame(TESTDATA)
    participant_id = 'example'
    print(f'Creating visualizer for {participant_id}')
    visualizer = ParticipantVisualizer(participant_id=participant_id, data_frame=df)
    visualizer.create_radial_plots()