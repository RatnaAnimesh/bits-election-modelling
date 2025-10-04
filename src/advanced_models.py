
from src.model import ElectionModel
import numpy as np

class BoundedConfidenceElectionModel(ElectionModel):
    def __init__(self, graph, confidence_threshold=0.2, **kwargs):
        super().__init__(graph, **kwargs)
        self.confidence_threshold = confidence_threshold

    def calculate_next_opinion(self, agent):
        agent.next_opinion = {post: op.copy() for post, op in agent.opinion.items()}
        neighbor_nodes = list(self.grid.neighbors(agent.node_id))
        if not neighbor_nodes:
            return

        for post, candidates in self.candidates_by_post.items():
            for cand in candidates:
                # Find neighbors within the confidence threshold
                influential_neighbors = []
                for neighbor_node_id in neighbor_nodes:
                    neighbor_agent = self.grid.nodes[neighbor_node_id]['agent']
                    if abs(agent.opinion[post][cand.id] - neighbor_agent.opinion[post][cand.id]) < self.confidence_threshold:
                        influential_neighbors.append(neighbor_agent)

                if not influential_neighbors:
                    continue

                # Update opinion based on the average opinion of influential neighbors
                avg_opinion = np.mean([n.opinion[post][cand.id] for n in influential_neighbors])
                agent.next_opinion[post][cand.id] = (1 - 0.1) * agent.opinion[post][cand.id] + 0.1 * avg_opinion
