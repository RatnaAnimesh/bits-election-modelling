
import random
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Student:
    """Represents a single student node in the network."""
    id: str
    hostel: str
    batch: int
    dept: str
    clubs: List[str] = field(default_factory=list)
    # Proxies for social network position
    friend_degree_proxy: int = 0
    online_reach_proxy: int = 0
    # Behavioral traits
    baseline_turnout_propensity: float = 0.5
    slander_susceptibility: float = 0.5
    skepticism: float = 0.5
    # Community label for segmentation
    micro_community: str = ""
    is_ssms_winner: bool = False
    interests: List[str] = field(default_factory=list)

@dataclass
class Candidate:
    """Represents a candidate in the election."""
    id: str
    name: str
    post: str
    credibility: float = 0.7
    speaking_capacity: int = 10 # e.g., hours per week
    media_assets: int = 100 # e.g., units of social media posts
    alliance_compatibility: Dict[str, float] = field(default_factory=dict)
    manifesto: List[str] = field(default_factory=list)

@dataclass
class Edge:
    """Represents a relationship (edge) between two students."""
    source: str
    target: str
    layer: str # e.g., 'residence', 'academic', 'club', 'friendship'
    weight: float

@dataclass
class Misinformation:
    """Represents a piece of slander or misinformation."""
    id: str
    content: str
    severity: float # 0-1 scale
    plausibility: float # 0-1 scale
    source_archetype: str # e.g., 'rival_camp', 'neutral_rumor', 'meme_page'

@dataclass
class Deal:
    """Represents a deal between two agents or an agent and a candidate."""
    id: str
    proposer_id: str
    target_id: str
    status: str # proposed, accepted, rejected
    payoff: dict # e.g., {'proposer': 0.1, 'target': 0.2}


