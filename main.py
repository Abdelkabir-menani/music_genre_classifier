from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
from preprocess_input import trim_audio
from inference import predict_audio
from pymongo.mongo_client import MongoClient
from config.database import collection_name
from schema.schemas import list_serial
from bson import ObjectId
import io
uri=os.getenv('URI')

# Create a new client and connect to the server
client = MongoClient(uri)
collection_name.delete_many({})
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


# Prediction function

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<html>
    <head>
        <title>Music genre classification</title>
        <link rel="stylesheet" href="/static/style.css">
        <style>
            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .file-input {
                display: flex;
                flex-direction: row;
                align-items: center;
                margin-bottom: 10px; /* Optional margin between elements */
            }
            .upload-btn {
                margin-left: 10px; /* Adjust the margin as needed */
            }
        </style>
        <script>
            function showLoadingMessage() {
                document.getElementById("loading-message").style.display = "block";
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Music genre Classifier</h1>
            <p>
                Description of the project: This is a multiclass classification project for music genres. You can upload an audio file using the below button, and the application will let you know the first 4 genres predicted using the CNN model trained using the MFCC attributes of the first 30 seconds of the song uploaded.
            </p>
            <form action="/upload/" method="post" enctype="multipart/form-data" class="file-input" onsubmit="showLoadingMessage()">
                <label>Choose a file:</label>
                <input type="file" name="file" accept=".mp3, .wav">
                <div class="upload-btn">
                    <input type="submit" value="Upload">
                </div>
            </form>
            <div id="loading-message" style="display: none;">
                Predicting...
            </div>
        </div>
    </body>
</html>
    """


@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    # Save the uploaded file
    file_content = await file.read()
    file_doc = {"name": file.filename, "song": file_content}
    id_=collection_name.insert_one(file_doc)
    song_id=id_.inserted_id 

    # Preprocess the audio file
    trim_audio(file_content,song_id)
    # Display a message indicating the completion of the preprocessing step
    message = "Preprocessing step complete!"
    print(message)
    return RedirectResponse(f"/predict/?song_id={str(song_id)}")


@app.post("/predict/", response_class=HTMLResponse)
async def predict(song_id: str):
    # Retrieve the processed audio file path
    audio_file = collection_name.find_one({"_id": ObjectId(song_id)})['first_minute_of_the_song']
    audio_file = io.BytesIO(audio_file)
    """if audio_file:
        serialized_music=list_serial(audio_file)
        song_bytes = serialized_music.get('first_minute_of_the_song')
    else:
        print("prediction error! preprocessed file not found..")"""
    # Perform the prediction
    prediction_result = predict_audio(audio_file,song_id)
    class_images = {
        "blues": "/static/img/blues.jpg",
        "classical": "/static/img/classical.jpg",
        "country": "/static/img/country.jpg",
        "disco": "/static/img/disco.jpg",
        "hiphop": "/static/img/hiphop.jpg",
        "jazz": "/static/img/jazz.jpg",
        "metal": "/static/img/metal.jpg",
        "pop": "/static/img/pop.jpg",
        "reggae": "/static/img/reggae.jpg",
        "rock": "/static/img/rock.jpg",
    }

    # Display the prediction result in a nice way using HTML
    html_result =f"""
   <html>
        <head>
            <title>Audio Classification Result</title>
            <link rel="stylesheet" href="/static/style.css">
            <style>
                .container {{
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }}
                .horizontal-list {{
                    display: flex;
                    flex-direction: row;
                    justify-content: center;
                    list-style-type: none;
                    padding: 0;
                }}
                .list-item {{
                    margin-right: 20px; /* Adjust the margin as needed */
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Audio Classification Result</h1>
                <ul class="horizontal-list">
                    {"".join(f'<li class="list-item"><img src="{class_images[key]}" alt="{key}" width="100"><br>{key}: {"{:.2%}".format(value)}</li>' for key, value in prediction_result.items())}
                </ul>
            </div>
        </body>
    </html>
    """

    return HTMLResponse(content=html_result)