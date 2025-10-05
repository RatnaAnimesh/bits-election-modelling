# BITS Pilani SU Election Simulator

## 1. Project Overview

This project is an end-to-end simulation and analysis platform for the BITS Pilani Student Union (SU) elections. It is designed to be a powerful tool for understanding and predicting election outcomes, as well as for optimizing campaign strategies.

The simulation is built on a sophisticated agent-based model (ABM) that represents the BITS Pilani student body as a multi-layer social network. Each student is modeled as an individual agent with unique attributes, behaviors, and social connections. The simulation then models the complex dynamics of an election, including peer influence, campaign messaging, misinformation, and deal-making.

The ultimate goal of this project is to provide a data-driven approach to election campaigning. By running thousands of Monte Carlo simulations, we can estimate the probability of different election outcomes, identify the most effective campaign strategies, and diagnose potential risks.

## 2. Project Status

This project is currently in the early stages of development. The following features have been implemented:

*   **Core Simulation Engine:** A basic simulation engine has been developed using the Mesa framework.
*   **Multi-Layer Network:** A multi-layer social network has been constructed using the NetworkX library.
*   **Agent-Based Model:** A simple agent-based model has been implemented with basic opinion and turnout dynamics.
*   **Advanced Opinion Dynamics:** The Bounded Confidence model has been implemented to provide a more realistic model of opinion formation.
*   **Advanced Turnout Dynamics:** A logit model of turnout has been implemented to provide a more realistic model of voter turnout.
*   **Network Analysis:** A notebook has been created to perform a more in-depth analysis of the social network.
*   **Data Integration:** The model now incorporates data on junior-senior relationships, SSMS election results, mess representatives, and AMC members.

The next steps in the project are to:

*   **Integrate the advanced dynamics models** into the main simulation engine.
*   **Implement the misinformation and deal-making modules.**
*   **Calibrate the model** using historical data.
*   **Run large-scale Monte Carlo simulations** to generate predictions and insights.

## 3. Data

### 3.1. Data Sources

The simulation is based on the following data sources:

*   **`students.csv`:** This file contains the demographic data for each student, including their hostel, batch, department, and clubs.
*   **`edges.csv`:** This file contains the social network data, including the connections between students in different layers of the network.
*   **`junior_senior.csv`:** This file contains the data on the relationships between juniors and seniors.
*   **`ssms_election_results.csv`:** This file contains the results of the SSMS elections.
*   **`mess_reps.csv`:** This file contains the data on the mess representatives.
*   **`amc_members.csv`:** This file contains the data on the AMC members.
*   **`past_hreps.csv`:** (To be created) This file will contain the data on the past H-reps.
*   **`past_mreps.csv`:** (To be created) This file will contain the data on the past M-reps.

### 3.2. Data Schema

The `Student` dataclass in `src/data_schema.py` defines the attributes of each student agent. The following attributes are currently included:

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
*   `is_ssms_winner`: A boolean that is true if the student is a winner of an SSMS election.
*   `is_mess_rep`: A boolean that is true if the student is a mess representative.
*   `is_amc_member`: A boolean that is true if the student is an AMC member.

## 4. Next Steps

The following tasks need to be completed to move the project forward:

1.  **Create the `past_hreps.csv` and `past_mreps.csv` data files.**
2.  **Update the `data_schema.py` file** to include attributes for past H-reps and M-reps.
3.  **Update the `src/model.py` file** to incorporate the new data and logic.
4.  **Update the `06_Influence_Analysis.ipynb` notebook** to analyze the influence of past H-reps and M-reps.
5.  **Integrate the advanced dynamics models** into the main simulation engine.
6.  **Implement the misinformation and deal-making modules.**
7.  **Calibrate the model** using historical data.
8.  **Run large-scale Monte Carlo simulations** to generate predictions and insights.

I will now wait for your approval before proceeding with any further actions.