def individual_serial(music)->dict:
    return{
        'id':music["_id"],
        'name':str(music["name"]),
        'song':music["song"].encode(),
        'first_minute_of_the_song':music["first_minute_of_the_song"].encode(),
        'prediction_state':str(music["prediction_state"]),
        'class_prediction':str(music["class_prediction"]),
        'probability':str(music["probability"])
    }
def list_serial(songs)->list:
    return[individual_serial(music) for music in songs]
