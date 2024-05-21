import os

from analysis.participant_data import ParticipantData

from config import Config

def get_unique_participant_ids(directory):
    participant_ids = set()
    for file in os.listdir(directory):
        if file.endswith(".xml"):
            participant_id = file.split('_')[0]
            participant_ids.add(participant_id)
    return sorted(participant_ids)

def load_data(directory):
    participant_ids =  get_unique_participant_ids(directory)
    participant_data_list = []

    for participant_id in participant_ids:
        participant_data = ParticipantData(participant_id, directory)
        participant_data_list.append(participant_data)

    print(f"Data for participant {participant_id}:")
    print(participant_data.data.head())

    return participant_data_list

if __name__ == "__main__":
    participant_data_list = load_data(Config.get_input_subdir('positive'))