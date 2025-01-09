# optimization.py

from column_calculations import co2_absorption

# Constants for energy calculation
METHANE_PURITY_TARGET = 0.95
ENERGY_PER_M3_PUMP = 0.3
ENERGY_PER_M3_COMPRESS = 0.1

# Base case parameters for reference
BASE_FEED_RATE = 20.0  # m³/hr
BASE_WATER_FLOW = 3.0  # m³/hr
BASE_COLUMN_HEIGHT = 5.98  # meters
BASE_COLUMN_DIAMETER = 0.15  # meters
BASE_WORKING_PRESSURE = 10.0  # bar
BASE_OUTPUT_PURITY = 98.0  # % Methane
BASE_ENERGY_CONSUMPTION = 5.25  # kW
BASE_SPECIFIC_ENERGY = 0.26  # kWh/Nm³

# 150 m³/hr case parameters for reference
LARGE_FEED_RATE = 150.0  # m³/hr
LARGE_COLUMNS = 3
LARGE_WATER_FLOW = 9.0  # m³/hr total, 3 m³/hr per column
LARGE_COLUMN_HEIGHT = 7.0  # meters
LARGE_COLUMN_DIAMETER = 1.0 / 3.0  # meters (1 m total diameter divided across 3 columns)
LARGE_WORKING_PRESSURE = 10.0  # bar
LARGE_OUTPUT_PURITY = 95.0  # % Methane
LARGE_SPECIFIC_ENERGY = 0.26  # kWh/Nm³ (similar energy consumption rate)

def methane_recovery(retention_time):
    recovery_efficiency = 0.9 + 0.02 * retention_time
    return max(0, min(1, recovery_efficiency))

def optimize_energy(params):
    feed_rate, water_flow, pressure, column_height, column_diameter, retention_time = params
    co2_removed = co2_absorption(feed_rate, water_flow, pressure, column_height, column_diameter)
    ch4_recovery = methane_recovery(retention_time)
    energy_cost = water_flow * ENERGY_PER_M3_PUMP + pressure * ENERGY_PER_M3_COMPRESS
    
    # Methane purity calculation based on CH4 recovered and CO2 removed
    methane_purity = (feed_rate * ch4_recovery) / (feed_rate + co2_removed)
    purity_penalty = abs(METHANE_PURITY_TARGET - methane_purity) * 100
    
    # Specific energy adjustment based on configuration size
    if feed_rate <= BASE_FEED_RATE:
        specific_energy = BASE_SPECIFIC_ENERGY
    elif feed_rate == LARGE_FEED_RATE:
        specific_energy = LARGE_SPECIFIC_ENERGY
    else:
        specific_energy = BASE_SPECIFIC_ENERGY * (feed_rate / BASE_FEED_RATE)
    
    total_energy = specific_energy * feed_rate  # Total energy in kWh
    
    # Add the total energy to the objective function
    return energy_cost + purity_penalty + total_energy
