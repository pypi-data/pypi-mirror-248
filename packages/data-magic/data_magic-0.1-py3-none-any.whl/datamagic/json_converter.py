import requests
import pandas as pd
import json

class JsonCsvConverter:

    def __init__(self, url, auth_token=None):
        self.url = url
        self.auth_token = auth_token

    def read_json_from_url(self):
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else None
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()
        return response.json()

    def convert_to_csv(self, json_data, output_file):
        df = pd.json_normalize(json_data)
        df.to_csv(output_file, index=False)

    def convert_to_json(self, json_data, output_file):
        with open(output_file, 'w') as f:
            json.dump(json_data, f)

    def convert_to_file(self, output_file, output_format='csv'):
        json_data = self.read_json_from_url()

        if output_format == 'csv':
            self.convert_to_csv(json_data, output_file)
        elif output_format == 'json':
            self.convert_to_json(json_data, output_file)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")