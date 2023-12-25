from .PipelineGen import pipeline_gen
from .Mapping import base_table_gen

def interactive_pipeline():
    require_new = True
    table, enum, description = base_table_gen()
    while require_new:
        query = str(input("Please enter your query: "))
        require_new, feedback = pipeline_gen(query, table, description, table_type="pd")
        if require_new:
            print("feedback: ", feedback)

if __name__ == "__main__":
    interactive_pipeline()