# This is a OpenAI Agent test file that using the scheama information JSON files
import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import Create_Schema

# Load environment variables from .env file
load_dotenv("secret_keys.env")
openai_key = os.getenv("OPENAI_API_KEY2")
# Load metadata from JSON files (schema_data)
with open("schema_data/db_names.json", "r", encoding="utf-8") as f:
    db_names = json.load(f)

with open("schema_data/db_names_test.json", "r", encoding="utf-8") as f:
    db_names_test = json.load(f)

with open("schema_data/sql_file_paths.json", "r", encoding="utf-8") as f:
    sql_file_paths = json.load(f)

with open("schema_data/combined_schema.json", "r", encoding="utf-8") as f:
    combined_schema = json.load(f)

# Initialize OpenAI client
client = OpenAI(api_key=openai_key)

def Agent_A(user_query: str):
    # Agent A: Select best database name from the schema information JSON files

    # Output structure
    text_format = {
        "type": "json_schema",
        "name": "db_names_list",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
            "db_names": {
                "type": "array",
                "description": "List of database names as strings.",
                "items": {
                "type": "string",
                "description": "A database name.",
                "minLength": 1
                }
            }
            },
            "required": [
            "db_names"
            ],
            "additionalProperties": False
        }
    }


    Agent_A_Response = client.responses.create(
        model="gpt-5",
        reasoning={
            "summary": "detailed", # CoT reasoning summary
            "effort": "high" # Effort level for reasoning
            }, # Effort level for reasoning
        text={
            "format": text_format, # output format
            # "verbosity": "low" # Length of response
        },
        instructions="You are an AI agent that selects the possible database names based on database_names and user query. " \
            "You can have more than one database if other have a high probability to be the correct one as same as the first one" \
            "Or if a sum of the databases have a high probability to be the correct one and mutiple databases are needed to answer the user query. "\
            "If you cannot find any database name, return the names as NOT_FOUND.",
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                         "text": "Database names:\n" + "\n".join(db_names_test)
                    }
                ]
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
        store=False,
        #temperature=0, # Temperature higher means more creative response, 0 means no creativity, but GPT-5 does not support top_p
        # top_p=0, # Top-p higher means more diverse response, 0 means no diversity, but GPT-5 does not support top_p
    )
    return Agent_A_Response

def Agent_B(user_query: str, temp_schema: str):
    # Agent B: Generate SQL queries based on the schema information JSON files
    temp_schema = str(temp_schema)
    Agent_B_Response = client.responses.create(
        model="gpt-5",
        reasoning={
            "summary": "detailed",
            "effort": "high"
            },
        text={
            "format": {"type": "text"}
        },
        instructions=(
            "You are an AI agent that generates SQL query based on the provided database schema and user request. "
            "Use only the tables and columns present in the schema. "
            "final output is SQL query code, if you cannot generate a query, return string 'NOT_FOUND'. "
        ),
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Database schema:\n" + temp_schema
                    }
                ]
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
        store=False,
    )
    return Agent_B_Response

def Agent_C(user_query: str, sql_result: str, previous_reasoning: str = None):
    # Agent C: Summarize the SQL query results or keep as SQL if summarization is not possible
    sql_result = str(sql_result)
    Agent_C_Response = client.responses.create(
        model="gpt-5",
        reasoning={
            "summary": "detailed",
            "effort": "high"
        },
        text={
            "format": {"type": "text"}
        },
        instructions=(
            "You are an AI agent that receives the results of an SQL query, the previous reasoning, and a user request. "
            "Figure out if the SQL query result can be summarized or not. "
            "If the SQL query result can be summarized, return a summary of the SQL query result. "
            "If not, return the original SQL query result. If not found then return 'NOT_FOUND'. "
            "You will explain your reason before the final output. " \
            "The final output is a string that contains the summarized SQL query result or the original SQL"\
        ),
        input=[
            {
                "role": "developer",
                "content": [
                    {
                        "type": "input_text",
                        "text": "SQL query result:\n" + sql_result + "\n\n Previous Reasoning Results:" + previous_reasoning
                    }
                ]
            },
            {
                "role": "user",
                "content": user_query,
            }
        ],
        store=False,
    )
    return Agent_C_Response