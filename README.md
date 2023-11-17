# leakageDataGenAndAnalysis

## Introduction

`leakageDataGenAndAnalysis` is a Python-based system for simulating a water distribution network and analyzing it for potential leakages. This project includes scripts for generating synthetic data representing water flow through a network of junctions and endpoints and for detecting and calculating water usage and leakages within this network.

## Setup

### Prerequisites

- Python 3.x
- Pandas library

### Installation

1. Clone the repository to your local machine:

```shell
git clone https://github.com/BlockOasis/leakageDataGenAndAnalysis.git
```

2. Navigate to the cloned repository.

3. (Optional) Set up a virtual environment:

```shell
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

4. Install the required packages:

```shell
pip install pandas
```

## Usage

### Data Generation

1. `data_maker.py` - Simulates basic water usage data in a distribution network.
2. `data_maker_leak.py` - Generates more complex network data with potential leakages.

Run these scripts to generate datasets. These datasets will be stored in the `outputs` directory.

### Data Analysis

1. `leakage_detection.py` - Analyzes the generated data to detect leakages in the network.
2. `usage_calculation.py` - Calculates the water usage at various endpoints over a specified time range.

Run these scripts to analyze the generated datasets for leakages and usage calculations.

### Running a Script

To run a script, navigate to its directory and execute it with Python. For example:

```shell
python data_generation/data_maker.py
```


## Scripts Description

- `data_generation/data_maker_no_leak.py`: Generates simulated water flow data for different types of locations in a water distribution network without consideration of leakage.
- `data_generation/data_maker_leak.py`: Simulates a complex water distribution network including a master junction and local junctions/endpoints with potential leakages.
- `data_analysis/leakage_detection.py`: Analyzes the generated dataset to identify and report potential leakages.
- `data_analysis/usage_calculation.py`: Calculates and reports the water usage at different endpoints within a specified time range.

## Outputs

The generated datasets and analysis reports are saved in the `outputs` directory.