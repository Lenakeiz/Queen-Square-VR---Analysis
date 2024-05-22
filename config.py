import os

class Config:
    OBJECT_CONFIGURATION_CSV_FILE_PATH = './configuration/4.csv'
    OUTPUT_DIR = './output'
    CONDITIONS = {"WalkEgo", "WalkAllo", "Teleport"}
    INPUT_DIR = './data'

    @staticmethod
    def get_output_subdir(subdir_name):
        return os.path.join(Config.OUTPUT_DIR, subdir_name)
    
    @staticmethod
    def get_input_subdir(subdir_name):
        return os.path.join(Config.INPUT_DIR, subdir_name)