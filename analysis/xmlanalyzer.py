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
    
    def extract_all_object_data(self,  include_block_num=False):
        all_data = []
        for xml_file in self.xml_files:
            block_num = int(xml_file.split('_')[-1].split('.')[0])
            data = self.extract_object_data_from_xml(xml_file, block_num)
            
            if include_block_num:
                all_data.extend([(block_num, d) for d in data])
            else:
                all_data.extend(data)

        return all_data

    def extract_object_data_from_xml(self, xml_file, block_num):
        data_list = []
        tree = etree.parse(xml_file)
        trials = tree.xpath('//Trial')

        for trial in trials:
            trial_num = int(trial.find('TrialNumber').text)
            trial_type = trial.find('Condition').text
            object_infos = trial.xpath('.//ConfigurationInfo/ObjectInfo')
            
            trial_data = []
            for obj_info in object_infos:
                obj_id = int(obj_info.find('Id').text)
                real_x = round(float(obj_info.xpath("./Real_Position/x/text()")[0]), 3)
                real_z = round(float(obj_info.xpath("./Real_Position/z/text()")[0]), 3)
                placed_x = round(float(obj_info.xpath("./Placed_Position/x/text()")[0]), 3)
                placed_z = round(float(obj_info.xpath("./Placed_Position/z/text()")[0]), 3)
                start_time = round(float(obj_info.find('Start_TrialTrial_UnityTimeStamp').text), 3)
                end_time = round(float(obj_info.find('End_Trial_UnityTimeStamp').text), 3)
                trial_data.append((obj_id, real_x, real_z, placed_x, placed_z, start_time, end_time))
            
            overall_trial_num = (block_num - 1) * 6 + trial_num
            data_list.append((overall_trial_num, trial_type, trial_data))
            
    
    def count_conditions_in_files(self):
        condition_dict = {condition: 0 for condition in Config.CONDITIONS}

        for xml_file in self.xml_files:
            with open(xml_file, 'r', encoding='utf-8') as file:
                content = file.read()
                for condition in condition_dict.keys():
                    condition_dict[condition] += content.count(condition)
                    
        return condition_dict