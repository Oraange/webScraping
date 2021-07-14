import requests
from bs4 import BeautifulSoup

LIMIT = 50

URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}&filter=0"

def extract_indeed_pages():
  result = requests.get(URL)

  soup = BeautifulSoup(result.text,"html.parser")

  start = 0
  next_bttn = soup.find("a",{"aria-label":"다음"})

  while next_bttn:
    url_next = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50&start={start*50}"

    result_next = requests.get(url_next)
    soup_next = BeautifulSoup(result_next.text, "html.parser")
    next_bttn = soup_next.find("a", {"aria-label":"다음"})

    if next_bttn==None:
      break
    start = int(start) + 1
  return start + 1

def extract_indeed_jobs(last_page):
  result = requests.get(f"{URL}&start={0*LIMIT}")
  soup = BeautifulSoup(result.text, "html.parser")

  results = soup.find_all("td",{"class":"resultContent"})

  title_list = []
  comp_list = []

  for res in results:
    h2_title = res.find_all("h2", {"class":"jobTitle"})

    for h2_item in h2_title:
      spans = h2_item.find_all("span")
      for span in spans:
        title = span.get("title")
        if title is not None:
          title_list.append(title)
      
    companys = res.find_all("span",{"class":"companyName"})

    for comp in companys:
      company = comp.string
      comp_list.append(company)
  for t in range(min(len(title_list),len(comp_list))):
    print(title_list[t], ':', comp_list[t],end='\n')