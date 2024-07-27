import numpy as np
from scipy import stats


class StepChangeDetector:
    """Base class for step change detection in time series data."""

    def detect_step_changes(self, stream: np.ndarray) -> None:
        """Detect step changes in a time series stream"""
        raise NotImplementedError("This method should be overridden by subclasses")

    def apply_to_streams(self, streams: np.ndarray) -> list:
        """Apply step change detection to multiple time series streams."""
        # Transpose the matrix to work on columns as rows
        transposed_streams = streams.T

        # Apply the detect_step_changes function to each row of the transposed matrix
        change_indices = [self.detect_step_changes(row) for row in transposed_streams]

        return change_indices


class LRTStepChangeDetector(StepChangeDetector):
    """Likelihood Ratio Test (LRT) based step change detector."""

    def __init__(self, delta: float, min_size: float):
        self.delta = delta
        self.min_size = min_size

    def detect_step_changes(self, stream: np.ndarray) -> np.ndarray:
        stream_length = stream.shape[0]
        lrt_ratios = np.zeros(stream_length)

        # Vectorized computation of likelihood ratios
        lrt_ratios[1:] = stats.norm.pdf(
            stream[1:], loc=stream[:-1], scale=1
        ) / stats.norm.pdf(stream[:-1], loc=stream[:-1], scale=1)

        # Identify potential step changes based on delta
        possible_changes = np.where(lrt_ratios < self.delta)[0]

        # Apply min_size constraint
        change_indices = possible_changes[possible_changes >= self.min_size]

        return change_indices
