# column_calculations.py

import numpy as np

# Constants
CO2_SOLUBILITY_RATIO = 26
COLUMN_PACKING_EFFICIENCY = 0.85
MAX_COLUMN_HEIGHT = 7
MAX_COLUMN_DIAMETER = 1
base_feed_rate = 150
base_columns = 3

def calculate_columns(feed_rate):
    columns_needed = max(1, int(np.ceil(feed_rate / base_feed_rate * base_columns)))
    return columns_needed

def column_dimensions_per_column(feed_rate_per_column):
    height = min(MAX_COLUMN_HEIGHT, (feed_rate_per_column / base_feed_rate) * MAX_COLUMN_HEIGHT)
    diameter = min(MAX_COLUMN_DIAMETER, (feed_rate_per_column / base_feed_rate) * MAX_COLUMN_DIAMETER)
    return height, diameter

def co2_absorption(feed_rate, water_flow, pressure, column_height, column_diameter):
    co2_absorbed = water_flow * CO2_SOLUBILITY_RATIO * COLUMN_PACKING_EFFICIENCY / (column_height * column_diameter)
    return co2_absorbed
