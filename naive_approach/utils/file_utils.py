class FileDataReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_lines(self):
        with open(self.file_path, 'r') as file:
            return file.readlines()


class SequenceReader(FileDataReader):
    def read_sequence(self):
        raw_seq = self.read_lines()
        for line in raw_seq:
            if line.isspace():
                continue
            return line.strip()
        return None


class PatternReader(FileDataReader):
    def read_patterns(self):
        res = set()
        raw_patterns = self.read_lines()
        for line in raw_patterns:
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.update(patterns)
        return res


class CostReader(FileDataReader):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.value_mapping = {
            'inf': float('inf'),
            'o': 0.0,
            's': float('inf'),
            'w': float('inf'),
            'x': 1.0
        }

    def read_costs(self):
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
