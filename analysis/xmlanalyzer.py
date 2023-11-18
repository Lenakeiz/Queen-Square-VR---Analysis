import os
from lxml import etree
from config import Config

class XMLAnalyzer:
    def __init__(self, participant_id, folder_path) -> None:
        self.participant_id = participant_id
        self.folder_path = folder_path # Adjust the path relative to the analysis folder
        self.xml_files = self.find_xml_files()

    def find_xml_files(self):
        xml_files = []
        for file in os.listdir(self.folder_path):
            if file.endswith(".xml") and file.startswith(self.participant_id + "_"):
                xml_files.append(os.path.join(self.folder_path, file))
        return xml_files
    
    def extract_all_object_positions(self):
        all_positions = []
        for xml_file in self.xml_files:
            block_num = int(xml_file.split('_')[-1].split('.')[0])
            positions = self.extract_object_positions_from_xml(xml_file, block_num)
            all_positions.extend(positions)
        return all_positions

    def extract_object_positions_from_xml(self, xml_file, block_num):
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
            
            overall_trial_num = (block_num - 1) * 9 + trial_num
            positions_list.append((overall_trial_num, positions))
                
        return positions_list
    
    def count_conditions_in_files(self):
        condition_dict = {condition: 0 for condition in Config.CONDITIONS}

        for xml_file in self.xml_files:
            with open(xml_file, 'r', encoding='utf-8') as file:
                content = file.read()
                for condition in condition_dict.keys():
                    condition_dict[condition] += content.count(condition)
                    
        return condition_dict