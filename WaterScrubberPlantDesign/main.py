# app.py

import streamlit as st
from design_plant import design_plant

def main():
    st.title("Biogas Upgrading Plant Configuration")
    
    # Get user input for feed rate
    feed_rate = st.number_input("Enter the feed rate (m³/h):", min_value=1.0, value=150.0, step=1.0)

    if st.button("Generate Plant Configuration"):
        # Generate plant setup based on the input feed rate
        plant_setup_stack = design_plant(feed_rate)

        # Display the full setup
        st.write("### Optimal Plant Configuration for Given Feed Rate:")
        full_setup = plant_setup_stack.get_full_setup()
        
        # Loop through each column setup and display neatly
        for column_setup in full_setup:
            col_number = column_setup['Column']
            with st.expander(f"Column {col_number} Configuration"):
                st.write(f"**Feed Rate per Column (m³/h):** {column_setup['Feed Rate per Column (m³/h)']}")
                st.write(f"**Column Height (m):** {column_setup['Column Height (m)']}")
                st.write(f"**Column Diameter (m):** {column_setup['Column Diameter (m)']}")
                st.write(f"**Water Flow Rate (m³/h):** {float(column_setup['Water Flow Rate (m³/h)'])}")
                st.write(f"**Operating Pressure (bar):** {float(column_setup['Operating Pressure (bar)'])}")
                st.write(f"**Methane Purity (%):** {column_setup['Methane Purity (%)']}")

if __name__ == "__main__":
    main()
