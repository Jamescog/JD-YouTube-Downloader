from flask import Flask, render_template, send_file, request, redirect, flash
from flask_cors import CORS
from main import information

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
CORS(app)

# set sectrets

app.config["SECRET-KEY"] = "secret"

# set the path to the download folder
app.config["DOWNLOAD_FOLDER"] = "downloads"


@app.route("/")
def home():
    flash("Welcome")
    return render_template("index.html")


@app.route("/meta-data")
def meta_data():
    """"""
    data = information(request.args.get("url"))
    print(data)
    return data


@app.route("/download")
def download():
    itag = request.args.get("itag")
    url = request.args.get("url")

    down_url = information(url, download=True, itag=itag)
    return down_url[0]


if __name__ == "__main__":
    app.run(debug=True)
