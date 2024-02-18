from pydub import AudioSegment
import io
from pymongo.mongo_client import MongoClient
from models.music import Music
from config.database import collection_name
from schema.schemas import list_serial
uri = "mongodb+srv://abdel9944:Svuz8WnLo5tfC2U9@cluster0.5blic6b.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

def trim_audio(input_file_as_bytes, id, duration_ms=30000):
    # Load the audio file
    input_file= io.BytesIO(input_file_as_bytes)
    audio = AudioSegment.from_file(input_file)

    # Trim the audio to the first one minute
    trimmed_audio = audio[:duration_ms]

    # Specify the output file path
    output_file = io.BytesIO()
    trimmed_audio.export(output_file, format='mp3')
    output_file.seek(0)
    trimmed_audio_bytes = output_file.read()
    song_document = collection_name.find_one({'_id': id})
    if song_document:
        # Update the document with preprocessed data
        collection_name.update_one({'_id': id }, {'$set': {'first_minute_of_the_song': trimmed_audio_bytes}})
        print("yes")
        return True
    else:
        return False  # Song not found
