
import sys
import os
sys.path.append('/Users/ashishmishra/bits-election-simulator/src')

import pandas as pd
import networkx as nx
from src.model import ElectionModel

def load_graph():
    """Loads student and edge data and constructs a networkx graph."""
    print("Loading data...")
    try:
        students_df = pd.read_csv("/Users/ashishmishra/bits-election-simulator/data/students.csv")
        edges_df = pd.read_csv("/Users/ashishmishra/bits-election-simulator/data/edges.csv")
        print("Datasets loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}. Please run the data generation script first.")
        return None

    print("Constructing graph...")
    G = nx.Graph()

    for _, row in students_df.iterrows():
        G.add_node(row['id'], **row.to_dict())

    for _, row in edges_df.iterrows():
        G.add_edge(row['source'], row['target'], layer=row['layer'], weight=row['weight'])
    
    print(f"Graph constructed with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def run_scenario(graph, num_steps, rebuttal_enabled, slander_step, slander_targets):
    """Runs a single simulation scenario."""
    model = ElectionModel(graph, rebuttal_enabled=rebuttal_enabled)
    model.release_manifestos()
    for i in range(num_steps):
        if i == slander_step:
            target_agents = [agent.node_id for agent in model.agents[:slander_targets]]
            model.slander_drop("m1", target_agents)
        model.step()
    return model.datacollector.get_model_vars_dataframe(), model

import plotly.graph_objects as go

def get_opinion_df(model):
    """Extracts agent opinions into a tidy DataFrame."""
    all_opinions = []
    for agent in model.agents:
        for post, opinions in agent.opinion.items():
            for candidate_id, score in opinions.items():
                all_opinions.append({
                    'agent_id': agent.node_id,
                    'post': post,
                    'candidate': candidate_id,
                    'opinion_score': score
                })
    return pd.DataFrame(all_opinions)

def main():
    """Main function to run the Monte Carlo simulation and intervention experiment."""
    graph = load_graph()
    if graph is None:
        return

    num_steps = 10
    num_runs = 1 # For faster testing
    slander_step = 4
    slander_targets = 50

    all_control_results = []
    all_intervention_results = []
    final_control_model = None

    print(f"\n--- Running Monte Carlo Simulation ({num_runs} runs) ---")
    for run in range(num_runs):
        print(f"  Run {run + 1}/{num_runs}")
        control_results, final_control_model = run_scenario(graph, num_steps, False, slander_step, slander_targets)
        all_control_results.append(control_results['Infected'])

        intervention_results, _ = run_scenario(graph, num_steps, True, slander_step, slander_targets)
        all_intervention_results.append(intervention_results['Infected'])

    # --- Analysis & Visualization ---
    print("\n--- Generating Visualization ---")
    avg_control_infected = pd.concat(all_control_results, axis=1).mean(axis=1)
    avg_intervention_infected = pd.concat(all_intervention_results, axis=1).mean(axis=1)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=avg_control_infected.index, y=avg_control_infected, name='Control (No Rebuttal)', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=avg_intervention_infected.index, y=avg_intervention_infected, name='Intervention (Rebuttal Enabled)', mode='lines+markers'))

    fig.update_layout(
        title_text="Effectiveness of Rebuttal Intervention on Misinformation Spread",
        xaxis_title="Simulation Step",
        yaxis_title="Average Number of Infected Agents",
        legend_title="Scenario"
    )
    fig.show()

    # --- Opinion Analysis ---
    if final_control_model:
        print("\n--- Analyzing Final Opinion Distribution (Control Scenario) ---")
        opinion_df = get_opinion_df(final_control_model)
        
        for post in opinion_df['post'].unique():
            post_df = opinion_df[opinion_df['post'] == post]
            avg_opinions = post_df.groupby('candidate')['opinion_score'].mean().sort_values(ascending=False)
            print(f"\nAverage Opinion Scores for {post}:")
            print(avg_opinions)

if __name__ == "__main__":
    main()
