from flask import Flask, redirect, render_template, request, url_for
import os


app = Flask(__name__)


def read_from_txt():
    with open(os.path.realpath("request_counts.txt"), "r") as data:
        lines = data.readlines()
        all_requests = {"GET": lines[0].strip("\n")[lines[0].index(":") + 1:],
                        "POST": lines[1].strip("\n")[lines[1].index(":") + 1:],
                        "DELETE": lines[2].strip("\n")[lines[2].index(":") + 1:],
                        "PUT": lines[3].strip("\n")[lines[3].index(":") + 1:-1]}

    return all_requests


def write_to_txt(list_of_requests):
    with open(os.path.realpath("request_counts.txt"), "w") as data:
        data.write("GET:" + str(list_of_requests["GET"]) + "\n")
        data.write("POST:" + str(list_of_requests["POST"]) + "\n")
        data.write("DELETE:" + str(list_of_requests["DELETE"]) + "\n")
        data.write("PUT:" + str(list_of_requests["PUT"]) + "\"")

    return None


@app.route("/")
@app.route("/statistics")
def redirect_to_homepage():
    counters = read_from_txt()

    return render_template("homepage.html", counters=counters)


@app.route("/request-counter", methods=["GET", "POST", "DELETE", "PUT"])
def request_counter():
    counters = read_from_txt()

    counters[request.method] = int(counters[request.method]) + 1

    write_to_txt(counters)

    return redirect(url_for("redirect_to_homepage"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
