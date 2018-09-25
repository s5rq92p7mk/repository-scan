import os
import shutil
import threading
import time

import requests
from git import Repo

list_reports_template = "<p><a href=\"%s\">%s</a></p>"

repo_dir_template = "repos/%s:%s/"
report_path = "scanreport/"
report_dir = "report/"
report_template = report_dir + "%s:%s.txt"
offensive_terms_url = "https://raw.githubusercontent.com/s5rq92p7mk/offensive-terms-in-code/master/offensive-terms.txt"

def ScanRepo(repo_url):

    repo_url_parts = repo_url.split("/")
    repo_dir = repo_dir_template % (repo_url_parts[3], repo_url_parts[4])
    report_file = report_template % (repo_url_parts[3], repo_url_parts[4])

    if not os.path.exists(report_file) and requests.get(repo_url).status_code != 404:

        offensive_terms = requests.get(offensive_terms_url).text.split("\n")[:-1]
        Repo.clone_from(repo_url, repo_dir)

        counter = {}
        for term in offensive_terms:
            counter[term] = 0
        
        for dname, dirs, files in os.walk(repo_dir):

            if ".git" in dname:
                continue

            for fname in files:
                fpath = os.path.join(dname, fname)
                with open(fpath) as f:
                    try:
                        s = f.read()
                    except:
                        break
                for term in offensive_terms:
                    try:
                        counter[term] += s.lower().count(term)
                    except:
                        break
        
        output_string = "Repository: " + repo_url_parts[3] + "/" + repo_url_parts[4] + "\n\n"
        for count in counter:
            output_string += count + ": " + str(counter[count]) + "\n"

        output_string += "\nLast update: " + str(int(time.time()))

        f = open(report_file, "w")
        f.write(output_string)
        f.close()

        shutil.rmtree(repo_dir, ignore_errors=True)


class ScanThread(threading.Thread):
    def __init__(self, repo_url):
        self.repo_url = repo_url
        threading.Thread.__init__(self)
 
    def run(self):
        ScanRepo(self.repo_url)
