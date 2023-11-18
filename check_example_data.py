import os
from lxml import etree
from config import Config
from analysis.xmlanalyzer import XMLAnalyzer
from analysis.objects_configurator import ObjectConfigurator


def order_positions(positions):
    """
    Order a set of positions based on the x-coordinate.
    
    Args:
    - positions (set): A set of 2D positions.

    Returns:
    - list: A list of 2D positions ordered by the x-coordinate.
    """
    return sorted(list(positions), key=lambda x: x[0])

def check_object_positions_integrity_from_original_file_to(object_positions_from_configurator, object_positions_from_participant_file):
    # Match XML configurations to CSV configurations
    matches = []
    for trial_num, xml_config in object_positions_from_participant_file:
        ordered_xml_config = order_positions(xml_config)
        for line_num, csv_config in enumerate(object_positions_from_configurator, 1):
            ordered_csv_config = order_positions(csv_config)
            if ordered_xml_config == ordered_csv_config:
                matches.append((trial_num, line_num))
                break
    
    for match in matches:
        print(f"Trial number {match[0]} matches line number {match[1]} in the CSV file")

if __name__ == "__main__":

    analyzer = XMLAnalyzer("1", "./example-data")    
    result = analyzer.count_conditions_in_files()    
    all_object_positions = analyzer.extract_all_object_positions()

    #Printing occurences of each condition in the entire task
    for condition, count in result.items():
        print(f"{condition}: {count} occurrences")

    object_configurator = ObjectConfigurator()
    object_configurator.read_positions()
    object_positions_from_configurator = object_configurator.csv_positions

    check_object_positions_integrity_from_original_file_to(object_positions_from_configurator,all_object_positions)