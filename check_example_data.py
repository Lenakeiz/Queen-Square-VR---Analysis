import os
from lxml import etree
from config import Config
from analysis.xmlanalyzer import XMLAnalyzer
from analysis.participant_data import ParticipantData
from analysis.objects_configurator import ObjectConfigurator

def order_positions(positions):
    """
    Order a set of positions based on the x-coordinate.
    
    Args:
    - positions (list): A list of dictionaries containing 'real_x' and 'real_z' keys,
                        or a list of tuples containing (x, z) coordinates.

    Returns:
    - list: A list of positions ordered by the x-coordinate.
    """
    if isinstance(positions[0], dict):
        return sorted(positions, key=lambda x: x['real_x'])
    elif isinstance(positions[0], tuple):
        return sorted(positions, key=lambda x: x[0])
    else:
        raise ValueError("Unsupported position format")

def check_object_positions_integrity(object_positions_from_configurator, object_positions_from_participant_data):
    # Match object configurations from configurator to participant data
    matches = []
    for trial_num, trial_data in object_positions_from_participant_data.groupby(['trial_num']):
        participant_config = trial_data[['real_x', 'real_z']].to_dict('records')
        ordered_participant_config = order_positions(participant_config)
        for line_num, configurator_config in enumerate(object_positions_from_configurator, 1):
            ordered_configurator_config = order_positions(list(configurator_config))
            if ordered_participant_config == [{'real_x': x, 'real_z': z} for x, z in ordered_configurator_config]:
                matches.append((trial_num, line_num))
                break
    
    for match in matches:
        print(f"Trial number {match[0]} matches line number {match[1]} in the configurator file")

if __name__ == "__main__":

    participant_data = ParticipantData("PAT002", "./data/positive/", "positive")    

    all_object_positions = participant_data.get_object_positions()
    object_configurator = ObjectConfigurator()
    object_configurator.read_positions()
    object_positions_from_configurator = object_configurator.csv_positions

    check_object_positions_integrity(object_positions_from_configurator,all_object_positions)