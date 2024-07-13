import numpy as np
import scipy.stats as stats

def detect_step_changes(stream, delta, min_size):
    """Perform the Likelihood Ratio Test (LRT) for detecting step changes in a time series stream.

    Args:
        stream (nparray): 1D numpy array, the time stream
        delta (float): significance level for detecting changes
        min_size (float): minimum size of a change to be detected

    Returns:
        nparray: Array that contains the indices where the step changes occur
    """
    
    stream_length = stream.shape[0]
    likelihood_ratios = np.zeros(stream_length)
    
    # Vectorized computation of likelihood ratios
    likelihood_ratios[1:] = stats.norm.pdf(
        stream[1:], loc=stream[:-1], scale=1) / stats.norm.pdf(stream[:-1], loc=stream[:-1], scale=1)
    
    # Identify potential step changes based on delta
    potential_changes = np.where(likelihood_ratios < delta)[0]
    
    # Apply min_size constraint
    step_changes_idx = potential_changes[potential_changes >= min_size]
    
    return step_changes_idx

def apply_detect_step_changes_to_multiplte_streams(streams_matrix, delta, min_size):
    """apply_detect_step_changes_to_multiplte_streams

    Args:
        streams_matrix ([type]): [description]
        delta ([type]): [description]
        min_size ([type]): [description]

    Returns:
        [type]: [description]
    """
    # Transpose the matrix to work on columns as rows
    transposed_matrix = streams_matrix.T
    
    # Apply the detect_step_changes function to each row of the transposed matrix
    addition_idx = [detect_step_changes(row, delta, min_size) for row in transposed_matrix]
    
    # Transpose the results back to original column-wise structure
    return addition_idx

def calculate_stream_volume(time, stream, addition_idx):
    """Calculate the amount of material entering the bioreactor at any given time 

    Args:
        time (nparray): time horizon (typicaly in hrs)
        stream (nparray): The cumulative addition stream from the bioreactor logger software
        addition_idx (nparray): Array containing intices that contain information about when a step change in the stream array occur 

    Returns:
        time_of_addition (nparray): times when material is added to the bioreactor
        amount_added (nparray): amount of material (mL) added to the bioreactor
    """
    
    time_of_addition = time[addition_idx]  # time points, h
    edge = stream[addition_idx]  # stream edges (corners) (mL)
    rolled_edge = np.roll(stream[addition_idx], 1)
    rolled_edge[0] = 0
    amount_added = edge - rolled_edge  # Delta V (mL)

    return time_of_addition, amount_added

def calculate_additions_from_multiple_streams(time, streams_matrix, addition_idx):
    """calculate_additions_from_multiple_streams

    Args:
        time ([type]): [description]
        streams_matrix ([type]): [description]
        addition_idx ([type]): [description]
    """
    times_store = np.zeros(1)
    amount_store = np.zeros(1)
    
    for i in range(streams_matrix.shape[1]):
        stream_i = streams_matrix[:,i]
        idx = addition_idx[i]
        time_of_addition, amount_added = calculate_stream_volume(time, stream_i, idx)
        times_store = np.concatenate((times_store, time_of_addition))
        amount_store = np.concatenate((amount_store, amount_added))
    
    final_times_store = np.delete(times_store, 0)
    final_amount_store = np.delete(amount_store, 0)
    material_addition_matrix = np.vstack((final_times_store, final_amount_store))
        
    return material_addition_matrix.T

def combine_online_and_offline_data(online_data, ofline_data):
    """combine online and offline data in one matrix for further processing"""
    return np.vstack((online_data, ofline_data))

def sort_time_data(data):
    """ Sorts the data by time (first column)"""
    return data[data[:, 0].argsort()]

def calculate_sampling_intervals(time_points):
    """ Calculate sampling intervals"""
    rolled_timed_points = np.roll(time_points, 1, axis=0)
    rolled_timed_points[0] = 0
    sampling_intevals = time_points - rolled_timed_points
    return sampling_intevals

def calculate_volume(time, sampling_intervals, material_addition_matrix, initial_volume):
    """Calculate working volume"""
    F_in = 0.00  # Constant inflow rate in mL per hour
    F_out = 0.00  # Constant outflow rate in mL per hour
    sampling_times = material_addition_matrix[:,0]  # Sampling times in hours
    sampling_volumes = material_addition_matrix[:,1]  # Sample volumes in mL

    # Initialize volume array
    volume = np.zeros(len(time))
    volume[0] = initial_volume

    # Perform numerical integration
    for i in range(1, len(time)):
        dt = sampling_intervals[i]
        current_time = time[i]

        # Continuous inflow and outflow
        volume[i] = volume[i-1] + (F_in - F_out) * dt

        # Discrete sampling events
        for t_sample, V_sample in zip(sampling_times, sampling_volumes):
            if abs(current_time - t_sample) < dt/2:
                volume[i] += V_sample
                
    return volume, sampling_volumes