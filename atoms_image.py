
import json
import re

#####################################################################################################
# Reads the diagram.json and extracts 'id' and 'name' pairs into a list of dictionaries.

def create_id_name_list(file_path):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
    id_name_list = []
    create_id_name_list_recursive(json_data, id_name_list)
    return id_name_list

def create_id_name_list_recursive(json_data, id_name_list, parent_id=None):
    if isinstance(json_data, list):
        for idx, item in enumerate(json_data):
            item_id = f"{parent_id}.{idx + 1}" if parent_id is not None else str(idx + 1)
            create_id_name_list_recursive(item, id_name_list, item_id)
    elif isinstance(json_data, dict):
        if 'name' in json_data:
            id_name_list.append({'id': parent_id, 'name': json_data['name']})
        for key, value in json_data.items():
            create_id_name_list_recursive(value, id_name_list, parent_id)

file_path = 'diagram.json'
result_list = create_id_name_list(file_path)
print(result_list) 

#####################################################################################################
# Remove special caracters and convert text

def clean_and_lower(text):
    return re.sub(r'[^a-zA-Z0-9]+', '', text).lower()

#####################################################################################################
# Searches for the target name, updates the corresponding background color and saves into a file

def update_bgcolour_by_names_separate_lists(json_data, target_names, target_colors, output_file_path):
    """
    Update the 'bgcolor' value associated with the 'name' key for multiple target names.

    Parameters:
    - json_data (dict or list): The JSON-like structure to search.
    - target_names (list): List of target names.
    - target_colors (list): List of corresponding bgcolors.
    - output_file_path (str): The path to save the modified JSON.

    Returns:
    - True if any 'bgcolor' is updated, False otherwise.
    """
    def update_bgcolour_recursive(data):
        updated = False
        if isinstance(data, dict):
            if 'name' in data:
                cleaned_data_name = clean_and_lower(data['name'])
                for target_name, new_bgcolour in zip(target_names, target_colors):
                    cleaned_target = clean_and_lower(target_name)
                    if cleaned_data_name == cleaned_target:
                        print(f"Found name: {data['name']}")
                        if 'bgcolor' in data:
                            data['bgcolor'] = new_bgcolour
                            print(f"Updated 'bgcolor' to: {new_bgcolour}")
                            updated = True

            for key, value in data.items():
                if update_bgcolour_recursive(value):
                    updated = True
        elif isinstance(data, list):
            for item in data:
                if update_bgcolour_recursive(item):
                    updated = True
        return updated

    if update_bgcolour_recursive(json_data):
        with open(output_file_path, 'w') as output_file:
            json.dump(json_data, output_file, indent=2)

        print(f"Updated JSON saved to {output_file_path}.")
        return True
    else:
        print("No 'bgcolor' found for any of the specified names.")
        return False

# Example usage
json_file_path = 'diagram.json'

#####################################################################################################
# Old target_names: target_names = ['assess_risks', 'calculate_terms'] # Add more target names as needed

# New target_names
def read_selected_id_output(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            # Use eval to evaluate the content as a Python literal
            target_names = eval(content)
            if isinstance(target_names, list):
                return target_names
            else:
                print(f"Invalid content in the file: {file_path}")
                return None
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

# Example usage
selected_id_output_file_path = 'selected_id_output.txt'
target_names = read_selected_id_output(selected_id_output_file_path)

# Print or use the extracted target_names
if target_names is not None:
    print("Extracted Target Names:", target_names)
else:
    print("Failed to extract target names.")

#####################################################################################################

target_colors = ['#FF8C00', '#FF8C00']  # Add more target colors as needed
output_file_path = 'output_updated.json'

with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)

update_result = update_bgcolour_by_names_separate_lists(json_data, target_names, target_colors, output_file_path)
