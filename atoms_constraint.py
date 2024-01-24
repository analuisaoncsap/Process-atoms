
import re
import json

#####################################################################################################
# Reads the output.csv, identify the lines containing the target string, extractscustom strings, the user chooses the ID associated with the string and saves the IDs into a new file

def read_file_to_list(file_path):
# Create file_lines as a list
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
    return lines

file_path = 'output.csv'
file_lines = read_file_to_list(file_path)

def find_positions(lines, target_string):
# Use list to find the positions of target string
    positions = [i + 1 for i, line in enumerate(lines) if target_string in line]
    return positions

file_path = 'output.csv'
target_string = 'review_request'
file_lines = read_file_to_list(file_path)
review_request_positions = find_positions(file_lines, target_string)

def extract_custom_strings(lines):
# Use a set to store unique strings
    unique_strings = set()
    pattern = r'\b[a-z][a-z_]*[a-z]\b'
    for line in lines:
        matches = re.findall(pattern, line)
        unique_strings.update(matches)

    return list(unique_strings)

file_path = 'output.csv'
file_lines = read_file_to_list(file_path)
custom_strings = extract_custom_strings(file_lines)

def extract_custom_strings_for_ids(file_lines, positions, custom_strings):
# Create a list of sets to store unique strings for each ID
    id_lists = [set() for _ in range(len(positions))]
    pattern = r'\b[a-z][a-z_]*[a-z]\b'
    for i, position in enumerate(positions):
        line = file_lines[position - 1]
        matches = re.findall(pattern, line)
        id_lists[i].update(match for match in matches if match in custom_strings)
    id_lists = [list(id_set) for id_set in id_lists]
    return id_lists

# Create lists for each ID using review_request_positions and populate them with unique custom_strings
id_lists = extract_custom_strings_for_ids(file_lines, review_request_positions, custom_strings)

#############################################################################
# Main

def main():

    file_path = 'output.csv'
    file_lines = read_file_to_list(file_path)
    print(file_lines)
    target_string = input("Enter the target string: ")
    target_positions = find_positions(file_lines, target_string)
    custom_strings = extract_custom_strings(file_lines)
    id_lists = extract_custom_strings_for_ids(file_lines, target_positions, custom_strings)

# Print the available IDs
    print("Available IDs:")
    for i, id_list in enumerate(id_lists, 1):
        print(f"ID {i}: {id_list}")

# Get user input to choose an ID
    selected_id = input("Choose an ID (enter the corresponding number): ")

    try:
        selected_id = int(selected_id)
        if 1 <= selected_id <= len(id_lists):
            selected_id_list = id_lists[selected_id - 1]
            print(f"You selected ID {selected_id}: {selected_id_list}")

# Save the selected ID and its corresponding list to a new file in list format
            output_file_path = 'selected_id_output.txt'
            with open(output_file_path, 'w') as output_file:    
                output_file.write(f"{selected_id_list}")
            print(f'Selected ID data saved to {output_file_path}.')

# Add additional actions
        else:
            print("Invalid ID selection.")
    except ValueError:
        print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()