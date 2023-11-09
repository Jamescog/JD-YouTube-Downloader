from flask import Flask, render_template, send_file, request, make_response, jsonify
from flask_cors import CORS
import emoji
from main import information
from pytube.exceptions import AgeRestrictedError, RegexMatchError

app = Flask(__name__)
app.config["DEBUG"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config[
    "SECRET_KEY"
] = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcb"

CORS(app)
# set the path to the download folder
app.config["DOWNLOAD_FOLDER"] = "downloads"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/meta-data")
def meta_data():
    """"""
    try:
        data = information(request.args.get("url"))
    except AgeRestrictedError:
        return make_response(
            jsonify(
                {
                    "message": "This video is so exclusive, it's got a bouncer! Sorry, can't sneak you in, it's past its bedtime!",
                    "title": "Age Restriction Alert!",
                }
            ),
            400,
        )

    except RegexMatchError:
        return make_response(
            jsonify(
                {
                    "message": "Oh, so you thought any old string could pass as a YouTube URL? Cute... 😏",
                    "title": "Invalid URL. Nice try though! 🙃",
                }
            ),
            400,
        )


@app.route("/download")
def download():
    itag = request.args.get("itag")
    url = request.args.get("url")

    down_url = information(url, download=True, itag=itag)
    return down_url[0]


if __name__ == "__main__":
    app.run(debug=True)
p
