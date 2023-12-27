import pandas as pd
from .PipelineGen import pipeline_gen
from .Mapping import base_table_gen

def interactive_pipeline():
    # Prompt user for file path
    file_path = input("Please enter the file path for your DataFrame: ")

    # Load DataFrame
    try:
        table = pd.read_csv(file_path)  # or pd.read_excel for Excel files
    except Exception as e:
        print(f"Failed to load DataFrame: {e}")
        return
    
    # Prompt user for file path
    file_path = input("Please enter the description for your DataFrame: ")

    # Load DataFrame
    try:
        with open(file_path, 'r') as file:
            description = file.read()
    except:
        description = file_path
    require_new = True
    # table, enum, description = base_table_gen()
    while require_new:
        print("-----------------------------")
        query = str(input("Please enter your query: "))
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("##########Feedback: ", feedback)

if __name__ == "__main__":
    interactive_pipeline()