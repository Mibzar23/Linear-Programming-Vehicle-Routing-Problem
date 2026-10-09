import pandas as pd
import streamlit as st
from vrp_backend import DeliveryNetwork, VRPSolver

# Page configuration
st.set_page_config(page_title="VRP Optimizer", layout="wide")
st.title("🚐 Vehicle Routing Problem Optimizer")
st.markdown("The vehicle routing problem minimizes the number of vehicles needed to reach all locations without repetition (retourning to a already visited location), and within a time constraint.")
st.markdown("Select your delivery locations, configure time constraint for each van, select number of available vans and calculate the optimal routes. Retourning to Heathrow does not add to the time constraint.")

# Session state keeps the network(and new locations loaded.
if 'network' not in st.session_state:
    network = DeliveryNetwork(depot='Heathrow')
    list_locations = [
        'Harrow',
        'Ealing',
        'Holborn',
        'Sutton',
        'Dartford',
        'Bromley',
        'Greenwich',
        'Barking',
        'Hammersmith',
        'Kingston',
        'Richmond',
        'Battersea',
        'Islington',
        'Woolwich'
    ]
    
    edges = [
        # Heathrow connections
        ('Heathrow', 'Harrow', 20),
        ('Heathrow', 'Ealing', 25),
        ('Heathrow', 'Holborn', 35),
        ('Heathrow', 'Sutton', 65),
        ('Heathrow', 'Dartford', 90),
        ('Heathrow', 'Bromley', 85),
        ('Heathrow', 'Greenwich', 80),
        ('Heathrow', 'Barking', 86),
        ('Heathrow', 'Hammersmith', 25),
        ('Heathrow', 'Kingston', 35),
        ('Heathrow', 'Richmond', 20),
        ('Heathrow', 'Battersea', 44),
        ('Heathrow', 'Islington', 35),
        ('Heathrow', 'Woolwich', 82),

        # Harrow connections
        ('Harrow', 'Ealing', 15),
        ('Harrow', 'Holborn', 35),
        ('Harrow', 'Sutton', 60),
        ('Harrow', 'Dartford', 55),
        ('Harrow', 'Bromley', 57),
        ('Harrow', 'Greenwich', 85),
        ('Harrow', 'Barking', 90),
        ('Harrow', 'Hammersmith', 25),
        ('Harrow', 'Kingston', 35),
        ('Harrow', 'Richmond', 30),
        ('Harrow', 'Battersea', 37),
        ('Harrow', 'Islington', 20),
        ('Harrow', 'Woolwich', 40),

        # Ealing connections
        ('Ealing', 'Holborn', 30),
        ('Ealing', 'Sutton', 50),
        ('Ealing', 'Dartford', 70),
        ('Ealing', 'Bromley', 55),
        ('Ealing', 'Greenwich', 50),
        ('Ealing', 'Barking', 65),
        ('Ealing', 'Hammersmith', 10),
        ('Ealing', 'Kingston', 25),
        ('Ealing', 'Richmond', 15),
        ('Ealing', 'Battersea', 24),
        ('Ealing', 'Islington', 20),
        ('Ealing', 'Woolwich', 90),

        # Holborn connections
        ('Holborn', 'Sutton', 45),
        ('Holborn', 'Dartford', 60),
        ('Holborn', 'Bromley', 53),
        ('Holborn', 'Greenwich', 55),
        ('Holborn', 'Barking', 47),
        ('Holborn', 'Hammersmith', 12),
        ('Holborn', 'Kingston', 22),
        ('Holborn', 'Richmond', 20),
        ('Holborn', 'Battersea', 12),
        ('Holborn', 'Islington', 10),
        ('Holborn', 'Woolwich', 21),

        # Sutton connections
        ('Sutton', 'Dartford', 46),
        ('Sutton', 'Bromley', 15),
        ('Sutton', 'Greenwich', 45),
        ('Sutton', 'Barking', 75),
        ('Sutton', 'Hammersmith', 25),
        ('Sutton', 'Kingston', 11),
        ('Sutton', 'Richmond', 19),
        ('Sutton', 'Battersea', 15),
        ('Sutton', 'Islington', 25),
        ('Sutton', 'Woolwich', 25),

        # Dartford connections
        ('Dartford', 'Bromley', 15),
        ('Dartford', 'Greenwich', 15),
        ('Dartford', 'Barking', 25),
        ('Dartford', 'Hammersmith', 45),
        ('Dartford', 'Kingston', 65),
        ('Dartford', 'Richmond', 53),
        ('Dartford', 'Battersea', 43),
        ('Dartford', 'Islington', 63),
        ('Dartford', 'Woolwich', 70),

        # Bromley connections
        ('Bromley', 'Greenwich', 17),
        ('Bromley', 'Barking', 25),
        ('Bromley', 'Hammersmith', 41),
        ('Bromley', 'Kingston', 25),
        ('Bromley', 'Richmond', 33),
        ('Bromley', 'Battersea', 27),
        ('Bromley', 'Islington', 45),
        ('Bromley', 'Woolwich', 30),

        # Greenwich connections
        ('Greenwich', 'Barking', 25),
        ('Greenwich', 'Hammersmith', 40),
        ('Greenwich', 'Kingston', 34),
        ('Greenwich', 'Richmond', 32),
        ('Greenwich', 'Battersea', 20),
        ('Greenwich', 'Islington', 30),
        ('Greenwich', 'Woolwich', 10),

        # Barking connections
        ('Barking', 'Hammersmith', 65),
        ('Barking', 'Kingston', 70),
        ('Barking', 'Richmond', 72),
        ('Barking', 'Battersea', 61),
        ('Barking', 'Islington', 45),
        ('Barking', 'Woolwich', 13),

        # Hammersmith connections
        ('Hammersmith', 'Kingston', 20),
        ('Hammersmith', 'Richmond', 8),
        ('Hammersmith', 'Battersea', 7),
        ('Hammersmith', 'Islington', 15),
        ('Hammersmith', 'Woolwich', 25),

        # Kingston connections
        ('Kingston', 'Richmond', 5),
        ('Kingston', 'Battersea', 12),
        ('Kingston', 'Islington', 45),
        ('Kingston', 'Woolwich', 65),

        # Richmond connections
        ('Richmond', 'Battersea', 14),
        ('Richmond', 'Islington', 34),
        ('Richmond', 'Woolwich', 56),

        # Battersea connections
        ('Battersea', 'Islington', 30),
        ('Battersea', 'Woolwich', 40),

        # Islington connections
        ('Islington', 'Woolwich', 27)
    ]

    network.load_initial_network(list_locations, edges)
    st.session_state.network = network



# New location UI
with st.sidebar:
    st.header("➕ Add New Location")
    st.info("Name must be a continuous string without spaces (e.g., 'NewName'). All times must be integers >= 1.")
    
    # Use a form so the app doesn't rerun on every single keystroke
    with st.form("add_location_form"):
        new_loc_name = st.text_input("New Location Name")
        st.write("Time to existing locations (minutes):")
        
        # Dynamically generate input fields for all currently existing locations
        new_distances = {}
        for loc in st.session_state.network.locations:
            new_distances[loc] = st.number_input(f"To {loc}", min_value=1, value=15, step=1)
            
        submitted = st.form_submit_button("Add Location to Network")
        
        if submitted:
            try:
                # The validation logic exists in the backend and the errors are caught here
                st.session_state.network.add_new_location(new_loc_name, new_distances)
                st.success(f"Successfully added '{new_loc_name}'!")
                st.rerun()   # refresh the app to update the checkboxes below.
            except ValueError as e:
                st.error(f"Input Error: {e}")

# Routing configuration
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. Select Delivery Locations")
    # Multiselect
    selected_locations = st.multiselect(
        "Choose locations for today's routes (Heathrow is included automatically):",
        options=st.session_state.network.locations,
        default=st.session_state.network.locations   # default selects all.
    )
    
    # Live distance matrix
    if selected_locations:
        # Fetch the matrix dynamically based on current selection
        active_locs, cost_matrix = st.session_state.network.get_subnetwork(selected_locations)
        
        matrix_df = pd.DataFrame(cost_matrix, index=active_locs, columns=active_locs)
        
        # Format the matrix to strings to manipulate the text
        matrix_df = matrix_df.astype(str)
        
        for col in matrix_df.columns:
            matrix_df[col] = matrix_df[col].apply(lambda x: x.replace('.0', '') if x.endswith('.0') else x)   # remove ".0" from floats.
        
        for i in range(len(active_locs)):
            matrix_df.iloc[i, i] = ""   # clear the diagonal.

        matrix_df = matrix_df.replace('99999', 'N/A')

        with st.expander("📊 View Live Distance Matrix (Minutes)", expanded=True):
            st.dataframe(matrix_df, use_container_width=True)

with col2:
    st.subheader("2. Set Fleet Constraints")
    num_vans = st.slider("Number of Vans Available", min_value=1, max_value=20, value=6)
    max_time = st.slider("Max Time per Van (minutes)", min_value=30, max_value=300, value=120, step=10)

# Execution and results
st.divider()

if st.button("🚀 Solve Routing Problem", use_container_width=True, type="primary"):
    if not selected_locations:
        st.warning("Please select at least one delivery location.")
    else:
        with st.spinner("Calculating optimal routes..."):
            try:
                # Extract matrix from backend
                active_locs, cost_matrix = st.session_state.network.get_subnetwork(selected_locations)
                
                # Execute solver
                solver = VRPSolver(active_locs, cost_matrix, num_vans, max_time)
                results = solver.solve()
                
                # Display success metrics
                st.success("Optimization Successful!")
                
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                metric_col1.metric("Status", results["status"])
                metric_col2.metric("Vans Used", f'{results["vans_used"]} / {num_vans}')
                metric_col3.metric("Longest Route Time", f'{results["max_time_T"]} min')
                
                # Display active routes
                st.subheader("Active Routes")
                for route in results["routes"]:
                    st.code(route, language="markdown")
                    
            except ValueError as e:
                # Catches the unfeasible constraint error from the backend
                st.error(f"Solver Error: {e}")
