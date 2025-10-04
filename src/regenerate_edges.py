
import pandas as pd
import random
from itertools import combinations
from typing import List
from data_schema import Student, Edge

# Configuration
INPUT_STUDENTS_FILE = "/Users/ashishmishra/bits-election-simulator/data/students.csv"
OUTPUT_EDGES_FILE = "/Users/ashishmishra/bits-election-simulator/data/edges.csv"
AVG_FRIENDS_PER_STUDENT = 20

def create_friendship_edges(students: List[Student], avg_friends: int) -> List[Edge]:
    """Generates random friendship edges between students."""
    edges = []
    student_ids = [s['id'] for s in students]
    for student in students:
        num_friends = random.randint(1, avg_friends * 2)
        friends = random.sample(student_ids, k=min(num_friends, len(student_ids)))
        for friend_id in friends:
            if student['id'] != friend_id:
                edge = Edge(
                    source=student['id'],
                    target=friend_id,
                    layer='friendship',
                    weight=random.uniform(0.2, 1.0)
                )
                edges.append(edge)
    return edges

def create_residence_edges(students: List[dict]) -> List[Edge]:
    """Generates edges between students in the same hostel."""
    edges = []
    students_by_hostel = pd.DataFrame(students).groupby('hostel')
    for hostel, group in students_by_hostel:
        for _ in range(int(len(group) / 10)):
            wing_members = group.sample(n=min(len(group), 10))
            for u, v in combinations(wing_members['id'], 2):
                edge = Edge(source=u, target=v, layer='residence', weight=random.uniform(0.4, 0.8))
                edges.append(edge)
    return edges

def create_academic_edges(students: List[dict]) -> List[Edge]:
    """Generates edges between students in the same batch and department."""
    edges = []
    df = pd.DataFrame(students)
    students_by_academic = df.groupby(['batch', 'dept'])
    for _, group in students_by_academic:
        for u, v in combinations(group['id'], 2):
            if random.random() < 0.1:
                edge = Edge(source=u, target=v, layer='academic', weight=random.uniform(0.2, 0.6))
                edges.append(edge)
    return edges

def create_club_edges(students: List[dict]) -> List[Edge]:
    """Generates edges between students in the same clubs."""
    edges = []
    df = pd.DataFrame(students)
    # The 'clubs' column is a string representation of a list, so we need to evaluate it
    df['clubs'] = df['clubs'].apply(eval)
    df_clubs = df.explode('clubs')
    students_by_club = df_clubs.groupby('clubs')
    for _, group in students_by_club:
        for u, v in combinations(group['id'], 2):
             if random.random() < 0.4:
                edge = Edge(source=u, target=v, layer='club', weight=random.uniform(0.5, 0.9))
                edges.append(edge)
    return edges

def save_to_csv(data: List, file_path: str):
    """Saves a list of dataclass objects to a CSV file."""
    if not data:
        return
    df = pd.DataFrame([vars(d) for d in data])
    df.to_csv(file_path, index=False)
    print(f"Successfully saved {len(data)} records to {file_path}")

def main():
    """Main function to regenerate edges based on the new students.csv."""
    print(f"Reading students from {INPUT_STUDENTS_FILE}...")
    try:
        students_df = pd.read_csv(INPUT_STUDENTS_FILE)
        students = students_df.to_dict('records')
    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_STUDENTS_FILE}")
        return

    print("Generating new edges...")
    friend_edges = create_friendship_edges(students, AVG_FRIENDS_PER_STUDENT)
    residence_edges = create_residence_edges(students)
    academic_edges = create_academic_edges(students)
    club_edges = create_club_edges(students)

    all_edges = friend_edges + residence_edges + academic_edges + club_edges
    print(f"Total edges from all layers: {len(all_edges)}")

    save_to_csv(all_edges, OUTPUT_EDGES_FILE)
    print("Edge regeneration complete.")

if __name__ == "__main__":
    main()
