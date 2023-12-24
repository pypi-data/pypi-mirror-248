import os
import requests
import tarfile
import networkx as nx
from scipy.io import mmread

class mtx_fetcher:
    def __init__(self, url):
        self.url = url
        self.local_filename = 'data_file.tar.gz'
        self.extract_folder = 'extracted_data'

        # Create the extraction folder if it doesn't exist
        os.makedirs(self.extract_folder, exist_ok=True)

    def download_and_extract(self):
        response = requests.get(self.url)

        # Save the tar file
        with open(self.local_filename, 'wb') as file:
            file.write(response.content)

        # Extract the contents
        with tarfile.open(self.local_filename, 'r') as tar:
            tar.extractall(self.extract_folder)

    def find_matrix_market_file(self):
        for root, dirs, files in os.walk(self.extract_folder):
            for filename in files:
                if filename.endswith(".mtx") and "coord" not in filename:
                    return os.path.join(root, filename)

    def load_matrix_market_to_networkx(self, filename):
        matrix = mmread(filename)
        print("Matrix Shape:", matrix.shape)
        graph = nx.from_scipy_sparse_array(matrix, create_using=nx.Graph)
        return graph

    def fetch_and_load(self):
        self.download_and_extract()
        matrix_market_file = self.find_matrix_market_file()

        if matrix_market_file:
            graph = self.load_matrix_market_to_networkx(matrix_market_file)

            # Print basic information about the graph
            print("Number of nodes:", graph.number_of_nodes())
            print("Number of edges:", graph.number_of_edges())
            return graph
        else:
            print("Matrix Market file not found in the extracted folder.")
            return None
