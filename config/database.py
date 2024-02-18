from pymongo.mongo_client import MongoClient
client = MongoClient("mongodb+srv://abdel9944:Svuz8WnLo5tfC2U9@cluster0.5blic6b.mongodb.net/?retryWrites=true&w=majority")
db=client.todo_db
collection_name=db['music_collection']