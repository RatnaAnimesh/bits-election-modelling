# BITS Pilani SU Election Simulator

## 1. Project Overview

This project is an end-to-end simulation and analysis platform for the BITS Pilani Student Union (SU) elections. It is designed to be a powerful tool for understanding and predicting election outcomes, as well as for optimizing campaign strategies.

The simulation is built on a sophisticated agent-based model (ABM) that represents the BITS Pilani student body as a multi-layer social network. Each student is modeled as an individual agent with unique attributes, behaviors, and social connections. The simulation then models the complex dynamics of an election, including peer influence, campaign messaging, misinformation, and deal-making.

The ultimate goal of this project is to provide a data-driven approach to election campaigning. By running thousands of Monte Carlo simulations, we can estimate the probability of different election outcomes, identify the most effective campaign strategies, and diagnose potential risks.

## 2. Features

The BITS Pilani SU Election Simulator is packed with features that make it a powerful tool for election analysis and strategy optimization.

### 2.1. Agent-Based Model

The core of the simulation is an agent-based model (ABM) that represents each student as an individual agent. Each agent has a rich set of attributes, including:

*   **Demographics:** Hostel, batch, department, and clubs.
*   **Behavioral Traits:** Turnout propensity, slander susceptibility, and skepticism.
*   **Social Connections:** A multi-layer network of social connections, including friendships, academic connections, and club memberships.

### 2.2. Multi-Layer Network

The simulation is built on a multi-layer social network that captures the complex social dynamics of the BITS Pilani student body. The network has the following layers:

*   **Residence:** Connections between students living in the same hostel.
*   **Academic:** Connections between students in the same batch and department.
*   **Clubs:** Connections between students in the same clubs.
*   **Friendship:** A layer of random friendship connections.

### 2.3. Misinformation Dynamics

The simulation includes a sophisticated model of misinformation dynamics, which allows us to study the impact of slander and fake news on election outcomes. The model includes the following features:

*   **SEIR Model:** A Susceptible-Exposed-Infected-Recovered (SEIR) model of misinformation spread.
*   **Slander Drops:** The ability to simulate targeted slander drops against specific candidates.
*   **Rebuttal Strategies:** The ability to model the effectiveness of different rebuttal strategies.

### 2.4. Deal-Making Engine

The simulation includes a deal-making engine that allows us to model the complex process of coalition building and deal-making that is a key feature of BITS Pilani SU elections. The engine includes the following features:

*   **Power Brokers:** The ability to identify and model the behavior of power brokers.
*   **Stochastic Deal-Making:** A stochastic model of deal-making, which allows us to explore a wide range of possible outcomes.
*   **Deal Effects:** The ability to model the impact of deals on voter behavior.

### 2.5. Monte Carlo Simulation

The simulation is designed to be run as a Monte Carlo simulation, which allows us to explore a wide range of possible outcomes and to estimate the probability of different election outcomes. The simulation can be run for thousands of iterations, which provides a robust estimate of the election dynamics.

## 3. Technical Architecture

The BITS Pilani SU Election Simulator is built on a modern, open-source technical stack.

### 3.1. Libraries and Frameworks

The simulation is built using the following libraries and frameworks:

*   **Mesa:** A Python framework for agent-based modeling.
*   **NetworkX:** A Python library for creating and analyzing complex networks.
*   **Pandas:** A Python library for data manipulation and analysis.
*   **NumPy:** A Python library for numerical computing.
*   **Plotly:** A Python library for interactive data visualization.

### 3.2. Project Structure

The project is structured as follows:

```
bits-election-simulator/
├── data/
│   ├── students.csv
│   └── edges.csv
├── notebooks/
│   └── 01_Network_Construction_and_Validation.ipynb
├── src/
│   ├── data_schema.py
│   ├── model.py
│   ├── process_hostel_data.py
│   └── regenerate_edges.py
├── venv/
├── .gitignore
├── README.md
├── requirements.txt
└── run_simulation.py
```

## 4. Data Schema

The simulation is based on two main data files: `students.csv` and `edges.csv`.

### 4.1. `students.csv`

The `students.csv` file contains the following information for each student:

*   `id`: A unique identifier for each student.
*   `hostel`: The student's hostel.
*   `batch`: The student's batch.
*   `dept`: The student's department.
*   `clubs`: A list of the clubs the student is a member of.
*   `baseline_turnout_propensity`: The student's baseline probability of voting.
*   `slander_susceptibility`: The student's susceptibility to misinformation.
*   `skepticism`: The student's skepticism towards information.
*   `micro_community`: The student's micro-community.
*   `interests`: A list of the student's interests.

### 4.2. `edges.csv`

The `edges.csv` file contains the following information for each social connection:

*   `source`: The source node of the edge.
*   `target`: The target node of the edge.
*   `layer`: The layer of the network the edge belongs to (e.g., `residence`, `academic`, `club`, `friendship`).
*   `weight`: The weight of the edge, which represents the strength of the connection.

## 5. Installation and Usage

To install and run the BITS Pilani SU Election Simulator, follow these steps:

1.  **Clone the repository:**

```
git clone https://github.com/RatnaAnimesh/bits-election-modelling.git
```

2.  **Create and activate a virtual environment:**

```
python -m venv venv
source venv/bin/activate
```

3.  **Install the dependencies:**

```
pip install -r requirements.txt
```

4.  **Run the simulation:**

```
python run_simulation.py
```

## 6. Simulation Workflow

The simulation workflow is as follows:

1.  **Load the data:** The simulation starts by loading the `students.csv` and `edges.csv` files.
2.  **Construct the graph:** The simulation then constructs a multi-layer social network using the NetworkX library.
3.  **Initialize the model:** The simulation then initializes the `ElectionModel` with the graph and other parameters.
4.  **Run the simulation:** The simulation then runs for a specified number of steps. At each step, the simulation updates the state of each agent based on the rules of the model.
5.  **Analyze the results:** After the simulation is complete, the results are analyzed to provide insights into the election dynamics.

## 7. Future Work

The BITS Pilani SU Election Simulator is a powerful tool, but there is always room for improvement. Here are some potential future enhancements:

*   **More sophisticated agent behaviors:** The agent behaviors could be made more sophisticated by incorporating more factors, such as personality traits and emotional states.
*   **More detailed network structures:** The network structure could be made more detailed by incorporating more layers, such as online social networks.
*   **More detailed analysis of the election results:** The analysis of the election results could be made more detailed by incorporating more metrics, such as the impact of specific campaign events.
*   **A web-based interface:** A web-based interface could be developed to make the simulation more accessible to a wider audience.

## 8. Appendices

### 8.1. Appendix A: Concrete parameter starting ranges

*   **Influence weight per layer:** residence 0.2–0.4, academic 0.15–0.3, clubs 0.2–0.35, friendships 0.3–0.5, online 0.1–0.25; normalize to 1.
*   **Misinformation transmission probability per exposure:** 0.03–0.15; rebuttal efficacy 0.2–0.6 reduction; forgetting/decay half-life 3–10 days.
*   **Deal acceptance base rate among leaders:** 0.2–0.5; spillover to members as 5–20% support bump within community cluster for 7–21 days.
*   **Turnout elasticity to enthusiasm:** 0.1–0.4; exam period turnout penalty: 5–15%.

### 8.2. Appendix B: Backtesting targets

*   Reproduce historical turnout rate distribution and known cluster skews.
*   Match observed message cascade sizes or email open rates where available.
*   Validate that simulated slander drops produce sentiment dips comparable to anecdotal peaks.

### 8.3. Appendix C: Minimal viable build checklist

*   Clean node/edge data; compute communities; validate.
*   Implement opinion + turnout core; single-layer test; sanity plots.
*   Add SEIR misinformation and one intervention (inoculation messaging).
*   Run 1000-path pilot; inspect distributions; then scale.