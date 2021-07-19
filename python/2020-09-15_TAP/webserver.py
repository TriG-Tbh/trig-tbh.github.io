from flask import Flask
app = Flask(__name__)

@app.route('/')
def display():
    return "Looks like it works!"

@app.route("/getAToken")
def gettoken():
    return

if __name__=='__main__':
    app.run(port=5000)