import pandas as pd

#chunk_size: no of rows to read per chunk
#chunk (DataFrame): The current chunk of data
#dict: Dictionary containing basic statistics like mean, median, etc.
class ChunkIterator:
    def __init__(self, file_path, chunk_size=100):
        self.file_path = file_path
        self.chunk_size = chunk_size
        self.reader = pd.read_csv(file_path, chunksize=chunk_size)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            chunk = next(self.reader)  #next chunk of data to be fetched
            return chunk
        except StopIteration:
            raise StopIteration #when no more data is present

    def calculate_statistics(self, chunk):
        stats = {
            "mean": chunk.mean(numeric_only=True).to_dict(),  #non-numeric data is giving warning
            "median": chunk.median(numeric_only=True).to_dict(),
            "std_dev": chunk.std(numeric_only=True).to_dict()
        }
        return stats


def process_dataset(file_path, chunk_size=100):
    chunk_iterator = ChunkIterator(file_path, chunk_size=chunk_size)

    for chunk in chunk_iterator:
        stats = chunk_iterator.calculate_statistics(chunk)
        print("Chunk statistics:", stats)


if __name__ == "__main__":
    # Replace with your dataset path
    file_path = "Mall_Customers.csv"
    process_dataset(file_path, chunk_size=50)
