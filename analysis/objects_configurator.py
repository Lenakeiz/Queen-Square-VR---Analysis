from config import Config

class ObjectConfigurator:
    def __init__(self):
        self.csv_positions = []

    def read_positions(self):
        with open(Config.OBJECT_CONFIGURATION_CSV_FILE_PATH, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                positions = {(float(values[i]), float(values[i+2])) for i in range(0, len(values), 3)}
                self.csv_positions.append(positions)

    @property
    def csv_positions(self):
        return self._csv_positions