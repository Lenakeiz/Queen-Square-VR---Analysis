import os
import numpy as np
import pandas as pd
from config import Config
from analysis.xmlanalyzer import XMLAnalyzer

class ParticipantData:
    def __init__(self, participant_id, folder_path):
        self.participant_id = participant_id
        self.folder_path = folder_path
        self.xml_analyzer = XMLAnalyzer(participant_id=self.participant_id, folder_path=self.folder_path)
        self.data = self._load_data()

    def _load_data(self):
        all_data = self.xml_analyzer.extract_all_object_data(include_block_num=True)

        data = []
        for block_num, trial_data in all_data:
            trial_num, trial_type, object_data = trial_data
            
            for obj_data in object_data:
                obj_id, real_x, real_z, placed_x, placed_z, start_time, end_time = obj_data
                distance = np.sqrt((real_x - placed_x) ** 2 + (real_z - placed_z) ** 2)
                data.append([self.participant_id, block_num, trial_type, trial_num, obj_id, real_x, real_z, placed_x, placed_z, start_time, end_time, distance])

        columns = ['participant_id', 'block_num', 'trial_type', 'trial_num', 'object_id', 'real_x', 'real_z', 'placed_x', 'placed_z', 'start_time', 'end_time', 'distance']
        return pd.DataFrame(data, columns=columns)
    
    def _print_condition_counts(self):
        condition_counts = self.xml_analyzer.count_conditions_in_files()
        print(f"Condition counts for participant {self.participant_id}:")
        for condition, count in condition_counts.items():
            print(f"{condition}: {count}")
        print()

    def save_data(self, subdirectory=''):
        participant_dir = os.path.join(Config.get_output_subdir('extracted_data'),subdirectory)
        os.makedirs(participant_dir, exist_ok=True)
        output_path = os.path.join(participant_dir, f'{self.participant_id}_data.csv')
        self.data.to_csv(output_path, index=False)
        print(f"{self.participant_id}: data saved to {output_path}")