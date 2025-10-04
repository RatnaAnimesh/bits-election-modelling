
import pandas as pd
import random

# Configuration
INPUT_FILE = "/Users/ashishmishra/Downloads/hostel_data_2025.csv"
OUTPUT_STUDENTS_FILE = "/Users/ashishmishra/bits-election-simulator/data/students.csv"

CLUBS = ['Dance', 'Music', 'Debate', 'Drama', 'Photography', 'Coding', 'Finance', 'Sports', 'Literature']
INTERESTS = ['Academics', 'Campus Facilities', 'Cultural Events', 'Sports', 'Career Development']

def get_dept_from_id(bits_id):
    """Extracts a department code from the BITS ID."""
    # This is a simplified mapping. A more accurate one might be needed.
    dept_code = bits_id[4:6]
    return dept_code

def process_students_data():
    """Processes the raw hostel data to create the students.csv file."""
    print(f"Reading raw data from {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: Input file not found at {INPUT_FILE}")
        return

    print("Processing student data...")
    students_data = []
    for _, row in df.iterrows():
        bits_id = row['BITS ID']
        hostel = row['HOSTEL CODE']
        batch = int(bits_id[:4])
        dept = get_dept_from_id(bits_id)

        student = {
            'id': bits_id,
            'hostel': hostel,
            'batch': batch,
            'dept': dept,
            'clubs': random.sample(CLUBS, k=random.randint(0, 3)),
            'interests': random.sample(INTERESTS, k=random.randint(1, 3)),
            'baseline_turnout_propensity': random.uniform(0.1, 0.9),
            'slander_susceptibility': random.uniform(0.1, 0.9),
            'skepticism': random.uniform(0.1, 0.9),
            'micro_community': f"{hostel}_{dept}"
        }
        students_data.append(student)

    students_df = pd.DataFrame(students_data)
    students_df.to_csv(OUTPUT_STUDENTS_FILE, index=False)
    print(f"Successfully created {OUTPUT_STUDENTS_FILE} with {len(students_df)} students.")

def main():
    process_students_data()

if __name__ == "__main__":
    main()
