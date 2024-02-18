from tensorflow.keras.models import load_model
import librosa, librosa.display
import numpy as np
import math
from pymongo.mongo_client import MongoClient
from models.music import Music
from config.database import collection_name
from schema.schemas import list_serial
import soundfile as sf
import tempfile
import os
from bson import ObjectId

def predict_audio(bytes_file,id):
  classif_model=load_model("/app/model/Music_Genre_15_CNN.h5")
  #signal, sample_rate = librosa.load(bytes_file)
  signal, sample_rate = sf.read(bytes_file)
  temp_fd, temp_audio_file_path = tempfile.mkstemp(suffix='.wav')
  os.close(temp_fd)
  sf.write(temp_audio_file_path, signal, sample_rate)
  signal, sample_rate = librosa.load(temp_audio_file_path)
  num_segments=15
  num_mfcc=13
  n_fft= 2048
  TRACK_DURATION = 30
  SAMPLES_PER_TRACK = sample_rate * TRACK_DURATION
  hop_length=512
  samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
  num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)
  # process all segments of audio file
  for d in range(num_segments):
    
    # calculate start and finish sample for current segment
    start = samples_per_segment * d
    finish = start + samples_per_segment
    # extract mfcc
    mfcc = librosa.feature.mfcc(y=signal[start:finish], sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)
    mfcc = mfcc.T
    print(mfcc.shape)
    mfcc=np.reshape(mfcc, (1,87, 13, 1))
  print("predicting...")
  prediction = classif_model.predict(mfcc)
  print("Done!")
  genre_list=['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
  top_four_indices = np.argsort(prediction)[0][-4:][::-1]
  classes =[genre_list[int(i)] for i in top_four_indices]
  probabilities=[prediction[0][i] for i in top_four_indices]
  # Print the top four classes along with their probabilities
  for i in top_four_indices:
      print(f"Class {genre_list[int(i)]}: Probability {prediction[0][i]}")
  result = dict(zip(classes, probabilities))
  song_document = collection_name.find_one({'_id': ObjectId(id)})
  if song_document:
        # Update the document with preprocessed data
      collection_name.update_one({'_id': id }, {'$set': {'class_prediction': classes[0]}})
      collection_name.update_one({'_id': id }, {'$set': {'probability': float(probabilities[0])}})
      print("yes")
  else:
      print('no')  # Song not found

  return result