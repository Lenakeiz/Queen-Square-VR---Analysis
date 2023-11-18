import os
from lxml import etree
from config import Config
from analysis.xmlanalyzer import XMLAnalyzer
from analysis.objects_configurator import ObjectConfigurator

def extract_positions_from_xml(xml_file, block_num):
    """
    Extract object positions from an XML file considering the correct XML structure.
    """
    positions_list = []
    tree = etree.parse(xml_file)
    trials = tree.xpath('//Trial')
    
    for trial in trials:
        trial_num = int(trial.find('TrialNumber').text)
        object_infos = trial.xpath('.//ConfigurationInfo/ObjectInfo')
        
        positions = set()
        for obj_info in object_infos:
            x = float(obj_info.xpath('./Real_Position/x/text()')[0])
            z = float(obj_info.xpath('./Real_Position/z/text()')[0])
            positions.add((x, z))
        
        # Combine block number with trial number to get the overall trial order
        overall_trial_num = (block_num - 1) * 9 + trial_num
        positions_list.append((overall_trial_num, positions))
            
    return positions_list

def order_positions(positions):
    """
    Order a set of positions based on the x-coordinate.
    
    Args:
    - positions (set): A set of 2D positions.

    Returns:
    - list: A list of 2D positions ordered by the x-coordinate.
    """
    return sorted(list(positions), key=lambda x: x[0])

def count_conditions_in_files(file_paths):
    """
    Count occurrences of specific conditions in a list of XML files.
    
    Args:
    - file_paths (list): List of paths to the XML files.

    Returns:
    - dict: Dictionary with counts of each condition.
    """
    # Initialize a dictionary to store the counts of each condition
    condition_dict = {"WalkAllo": 0, "Teleport": 0, "WalkEgo": 0}

    # Iterate through each file and count the occurrences of each condition
    for xml_file in file_paths:
        with open(xml_file, 'r', encoding='utf-8') as file:
            content = file.read()
            for condition in condition_dict.keys():
                condition_dict[condition] += content.count(condition)
                
    return condition_dict

def check_object_configurations_on_real_data():
    # List of XML files provided by the user
    xml_files = [
        "./example-data/1_1.xml",
        "./example-data/1_2.xml",
        "./example-data/1_3.xml",
        "./example-data/1_4.xml"
    ]
    
    # Call the function and print the results
    result = count_conditions_in_files(xml_files)
    for condition, count in result.items():
        print(f"{condition}: {count} occurrences")

    # Extract object positions from all XML files
    all_positions_corrected = []
    for i, xml_file in enumerate(xml_files, 1):
        all_positions_corrected.extend(extract_positions_from_xml(xml_file, i))
    
    # Read the positions from the 4.csv file without skipping any line
    csv_positions = []
    with open(Config.OBJECT_CONFIGURATION_CSV_FILE_PATH, 'r') as file:
        for line in file:
            values = line.strip().split(',')
            positions = {(float(values[i]), float(values[i+2])) for i in range(0, len(values), 3)}
            csv_positions.append(positions)
    
    # Match XML configurations to CSV configurations
    matches = []
    for trial_num, xml_config in all_positions_corrected:
        ordered_xml_config = order_positions(xml_config)
        for line_num, csv_config in enumerate(csv_positions, 1):
            ordered_csv_config = order_positions(csv_config)
            if ordered_xml_config == ordered_csv_config:
                matches.append((trial_num, line_num))
                break
    
    for match in matches:
        print(f"Trial number {match[0]} matches line number {match[1]} in the CSV file")

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