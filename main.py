"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q={keyword}
https://weworkremotely.com/remote-jobs/search?term={keyword}
https://remoteok.io/remote-dev+{keyword}-jobs

Good luck!
"""
import os
from flask import Flask, render_template, request
from scrapper import get_expand_scrap
from download import download

os.system("clear")

app = Flask("Final Python")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/result")
def result():
  keyword = request.args.get("job")
  result = get_expand_scrap(keyword)
  target_sites = result.keys()
  return render_template("result.html", sites = target_sites, result = result, job=keyword)

@app.route("/download")
def download_file():
  keyword = request.args.get("job")
  return download(keyword)
  

  
  

app.run("0.0.0.0")
