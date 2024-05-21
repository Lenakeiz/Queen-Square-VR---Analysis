import numpy as np
import pandas as pd
from analysis.xmlanalyzer import XMLAnalyzer

class ParticipantData:
    def __init__(self, participant_id, folder_path):
        self.participant_id = participant_id
        self.folder_path = folder_path
        self.data = self._load_data()

    def _load_data(self):
        xml_analyzer = XMLAnalyzer(participant_id=self.participant_id, folder_path=self.folder_path)
        real_positions = xml_analyzer.extract_all_object_positions()
        placed_positions = xml_analyzer.extract_all_placed_positions()
        trial_conditions = xml_analyzer.extract_all_trial_types()


        data = []
        for real, placed, condition in zip(real_positions, placed_positions, trial_conditions):
            trial_num = real[0]
            type_condition = condition
            for obj_num, (real_pos, placed_pos) in enumerate(zip(real[1], placed[1]), start=1):
                real_x, real_z = real_pos
                placed_x, placed_z = placed_pos
                distance = np.sqrt((real_x - placed_x) ** 2 + (real_z - placed_z) ** 2)
                data.append([self.participant_id, type_condition, trial_num, obj_num, real_x, real_z, placed_x, placed_z, distance])

        columns = ['participant_id', 'trial_type', 'trial_num', 'object_num', 'real_x', 'real_z', 'placed_x', 'placed_z', 'distance']
        return pd.DataFrame(data, columns=columns)

if __name__ == "__main__":
    pass