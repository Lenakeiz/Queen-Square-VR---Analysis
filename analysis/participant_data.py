import os
import numpy as np
import pandas as pd
from config import Config
from analysis.xmlanalyzer import XMLAnalyzer

class ParticipantData:
    def __init__(self, participant_id, folder_path):
        self.participant_id = participant_id
        self.folder_path = folder_path
        self.data = self._load_data()

    def _load_data(self):
        xml_analyzer = XMLAnalyzer(participant_id=self.participant_id, folder_path=self.folder_path)
        real_positions = xml_analyzer.extract_all_object_positions(include_block_num=True)
        placed_positions = xml_analyzer.extract_all_placed_positions(include_block_num=True)
        trial_conditions = xml_analyzer.extract_all_trial_types()

        data = []
        for real, placed, condition in zip(real_positions, placed_positions, trial_conditions):
            block_num_real, real_pos_data = real
            block_num_placed, placed_pos_data = placed
            type_condition = condition
            trial_num = real_pos_data[0]
            
            for obj_num, (real_pos, placed_pos) in enumerate(zip(real_pos_data[1], placed_pos_data[1]), start=1):
                real_x, real_z = real_pos
                placed_x, placed_z = placed_pos
                distance = np.sqrt((real_x - placed_x) ** 2 + (real_z - placed_z) ** 2)
                data.append([self.participant_id, block_num_real, type_condition, trial_num, obj_num, real_x, real_z, placed_x, placed_z, distance])

        columns = ['participant_id', 'block_num', 'trial_type', 'trial_num', 'object_num', 'real_x', 'real_z', 'placed_x', 'placed_z', 'distance']
        return pd.DataFrame(data, columns=columns)


    def save_data(self, subdirectory=''):
        participant_dir = os.path.join(Config.get_output_subdir('extracted_data'),subdirectory)
        os.makedirs(participant_dir, exist_ok=True)
        output_path = os.path.join(participant_dir, f'{self.participant_id}_data.csv')
        self.data.to_csv(output_path, index=False)
        print(f"{self.participant_id}: data saved to {output_path}")

if __name__ == "__main__":
    pass