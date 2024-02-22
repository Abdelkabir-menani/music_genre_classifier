# music genre classifier :
This project is created to classify songs automatically to 10 different genres 'blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'.
# Model and features:
I used a CNN model with 3 convolutional layers, learning_rate=0.0001. the dataset used for training is : https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification. 
The model works on the Mel Frequency Cepstral Coefficients (MFCCs) of the audio files.
# requirements:
-python 3.8

-fast-api

-pymongo

-docker
# run:
To run the app, clone the repo and run these commands:
```
cd app
docker compose up --build
```
# app demo
Home page:

![home_page](https://github.com/Abdelkabir-menani/music_genre_classifier/assets/75325884/36dbda9e-085b-492a-afab-cf180a7d0703)

Predictions page:
![predictions_page](https://github.com/Abdelkabir-menani/music_genre_classifier/assets/75325884/d64b863f-e010-4cea-9ff3-f7addbfad763)
