
def read_seq_from_file(file_path):
    with open(file_path, 'r') as file:
        raw_seq = file.readlines()
        for line in raw_seq:
            if line.isspace():
                continue
            return line.strip()
    return None


def read_patterns_from_file(file_path):
    res = set()
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.update(patterns)

    return res


def read_costs_from_file(file_path):
    value_mapping = {
        'inf': float('inf'),
        'o': 0.0,
        's': float('inf'),
        'w': float('inf'),
        'x': 1.0
    }

    costs = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.strip():  # Skip empty lines
                pairs = line.strip().split(',')
                cost_dict = {}
                for pair in pairs:
                    key, value = pair.strip().split('=')
                    cost_dict[key.strip()] = value_mapping[value.strip()]
                costs.append(cost_dict)
    return costs
