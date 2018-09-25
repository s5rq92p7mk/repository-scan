import os
import re
import threading

from flask import Flask, request

import functions

r = re.compile(r"^(https:\/\/github.com\/)([a-zA-Z0-9-])+(\/)([a-zA-Z0-9-_])+$")

BadRequest = "Bad request", 400

app = Flask(__name__)

@app.route("/scan", methods=["GET"])
def addScan():

    if len(request.args) != 1 or request.args.get("url") is None:
        return BadRequest

    repo_url = request.args.get("url")
    if not r.match(repo_url) is None:
        repoThread = functions.ScanThread(repo_url)
        repoThread.start()
        return "OK", 200

    else:
        return BadRequest

@app.route("/reports")
def listReports():
    reports = os.listdir(functions.report_dir)
    outputString = "<h1>Reports:</h1>"
    for report in reports:
        reportStr = report[:-4].replace(":", "/")
        outputString += functions.list_reports_template % (functions.report_path + report, reportStr)

    return outputString
