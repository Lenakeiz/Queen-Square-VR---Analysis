import os
from typing import List
from analysis.participant_data import ParticipantData

from config import Config

class DataLoader:
    def __init__(self, data_directory: str, data_group='unknown'):
        self.data_directory = data_directory
        self.participant_data_list = self._load_data()
        self.data_group = data_group

    def _get_unique_participant_ids(self) -> List[str]:
        participant_ids = set()
        for file in os.listdir(self.data_directory):
            if file.endswith(".xml"):
                participant_id = file.split('_')[0]
                participant_ids.add(participant_id)
        return sorted(participant_ids)

    def _load_data(self) -> List[ParticipantData]:
        participant_ids = self._get_unique_participant_ids()
        participant_data_list = []

        for participant_id in participant_ids:
            participant_data = ParticipantData(participant_id, self.data_directory)
            participant_data_list.append(participant_data)
        
        return participant_data_list

    def save_extracted_data(self):
        for participant_data in self.participant_data_list:
            participant_data.save_data(self.data_group)

    def get_data(self) -> List[ParticipantData]:
        return self.participant_data_list