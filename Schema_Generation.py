'''
This script is used to generate a schema for the database.
Run this script to generate the schema
- Path JSON
- Database name JSON
- Main schema JSON
- Schema instruction JSON
'''

import Create_Schema
import SQL_Connector

# Create path JSON
sql_file_paths = Create_Schema.extract_sql_file_paths(save_json=True)
print("SQL file paths extracted and saved as 'sql_file_paths.json'.")
# Create database name JSON
Create_Schema.create_names_json(sql_file_paths, save_json=True)
# Create the combined schema
combined_schema = Create_Schema.create_combined_schema(sql_file_paths, save_json=True)
# Create the schema with tables and columns (TESTING)
Create_Schema.create_names_json_test(combined_schema, save_json=True)