
def read_seq_from_file(file_path):
    with open(file_path, 'r') as file:
        raw_seq = file.readlines()
        for line in raw_seq:
            if line.isspace():
                continue
            return line.strip()
    return None


def read_patterns_from_file(file_path):
    res = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.isspace():
                continue
            patterns = line.strip().split(',')
            res.extend(patterns)
    return res
