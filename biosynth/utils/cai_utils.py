import numpy as np

def calculate_cai(sum_log, count_log) -> float:
    cai = np.exp(-sum_log / count_log) if count_log > 0 else 0.0
    return np.trunc(cai * 10000) / 10000
