# Bioreactor Volume Calculation and Analysis

This project provides tools for calculating the working volume of a bioreactor based solely on (typically online) measurements of the cumulative amount of reagents/nutrients that were used for a specific experiment. The amount of broth that is removed during manual sampling can be also be acounted for.  

## Project Structure

- `src/`
  - `constants.py`: Contains the relevant project parameters. 

  - `data_loader.py`: Contains the `DataLoader` class for loading and validating data with `pandera`.

  - `reactor_volume.py`: Contains the `BioreactorVolumeCalculator` class for calculating bioreactor volume.

  - `schemas.py`: Contains schemas for online and offline data validation.

  - `stepdetect.py`: Contains the `LRTStepChangeDetector` class for detecting step changes in a time series signal using the *Likelihood Ratio Test* method.

  - `utils.py`: Contains utility functions

## Installation

### Clone the Repository

To get started, cd into the direcotry of your project and clone the repository from GitHub:

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
