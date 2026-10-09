""" VEHICLE ROUTING PROBLEM """

"""This is  an implementation of the Vehicle Routing Problem (VRP) using Linear Programming (LP)."""

import pulp
import numpy as np

class DeliveryNetwork:
    """Manages the locations, distance matrix, and user input validations."""
    
    def __init__(self, depot="Heathrow"):
        self.depot = depot
        self.locations = [depot]
        self.edges = {}
        
    def load_initial_network(self, locations_list, edges_list):
        """Loads the default starting locations and distances."""

        self.locations.extend(locations_list)
        for loc1, loc2, dist in edges_list:
            self._add_edge(loc1, loc2, dist)

    def _add_edge(self, loc1, loc2, dist):
        """Helper to store undirected edges uniformly."""

        key = tuple(sorted([loc1, loc2]))
        self.edges[key] = dist

    def add_new_location(self, new_name, distances):
        """Adds a user-defined location with validations."""

        # Name format (no spaces or special characters)
        if not new_name.isalnum():
            raise ValueError(
                f"Invalid name '{new_name}'. The name can only be a continuous string "
                "without special characters or spaces. Suggestion: use 'NewName' format."
            )
            
        # Duplicate check
        existing_names_upper = [loc.upper() for loc in self.locations]
        if new_name.upper() in existing_names_upper:
            raise ValueError(f"Location '{new_name}' already exists in the network.")
            
        # Integer check >= 1
        for loc, dist in distances.items():
            if not isinstance(dist, int) or dist < 1:
                raise ValueError(
                    f"Distance to {loc} must be an integer equal to or greater than 1. "
                    f"Received: {dist}"
                )

        # Apply the new location and its distances to the network
        self.locations.append(new_name)
        for loc, dist in distances.items():
            self._add_edge(new_name, loc, dist)

    def get_subnetwork(self, selected_locations):
        """Generates the locations list and symmetric cost matrix for a user's selection."""

        if self.depot not in selected_locations:
            selected_locations = [self.depot] + selected_locations
            
        n = len(selected_locations)
        c = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    loc1, loc2 = selected_locations[i], selected_locations[j]
                    key = tuple(sorted([loc1, loc2]))
                    if key in self.edges:
                        c[i, j] = self.edges[key]
                    else:
                        c[i, j] = 99999    # fallback penalty for missing edge data.
                        
        return selected_locations, c


class VRPSolver:
    """Constructs and solves the Single-Commodity Flow VRP Model."""
    
    def __init__(self, locations, cost_matrix, num_vehicles, max_time):
        self.locations = locations
        self.c = cost_matrix
        self.n = len(locations)
        self.num_vehicles = num_vehicles
        self.max_time = max_time
        self.model = pulp.LpProblem("VRP_SCF_Model", pulp.LpMinimize)
        self.M = 1000    # big M constant.

    def _build_model(self):
        # Variables
        self.x = {
            (i, j): pulp.LpVariable(f"x_{i}_{j}", cat='Binary') 
            for i in range(self.n) for j in range(self.n) if i != j
        }
        
        self.f = {
            (i, j): pulp.LpVariable(f"f_{i}_{j}", lowBound=0) 
            for i in range(self.n) for j in range(self.n) if i != j
        }
        
        self.T = pulp.LpVariable("T", lowBound=0)

        # Objective
        self.model += self.M * pulp.lpSum(self.x[0, j] for j in range(1, self.n)) + self.T, "Objective"

        # Constraints
        for j in range(1, self.n):
            self.model += pulp.lpSum(self.x[i, j] for i in range(self.n) if i != j) == 1, f"In_Degree_{j}"
            
        for i in range(1, self.n):
            self.model += pulp.lpSum(self.x[i, j] for j in range(self.n) if i != j) == 1, f"Out_Degree_{i}"

        for j in range(1, self.n):
            self.model += (pulp.lpSum(self.f[i, j] for i in range(self.n) if i != j) - 
                           pulp.lpSum(self.f[j, k] for k in range(self.n) if k != j) == 
                           pulp.lpSum(self.c[i, j] * self.x[i, j] for i in range(self.n) if i != j)), f"Flow_Cons_{j}"

        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    self.model += self.f[i, j] <= self.max_time * self.x[i, j], f"Max_Capacity_{i}_{j}"

        self.model += pulp.lpSum(self.x[0, j] for j in range(1, self.n)) <= self.num_vehicles, "Max_Vehicles"

        for j in range(1, self.n):
            self.model += self.f[0, j] <= self.T, f"Bound_T_{j}"

    def solve(self):
        """Solves the model and returns mapped routes or raises an unfeasible error."""

        self._build_model()
        
        # msg=False for deployment
        self.model.solve(pulp.PULP_CBC_CMD(msg=False))

        status = pulp.LpStatus[self.model.status]
        
        # Feasibility check based on user constraints
        if status != 'Optimal':
            raise ValueError(
                f"The constraints are unfeasible. Unable to complete the routes with "
                f"{self.num_vehicles} vans under {self.max_time} minutes."
            )

        # Gather active edges
        active_edges = []
        for i in range(self.n):
            for j in range(self.n):
                if i != j and pulp.value(self.x[i, j]) == 1.0:
                    active_edges.append((i, j))

        # Reconstruct full routes
        full_routes = []
        starting_nodes = [v for u, v in active_edges if u == 0]
        
        van_count = 1
        for start_node in starting_nodes:
            route_sequence = [self.locations[0], self.locations[start_node]]
            current_node = start_node
            
            while current_node != 0:
                next_node = next(v for u, v in active_edges if u == current_node)
                route_sequence.append(self.locations[next_node])
                current_node = next_node
                
            full_routes.append(f"Van {van_count}: " + " -> ".join(route_sequence))
            van_count += 1

        return {
            "status": status,
            "vans_used": int(sum(pulp.value(self.x[0, j]) for j in range(1, self.n))),
            "max_time_T": pulp.value(self.T),
            "routes": full_routes
        }
