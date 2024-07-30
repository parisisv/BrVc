import numpy as np


def combine_online_and_offline_data(online_data, ofline_data):
    """combine online and offline data in one matrix for further processing"""
    return np.vstack((online_data, ofline_data))


def sort_time_data(data):
    """Sorts the data by time (first column)"""
    return data[data[:, 0].argsort()]


def calculate_time_intervals(time_points):
    """Calculate time intervals"""
    rolled_timed_points = np.roll(time_points, 1, axis=0)
    rolled_timed_points[0] = 0
    sampling_intevals = time_points - rolled_timed_points
    return sampling_intevals
