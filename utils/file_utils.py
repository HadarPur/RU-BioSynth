# Define a base class for reading data from a file.
class FileDataReader:
    def __init__(self, file_path):
        """
        Initializes a FileDataReader object.

        :param file_path: Path to the file to be read.
        """
        self.file_path = file_path

    def read_lines(self):
        """
        Reads the lines from the specified file.

        :return: A list containing the lines read from the file.
        """
        with open(self.file_path, 'r') as file:
            return file.readlines()

# Inherit from FileDataReader to read sequences from a file.
class SequenceReader(FileDataReader):
    def read_sequence(self):
        """
        Reads a sequence from the file, removing leading/trailing whitespace.

        :return: A string representing a sequence, or None if no valid sequence is found.
        """
        raw_seq = self.read_lines()
        for line in raw_seq:
            if line.isspace():
                continue
            return line.strip()
        return None

# Inherit from FileDataReader to read patterns from a file.
class PatternReader(FileDataReader):
    def read_patterns(self):
        """
        Reads patterns from the file, splitting them by commas and adding to a set.

        :return: A set containing the extracted patterns.
        """
        res = set()
        raw_patterns = self.read_lines()
        for line in raw_patterns:
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.update(patterns)
        return res

# Inherit from FileDataReader to read costs from a file.
class CostReader(FileDataReader):
    def __init__(self, file_path):
        """
        Initializes a CostReader object.

        :param file_path: Path to the file containing cost data.
        """
        super().__init__(file_path)
        self.value_mapping = {
            'inf': float('inf'),
            'o': 0.0,
            'w': 1e+15,
            'x': 1.0
        }

    def read_costs(self):
        """
        Reads cost data from the file, creating dictionaries based on key-value pairs.

        :return: A list of dictionaries representing cost mappings.
        """
        costs = []
        raw_costs = self.read_lines()
        for line in raw_costs:
            if line.strip():
                pairs = line.strip().split(',')
                cost_dict = {}
                for pair in pairs:
                    key, value = pair.strip().split('=')
                    cost_dict[key.strip()] = self.value_mapping[value.strip()]
                costs.append(cost_dict)
        return costs
