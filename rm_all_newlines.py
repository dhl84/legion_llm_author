import os
from toolkit.remove_newlines import remove_newlines

input_dir = 'stories'
output_dir = 'stories/processed'

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.txt'):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        remove_newlines(input_path, output_path)

print("Processing complete.")