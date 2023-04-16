#!flask/bin/python

from flask import Flask, render_template, request, redirect, session, url_for

from utils.sentinel_sat import query_SentinelAPI
from utils.file_handling import unzip_file
from utils.query_model import query_model
#from utils.env import *
import os
import numpy as np

app = Flask(__name__)
app.secret_key = "someKey"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # if not logged in, return to login page
    if 'username' not in session:
        return redirect(url_for('login'))

    # otherwise, get data from the form and use it to predict the crops after querying sentinel api for the date & location
    top_coord = request.form.get("top_coord")
    left_coord = request.form.get("left_coord")
    right_coord = request.form.get("right_coord")
    bottom_coord = request.form.get("bottom_coord")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    api_username = session["username"]
    api_password = session["password"]

    product_name = query_SentinelAPI(top_coord, left_coord, right_coord, bottom_coord, start_date, end_date, api_username, api_password)
    unzip_file(product_name)
    prediction_results = query_model(os.path.join(FILE_PATH, product_name))
    #prediction_results = np.random.randint(9, size=10980*10980).reshape(10980, 10980)
    #with open('output.txt', 'w+') as filehandle:
    # file = open("prediction.txt", "w+")  
    # content = str(prediction_results)
    # file.write(content)
    # file.close() 
    return render_template("result.html", prediction_results=prediction_results)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # save the user's username and password for future use in the same session
        username = request.form.get("username")
        password = request.form.get("password")
        session['username'] = username
        session['password'] = password
        return redirect(url_for('index'))
    else:
        return render_template("login.html")

@app.route("/logout", methods=['GET', 'POST'])
# logout user by popping session var and returning them to login page
def logout():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
