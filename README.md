# BrVc: Bioreactor Volume Calculator

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

This project was developed using *Python 3.11*. To get started follow the steps below:

### Clone the Repository

To get started, cd into the direcotry of your project and clone the repository from GitHub:

```sh
git clone https://github.com/parisisv/BrVc.git
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

## A note on the dataset

The dataset provided in this repository is a fictitious data set that contains the cumulative amounts of acid, base and antifoam as well as two nutrient feed streams to the bioreactor. Manual sampling is considered as well. `BrVc`, at the moment, expects only the cumulative amount of each nutrient/reagent and utilises `pandera` schemas to validate that condition.

For using the tool with real datasets the user can modify the corresponding *schema* in order to add/delete nutrient/reagent streams. For example, if only a base solution and a nutrient solution were used in an experiment, the corresponding schema can be written as follows:

```py
class OnlineDataSchema(DataFrameModel):
    """Schema for online data"""

    time_h: Series[float] = pa.Field(ge=0, coerce=True)
    base_total_ml: Series[float] = pa.Field(ge=0, coerce=True)
    stream_1_total_ml: Series[float] = pa.Field(ge=0, coerce=True)

    @pa.dataframe_check()
    def check_cum_sum(cls, df: pd.DataFrame) -> bool:
        # Check if the cumulative sum of each column is not zero
        columns_with_zero_cumsum = [
            col for col in df.columns if df[col].cumsum().iloc[-1] == 0
        ]
        if columns_with_zero_cumsum:
            raise pa.errors.SchemaError(
                schema=cls,
                data=df,
                message=f"Columns with zero cumulative sum: {columns_with_zero_cumsum}",
            )
        return True
```

**Important note**: Make sure to use the same class variable names as the headers of then data columns, otherwise `pandera` will raise a `SchemaError`.  










