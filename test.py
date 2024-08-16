import json
from uuid import uuid4

# Generate unique IDs for testing
list1_id = str(uuid4())
list2_id = str(uuid4())

# Define example lists
list1 = [{
    "key1": "value1",
    "key2": "value2"
}, {
    "key1": "value3",
    "key2": "value4"
}]

list2 = [{"keyA": "valueA", "keyB": "valueB"}]

# Initialize data
data = {list1_id: list1, list2_id: list2}


# Save initial data to JSON file
def initialize_data():
  with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)


# Define functions
def get_all_lists():
  with open('data.json', 'r') as f:
    loaded_data = json.load(f)
  print("All Lists:", loaded_data)
  return loaded_data


def set_lists(id, body):
  list_dict = get_all_lists()
  list_dict[id] = body
  with open('data.json', 'w') as f:
    json.dump(list_dict, f, indent=4)
  print(f"Updated List with ID {id}:", body)


def get_list_by_id(list_id):
  with open('data.json', 'r') as f:
    loaded_data = json.load(f)
  result = loaded_data.get(list_id, "List ID not found")
  print(f"List with ID {list_id}:", result)
  return result


# Initialize data
initialize_data()

# Test functions
print("Testing get_all_lists:")
get_all_lists()

print("\nTesting set_lists:")
# Update a list
new_list = [{"key1": "updated_value1", "key2": "updated_value2"}]
set_lists(list1_id, new_list)

print("\nTesting get_all_lists after update:")
get_all_lists()

print("\nTesting get_list_by_id with existing ID:")
get_list_by_id(list1_id)

print("\nTesting get_list_by_id with non-existing ID:")
get_list_by_id(str(uuid4()))  # Using a new UUID that doesn't exist in the file
