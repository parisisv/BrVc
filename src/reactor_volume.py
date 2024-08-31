import numpy as np


class BioreactorVolumeCalculator:
    def __init__(
        self, initial_volume: float, F_in: float = 0.00, F_out: float = 0.00
    ) -> None:
        self.initial_volume = initial_volume
        self.F_in = F_in
        self.F_out = F_out

    def calculate_stream_volume(
        self, time: np.ndarray, streams: np.ndarray, addition_indices: np.ndarray
    ) -> np.ndarray:
        """Calculate the amount of material entering the bioreactor for multiple streams at any given time."""

        time_of_addition_list = []
        amount_added_list = []

        for i in range(streams.shape[1]):
            stream = streams[:, i]
            addition_idx = addition_indices[i]

            time_of_addition = time[addition_idx]  # time points, h
            edge = stream[addition_idx]  # stream edges (mL)
            rolled_edge = np.roll(stream[addition_idx], 1)
            rolled_edge[0] = 0
            amount_added = edge - rolled_edge  # Delta V (mL)

            time_of_addition_list.append(time_of_addition)
            amount_added_list.append(amount_added)

        # Flatten the lists to create a combined array
        all_times = np.concatenate(time_of_addition_list)
        all_amounts = np.concatenate(amount_added_list)

        # Combine times and amounts into a 2D array
        times_amounts = np.vstack((all_times, all_amounts)).T

        # Sort the combined array by the first column (time)
        sorted_times_amounts = times_amounts[np.argsort(times_amounts[:, 0])]

        return sorted_times_amounts

    def calculate_volume(
        self,
        time: np.ndarray,
        sampling_intervals: np.ndarray,
        material_addition_matrix: np.ndarray,
    ) -> np.ndarray:
        """Calculate working volume"""

        sampling_times = material_addition_matrix[:, 0]  # Sampling times in hours
        sampling_volumes = material_addition_matrix[:, 1]  # Sample volumes in mL

        # Initialize volume array
        volume = np.zeros(len(time))
        volume[0] = self.initial_volume

        for i, _ in enumerate(time[:-1], 1):
            dt = sampling_intervals[i]
            current_time = time[i]

            # Continuous inflow and outflow
            volume[i] = volume[i - 1] + (self.F_in - self.F_out) * dt

            # Discrete sampling events
            for t_sample, V_sample in zip(sampling_times, sampling_volumes):
                if abs(current_time - t_sample) < dt / 2:
                    volume[i] += V_sample

        return volume
