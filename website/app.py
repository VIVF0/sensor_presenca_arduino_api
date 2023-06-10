from flask import Flask

app=Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

if __nome__=='__main__':
    app.run(port=8085, host='0.0.0.0',debug=True)