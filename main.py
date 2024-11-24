from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from wine_data_filter import WineDataFilter  # Ensure this matches the class name in wine_data_filter.py

app = FastAPI()

wine_data = WineDataFilter("winequality-red.csv")  # Ensure this matches the class name in wine_data_filter.py

class FilterRequest(BaseModel):  # Ensure class name matches
    quality: int
    features: List[str]

@app.get('/')
def read_root():
    return {'message': "Welcome to the Wine Quality API"}

@app.post("/filter/")
def filter_wine_data(request: FilterRequest):  # Ensure class name matches
    if request.quality not in wine_data.data['quality'].unique():
        raise HTTPException(status_code=400, detail="Invalid quality value")

    # Filter the data based on quality
    filtered_data = wine_data.filter_by_quality(request.quality)  # This should now work

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="No data found for the specified quality")

    # Visualize the distribution of requested features
    image_paths = wine_data.visualize_distribution(filtered_data, request.features)

    return {
        "filtered_data": filtered_data.to_dict(orient="records"),
        "visualizations": image_paths  # Returns filtered data and paths to the saved visualizations
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
