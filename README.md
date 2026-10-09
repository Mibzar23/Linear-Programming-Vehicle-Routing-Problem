ENGLISH:
# 🚚 Linear-Programming-Vehicle-Routing-Problem 📦

This repository features a linear programming problem based on the book *"Model Building in Mathematical Programming."* 📚 The objective is to minimize both the time ⏱️ and the number of vehicles 🚐 required in a distribution network. This project includes the mathematical formulation, an Excel-based implementation, and a scalable interactive application. The problem description, directly extracted from the book, can be found in the PDFs in `vrp_problem` 📂.

## 🧮 Mathematical Formulation
The detailed steps for the mathematical formulation are located in the `vrp_math_sol` folder 📂. The solution is decomposed into its core components and solved using a Linear Programming solver with a rigorous mathematical approach. Additionally, an Excel implementation is provided as a user-friendly alternative, condensing the complex equations into accessible variable matrices and cells.

*(Note: The Excel implementation requires the Open Solver add-in to be executed ⚙️).*

## 🌐 Interactive Application
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://linear-programming-vehicle-routing-problem-dxcd6op6l7tbehqfvl5.streamlit.app/)

The interactive web application provides an environment where users have full control over the routing variables and fleet constraints. The underlying Python architecture is designed to be scalable, allowing for future developments such as API integrations and advanced real-time data processing.

## How to Run the Application Locally

Follow these instructions to set up and run the Streamlit application on your local machine.

### Prerequisites
* **Python 3.8+** installed on your system.

### Installation Steps

**1. Clone the repository**
```bash
git clone [https://github.com/your-username/Linear-Programming-Vehicle-Routing-Problem.git](https://github.com/Mibzar23/Linear-Programming-Vehicle-Routing-Problem.git)
```

**2. Navigate to the application folder**
```bash
cd Linear-Programming-Vehicle-Routing-Problem/vrp_app
```

**3. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**4. Install dependencies**
Install the required packages using the `requirements.txt` file. *(Note: The PuLP library is version 3.3.2 to ensure mathematical stability).*
```bash
pip install -r requirements.txt
```

**5. Launch the application**
```bash
streamlit run vrp_execution.py
```
*Once executed, your default web browser will automatically open a new tab hosting the local VRP Optimizer dashboard.* 🚀
