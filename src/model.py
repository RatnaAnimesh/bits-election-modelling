
from mesa import Agent, Model
from mesa.datacollection import DataCollector
import networkx as nx
import random
from src.data_schema import Misinformation, Candidate, Deal

class StudentAgent(Agent):
    """An agent representing a student in the election simulation."""
    def __init__(self, model, node_id, interests, turnout_propensity, slander_susceptibility, skepticism):
        super().__init__(model)
        self.node_id = node_id
        self.interests = interests
        self.baseline_turnout_propensity = turnout_propensity
        self.turnout_propensity = turnout_propensity
        self.slander_susceptibility = slander_susceptibility
        self.skepticism = skepticism
        self.misinformation_state = "susceptible"
        self.infected_by = None
        self.power_broker_score = random.random()
        self.deals = []
        self.opinion = {}
        self.next_opinion = None
        self.next_turnout_propensity = None

    def evaluate_manifestos(self):
        """Initial evaluation of candidate manifestos based on interests."""
        for post, candidates in self.model.candidates_by_post.items():
            self.opinion[post] = {}
            for candidate in candidates:
                # Calculate alignment score
                alignment = len(set(self.interests) & set(candidate.manifesto))
                self.opinion[post][candidate.id] = 0.5 + alignment * 0.1 # Simple linear model

    def step(self):
        """Calculates the agent's next state."""
        if self.misinformation_state == "exposed":
            self.process_exposure()
        if self.misinformation_state == "infected":
            self.spread_misinformation()
        if self.misinformation_state == "fact-checker" and self.model.rebuttal_enabled:
            self.rebut_misinformation()
        self.calculate_next_opinion()
        self.update_turnout_propensity()

    def advance(self):
        """Updates the agent's state to the one calculated in the step phase."""
        if self.next_opinion is not None:
            self.opinion = self.next_opinion
        if self.next_turnout_propensity is not None:
            self.turnout_propensity = self.next_turnout_propensity

    def process_exposure(self):
        if self.infected_by and random.random() < self.skepticism:
            self.misinformation_state = "fact-checker"
        elif self.infected_by and random.random() < self.slander_susceptibility * self.infected_by.plausibility:
            self.misinformation_state = "infected"

    def spread_misinformation(self):
        for neighbor in self.model.grid.neighbors(self.node_id):
            neighbor_agent = self.model.grid.nodes[neighbor]['agent']
            if neighbor_agent.misinformation_state == "susceptible" and random.random() < 0.2:
                neighbor_agent.misinformation_state = "exposed"
                neighbor_agent.infected_by = self.infected_by

    def rebut_misinformation(self):
        for neighbor in self.model.grid.neighbors(self.node_id):
            neighbor_agent = self.model.grid.nodes[neighbor]['agent']
            if neighbor_agent.misinformation_state in ["infected", "exposed"] and random.random() < self.skepticism * 0.5:
                neighbor_agent.misinformation_state = "susceptible"
                neighbor_agent.infected_by = None

    def calculate_next_opinion(self):
        self.next_opinion = {post: op.copy() for post, op in self.opinion.items()}
        neighbor_nodes = list(self.model.grid.neighbors(self.node_id))
        if not neighbor_nodes:
            return

        for post, candidates in self.model.candidates_by_post.items():
            avg_neighbor_opinion = {cand.id: 0.0 for cand in candidates}
            total_weight = 0

            for neighbor_node_id in neighbor_nodes:
                edge_data = self.model.grid.get_edge_data(self.node_id, neighbor_node_id)
                weight = edge_data.get('weight', 0.1)
                neighbor_agent = self.model.grid.nodes[neighbor_node_id]['agent']

                # Give more weight to seniors
                if edge_data.get('layer') == 'junior-senior':
                    weight *= 1.5

                for cand_id in avg_neighbor_opinion:
                    avg_neighbor_opinion[cand_id] += neighbor_agent.opinion[post][cand_id] * weight
                total_weight += weight

            if total_weight > 0:
                for cand_id in avg_neighbor_opinion:
                    avg_neighbor_opinion[cand_id] /= total_weight

                influence_factor = 0.1
                for cand_id in self.next_opinion[post]:
                    self.next_opinion[post][cand_id] = (1 - influence_factor) * self.opinion[post][cand_id] + influence_factor * avg_neighbor_opinion[cand_id]

        if self.misinformation_state == "infected" and self.infected_by:
            # Assuming slander targets a specific candidate, not a post for now
            for post in self.next_opinion:
                if 'cand_A' in self.next_opinion[post]: # Example: slander always targets cand_A
                    self.next_opinion[post]['cand_A'] -= self.infected_by.severity * 0.1
                    self.next_opinion[post]['cand_A'] = max(0, self.next_opinion[post]['cand_A'])

    def update_turnout_propensity(self):
        enthusiasm = 0
        for post_opinions in self.opinion.values():
            for opinion_score in post_opinions.values():
                enthusiasm += abs(opinion_score - 0.5)
        enthusiasm /= len(self.model.candidates)
        self.next_turnout_propensity = (0.8 * self.baseline_turnout_propensity) + (0.2 * enthusiasm * 2)

        # Increase turnout propensity of SSMS winners
        if self.is_ssms_winner:
            self.next_turnout_propensity *= 1.2

        self.next_turnout_propensity = max(0, min(1, self.next_turnout_propensity))

    def evaluate_deal(self, deal):
        if deal.payoff['target'] > 0.5 and not self.deals:
            self.deals.append(deal)
            self.execute_deal_effects(deal)
            return True
        return False

    def execute_deal_effects(self, deal):
        if self.next_opinion is None:
            self.next_opinion = {post: op.copy() for post, op in self.opinion.items()}
        
        for post, opinions in self.next_opinion.items():
            if deal.proposer_id in opinions:
                opinions[deal.proposer_id] = min(1.0, self.opinion[post][deal.proposer_id] + 0.2)

import pandas as pd

class ElectionModel(Model):
    """The main model for the BITS SU election simulation."""
    def __init__(self, graph: nx.Graph, rebuttal_enabled=False):
        super().__init__()
        self.grid = graph
        self.rebuttal_enabled = rebuttal_enabled
        self.posts = ["President", "General Secretary"]
        self.candidates = [
            Candidate("cand_A", "Anuj Wagh", "General Secretary", manifesto=['Academics', 'Campus Facilities']),
            Candidate("cand_B", "John Doe", "General Secretary", manifesto=['Cultural Events', 'Sports']),
            Candidate("cand_C", "Jane Smith", "President", manifesto=['Career Development', 'Academics']),
            Candidate("cand_D", "Peter Jones", "President", manifesto=['Sports', 'Campus Facilities'])
        ]
        self.candidates_by_post = {post: [c for c in self.candidates if c.post == post] for post in self.posts}
        self.misinformation = [
            Misinformation("m1", "Candidate A cheated in an exam", 0.8, 0.6, "rival_camp"),
        ]

        # Load junior-senior and SSMS election results data
        try:
            junior_senior_df = pd.read_csv("/Users/ashishmishra/bits-election-simulator/data/junior_senior.csv")
            ssms_election_results_df = pd.read_csv("/Users/ashishmishra/bits-election-simulator/data/ssms_election_results.csv")
        except FileNotFoundError:
            junior_senior_df = pd.DataFrame(columns=['junior_id', 'senior_id'])
            ssms_election_results_df = pd.DataFrame(columns=['student_id', 'post'])

        # Add junior-senior layer to the graph
        for index, row in junior_senior_df.iterrows():
            self.grid.add_edge(row['junior_id'], row['senior_id'], layer='junior-senior', weight=0.5)

        for i, node in enumerate(self.grid.nodes(data=True)):
            agent_id = node[0]
            attributes = node[1]
            interests = attributes.get('interests', [])
            if isinstance(interests, str):
                interests = eval(interests) # Convert string representation of list to actual list

            agent = StudentAgent(self, agent_id, {}, attributes.get('baseline_turnout_propensity', 0.5), attributes.get('slander_susceptibility', 0.5), attributes.get('skepticism', 0.5))
            agent.interests = interests

            # Set is_ssms_winner attribute
            if agent_id in ssms_election_results_df['student_id'].values:
                agent.is_ssms_winner = True

            self.grid.nodes[agent_id]['agent'] = agent

        self.datacollector = DataCollector(model_reporters={"Infected": lambda m: sum([1 for a in m.agents if a.misinformation_state == 'infected'])})

    def release_manifestos(self):
        print("\n--- Releasing Manifestos ---")
        self.agents.do("evaluate_manifestos")

    def slander_drop(self, misinformation_id, target_agents_ids):
        misinfo = next((m for m in self.misinformation if m.id == misinformation_id), None)
        if not misinfo:
            return
        for agent_id in target_agents_ids:
            agent = self.grid.nodes[agent_id]['agent']
            if agent.misinformation_state == "susceptible":
                agent.misinformation_state = "exposed"
                agent.infected_by = misinfo

    def propose_deals(self):
        power_brokers = [agent for agent in self.agents if agent.power_broker_score > 0.9]
        for broker in power_brokers:
            if not broker.deals:
                candidate = random.choice(self.candidates)
                deal = Deal(id=f"d_{random.randint(1000,9999)}", proposer_id=candidate.id, target_id=broker.node_id, status="proposed", payoff={'proposer': 0, 'target': random.uniform(0.4, 0.8)})
                broker.evaluate_deal(deal)

    def step(self):
        self.datacollector.collect(self)
        self.propose_deals()
        self.agents.do("step")
        self.agents.do("advance")
