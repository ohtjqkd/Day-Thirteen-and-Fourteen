import os
import time
import csv
from flask import send_file
from scrapper import get_expand_scrap


def download(keyword):
  file_info = os.stat(f"csv/{keyword}.csv")
  if os.path.exists(f"csv/{keyword}.csv") and time.time() - file_info.st_mtime < 300:

    print(time.ctime(file_info.st_mtime))
    pass
  else:
    contents = get_expand_scrap(keyword)
    field_names = {"title":"title","url":"url","company":"company","location":"location"}
    with open(f"csv/{keyword}.csv", "w", encoding="utf-8", newline="") as file:
      csv_wr = csv.DictWriter(file,field_names)
      for key in contents.keys():
        for job in contents[key]:
          csv_wr.writerow(job)
  return send_file(f"csv/{keyword}.csv", mimetype="text/csv", as_attachment=True, cache_timeout = 0, attachment_filename=f"{keyword}.csv")