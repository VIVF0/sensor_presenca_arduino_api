from flask import Flask
from pymongo import MongoClient

cliente=MongoClient('mongodb://172.17.0.2:27017')
db=cliente.Sensor

app=Flask(__name__)
app.secrety_key='api_arduino'

if __name__=='__main__':
    app.run(port=5000, host='0.0.0.0',debug=True)