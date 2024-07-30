# Bioreactor Volume Calculation and Analysis

This project provides tools for calculating and analyzing bioreactor volume based on online and offline data measurements. It includes modules for data loading, step change detection, volume calculation, and data combination and sorting.

## Project Structure

- `src/`
  - `data_loader.py`: Contains the `DataLoader` class for loading and validating online and offline data with `pandera`.
  - `stepdetect.py`: Contains the `LRTStepChangeDetector` class for detecting step changes in a time series signal.
  - `reactor_volume.py`: Contains the `BioreactorVolumeCalculator` class for calculating bioreactor volume.
  - `utils.py`: Contains utility functions such as `combine_online_and_offline_data`, `sort_time_data`, and `calculate_time_intervals`.

## Installation

### Clone the Repository

To get started, clone the repository from GitHub:

```sh
git clone https://github.com/yourusername/bioreactor_volume.git
cd bioreactor_volume
```
### Set Up a Virtual Environment from a yaml file
1. Create a Virtual Environment Using Anaconda

If you have Anaconda installed, you can create a virtual environment using the provided env.yaml file. This file specifies the dependencies required for the project.

```sh
conda env create -f env.yaml
```
2. Activate the virtual environment

```sh
conda activate bioreactor_volume
```
### Setup a Virtual Environment manually and install dependencies
If you prefer to set up the environment manually or if you don't have an env.yaml file, you can create an anaconda environment using the following command 

```sh
conda create --name bioreactor_volume python=3.11
```

install the required packages using pip:

```sh
pip install -r requirements.txt
```
or conda

```sh
conda install --yes --file requirements.txt
```
