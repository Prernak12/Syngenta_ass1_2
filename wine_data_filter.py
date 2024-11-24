import pandas as pd
import matplotlib.pyplot as plt
import os

class WineDataFilter:  # Ensure this matches the usage in main.py
    def __init__(self, file_path):  # Fixed constructor method name
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.save_dir = os.path.dirname(file_path)

    def filter_by_quality(self, quality):  # Ensure this method is correctly defined
        filtered_data = self.data[self.data['quality'] == quality]  # quality(int): the wine quality to filter
        return filtered_data  # return the dataframe

    def visualize_distribution(self, filtered_data, features):
        saved_files = {}
        for feature in features:
            plt.figure(figsize=(8, 6))
            plt.hist(filtered_data[feature], bins=20, color='skyblue', edgecolor='black')
            plt.title(f'Distribution of {feature} for Quality {filtered_data["quality"].iloc[0]}')
            plt.xlabel(feature)
            plt.ylabel('Frequency')

            # Save image in the same directory as the data file
            file_path = os.path.join(self.save_dir, f'{feature}_distribution.png')
            plt.savefig(file_path)
            plt.close()
            saved_files[feature] = file_path

        return saved_files
