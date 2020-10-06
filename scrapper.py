import os
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'accept-language':'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'    
}

# obj_model = {
#   "title":None,
#   "url":None,
#   "company":None,
#   "location":None
# }

# scrap_result = {
#   "keyword":{
#     "stackoverflow":[
#       {
#         "title":title,
#         "url":url,
#         "company":company,
#         "location":location
#       }
#     ]
#   }
# }
scrap_result = {}

def sof_scrapper(keyword):
  print("find job in stackoverflow")
  search_url = f"https://stackoverflow.com/jobs?q={keyword}&r=true"
  result_list = []
  page = 1
  while True:
    print(f"page is {page}")
    res = requests.get(f"{search_url}&pg={page}")
    print(f"{search_url}&pg={page}")
    soup = BeautifulSoup(res.text, "html.parser")
    job_list_soup = soup.find_all("div", {"class":"-job"})
    if not job_list_soup:
      print("No more job")
      break
    for job in job_list_soup:
      job_a = job.find("a", {"class":"s-link"})
      if job_a:
        title = job_a.text
        url = job_a["href"]
      else:
        continue
      company = job.find("h3", {"class":"fc-black-700"}).find("span").text
      location = job.find("span", {"class":"fc-black-500"}).text
      obj = {
        "title":title.strip(),
        "url":f"http://stackoverflow.com/{url}".strip(),
        "company":company.strip(),
        "location":location.strip()
      }
      result_list.append(obj)
    page += 1

  return result_list

def wework_scrapper(keyword):
  print("find job in weworkremotely")
  weworkremote_url = f"https://weworkremotely.com/remote-jobs/search?term={keyword}"
  result_list = []
  weworkremote_res = requests.get(weworkremote_url, headers = headers)
  soup = BeautifulSoup(weworkremote_res.text, "html.parser")
  category_box = soup.find("section", {"class":"jobs"})
  job_list_soup = category_box.find_all("li", {"class":"feature"})
  for job in job_list_soup:
    try:
      title = job.find("span", {"class":"title"}).text.strip()
      url = job.select(".feature>a")[0]["href"].strip()
      company = job.find("span", {"class":"company"}).text.strip()
      location = job.find("span", {"class":"region"}).text.strip()
    except:
      continue
    obj = {
      "title":title,
      "url":f"https://weworkremotely.com/{url}",
      "company":company,
      "location":location
    }
    result_list.append(obj)
  return result_list

def remote_scrapper(keyword):
  print("find job in remoteok")
  remoteok_url = f"https://remoteok.io/remote-dev+{keyword}-jobs"
  result_list = []
  remoteok_res = requests.get(remoteok_url, headers = headers)
  soup = BeautifulSoup(remoteok_res.text, "html.parser")
  job_list_soup = soup.find_all("tr", {"class":"job"})
  for job in job_list_soup:
    time_info = job.find("time").text
    if time_info[-1] != "d":
      break
    td = job.find("td", {"class":"company_and_position_mobile"})
    title = td.find("h2")
    if title:
      title = title.text.strip()
    url = td.find("a")
    if url:
      url = url["href"].strip()
    company = td.find("h3")
    if company:
      company = company.text.strip()
    location = td.find("span", {"class":"location"})
    if location:
      location = location.text.strip()
    else:
      location = "No office location"
    obj = {
      "title":title,
      "url":f"https://remoteok.io/{url}",
      "company":company,
      "location":location
    }
    result_list.append(obj)
  return result_list

def get_expand_scrap(keyword):
  try: 
    return scrap_result[keyword]
  except:
    scrap_result[keyword] = {
      "stackoverflow":sof_scrapper(keyword),
      "weworkremotely":wework_scrapper(keyword),
      "remoteok":remote_scrapper(keyword)
    }
    return scrap_result[keyword]