# design_plant.py

from scipy.optimize import minimize
from column_calculations import calculate_columns, column_dimensions_per_column
from optimization import optimize_energy, METHANE_PURITY_TARGET, BASE_COLUMN_HEIGHT, BASE_COLUMN_DIAMETER, LARGE_FEED_RATE, LARGE_COLUMNS, LARGE_COLUMN_HEIGHT, LARGE_COLUMN_DIAMETER
from stack import PlantStack

def design_plant(feed_rate):
    plant_stack = PlantStack()
    columns = calculate_columns(feed_rate)
    feed_rate_per_column = feed_rate / columns

    for i in range(columns):
        # Handle specific cases
        if feed_rate_per_column <= 20.0:
            # Base case for smaller feed rate
            column_height = BASE_COLUMN_HEIGHT
            column_diameter = BASE_COLUMN_DIAMETER
            water_flow = 3.0
        elif feed_rate == LARGE_FEED_RATE and columns == LARGE_COLUMNS:
            # 150 m³/hr case with three parallel columns
            column_height = LARGE_COLUMN_HEIGHT
            column_diameter = LARGE_COLUMN_DIAMETER
            water_flow = 3.0  # Water flow per column
        else:
            # Scale up for larger configurations
            column_height, column_diameter = column_dimensions_per_column(feed_rate_per_column)
            water_flow = 2.0  # Default value for larger feeds
        
        # Initial guess for optimization, without flash pressure
        initial_params = [
            feed_rate_per_column, 
            water_flow, 
            10,  # Pressure
            column_height, 
            column_diameter, 
            60  # Retention time
        ]
        
        bounds = [
            (feed_rate_per_column, feed_rate_per_column),  # Feed rate per column (fixed)
            (1.0, 3.0),  # Water flow rate bounds
            (5, 15),  # Pressure bounds
            (column_height, column_height),  # Column height (fixed)
            (column_diameter, column_diameter),  # Column diameter (fixed)
            (30, 120)  # Retention time bounds
        ]
        
        # Run optimization
        result = minimize(optimize_energy, initial_params, bounds=bounds)
        optimal_params = result.x
        
        setup = {
            "Column": i + 1,
            "Feed Rate per Column (m³/h)": feed_rate_per_column,
            "Column Height (m)": column_height,
            "Column Diameter (m)": column_diameter,
            "Water Flow Rate (m³/h)": optimal_params[1],
            "Operating Pressure (bar)": optimal_params[2],
            "Retention Time (s)": optimal_params[5],
            "Methane Purity (%)": METHANE_PURITY_TARGET * 100
        }
        
        # Push each column configuration onto the stack
        plant_stack.push(setup)
    
    return plant_stack
