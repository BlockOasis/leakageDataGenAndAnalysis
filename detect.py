import pandas as pd


def input_branch_structure():
    main_branch = input("Enter the name of the main branch: ")
    branches = {main_branch: {}}

    sub_branch_names = input(f"Enter sub-branches for {main_branch} separated by commas: ").split(',')
    for sub_branch_name in sub_branch_names:
        trimmed_name = sub_branch_name.strip()
        branches[main_branch][trimmed_name] = input_branch_structure_for_sub(trimmed_name)

    return branches


def input_branch_structure_for_sub(branch_name):
    branches = {}
    sub_branch_names = input(f"Enter sub-branches for {branch_name} separated by commas (leave empty if none): ")

    if not sub_branch_names:
        return branches

    for sub_branch_name in sub_branch_names.split(','):
        trimmed_name = sub_branch_name.strip()
        branches[trimmed_name] = input_branch_structure_for_sub(trimmed_name)

    return branches


def detect_leakage(data, branches):
    leakages = []
    for index, row in data.iterrows():
        for branch, sub_branches in branches.items():
            if branch not in data.columns:
                continue

            if not sub_branches:  # Skip branches without sub-branches
                continue

            total_flow = row[branch]
            sub_branch_flow = sum([row[sub_branch] for sub_branch in sub_branches if sub_branch in data.columns])

            # Check for discrepancies in flow conservation
            discrepancy = total_flow - sub_branch_flow
            if abs(discrepancy) > 0.05 * total_flow:  # 5% threshold for leakage detection
                timestamp = row['Time_in_sec']
                leakages.append((branch, timestamp, discrepancy, total_flow))

            # Recursively check sub-branches
            leakages += detect_leakage(pd.DataFrame([row]), sub_branches)

    return leakages


def main():
    # Input the network structure
    network_structure = input_branch_structure()

    # Load the CSV data
    csv_path = input("Enter the path to the CSV file: ")
    data = pd.read_csv(csv_path)

    # Detect leakage
    leakages = detect_leakage(data, network_structure)

    if leakages:
        branch = leakages[0][0]
        start_time = leakages[0][1]
        end_time = leakages[-1][1]
        total_discrepancy = sum([entry[2] for entry in leakages])
        total_flow = sum([entry[3] for entry in leakages])
        leakage_percentage = (total_discrepancy / total_flow) * 100
        total_leaked_water = total_discrepancy * (end_time - start_time) / 60  # Convert seconds to minutes

        print(f"Leakage detected in {branch} from time {start_time} to {end_time}.")
        print(f"Leakage Percentage: {leakage_percentage:.2f}%, Total leaked water: {total_leaked_water:.2f} L")
    else:
        print("No leakage detected.")


if __name__ == "__main__":
    main()
