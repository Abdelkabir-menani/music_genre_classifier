from pydantic import BaseModel
from typing import Optional
class Music(BaseModel):
    name: str
    song: bytes  # Assuming you'll store the mp4 file as bytes in the database
    first_minute_of_the_song: bytes  # Assuming you'll store the first minute as bytes as well
    prediction_state: bool
    class_prediction: Optional[str]  # Optional if prediction_state is False
    probability: Optional[float]