import pandas as pd
import json

class DatabaseToCSVConverter:
    def __init__(self, connection_params):
        self.connection_params = connection_params

    def fetch_data_from_db(self, query):
        try:
            connection = pd.connect(**self.connection_params)
            data = pd.read_sql(query, connection)
            connection.close()
            return data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None

    def convert_to_csv(self, data, output_file):
        data.to_csv(output_file, index=False)

    def convert_to_json(self, data, output_file):
        data_json = data.to_dict(orient='records')
        with open(output_file, 'w') as file:
            json.dump(data_json, file)

    def convert_to_file(self, query, output_file, output_format='csv'):
        fetched_data = self.fetch_data_from_db(query)

        if fetched_data is not None:
            if output_format == 'csv':
                self.convert_to_csv(fetched_data, output_file)
            elif output_format == 'json':
                self.convert_to_json(fetched_data, output_file)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
