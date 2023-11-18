import os

class Config:
    OBJECT_CONFIGURATION_CSV_FILE_PATH = './configuration/4.csv'
    OUTPUT_DIR = './output'
    CONDITION_DICT = {"WalkAllo": 0, "Teleport": 0, "WalkEgo": 0}

    @staticmethod
    def get_output_subdir(subdir_name):
        return os.path.join(Config.OUTPUT_DIR, subdir_name)