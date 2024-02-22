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

``![home_page]([https://cloud.githubusercontent.com/assets/711743/25648417/57cd2c0c-2fe9-11e7-8753-b60ea2656faf.png](https://github.com/Abdelkabir-menani/music_genre_classifier/blob/main/app_images/predictions_page.png)https://github.com/Abdelkabir-menani/music_genre_classifier/blob/main/app_images/home_page_page.png)``

Predictions page:
``![predictions_page]([https://cloud.githubusercontent.com/assets/711743/25648417/57cd2c0c-2fe9-11e7-8753-b60ea2656faf.png](https://github.com/Abdelkabir-menani/music_genre_classifier/blob/main/app_images/predictions_page.png)https://github.com/Abdelkabir-menani/music_genre_classifier/blob/main/app_images/predictions_page.png)``
