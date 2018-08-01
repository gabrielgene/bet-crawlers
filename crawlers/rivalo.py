import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time

def configure_driver():
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  return webdriver.Chrome(chrome_options=chrome_options)

driver = configure_driver()

site_url = "https://www.rivalo.com/en/sportsbook"

def main_page():
  print('getting...', site_url)
  driver.get(site_url)

main_page()

data = {}

driver.find_element_by_css_selector("#jq-further-0").click()
sports_driver_list = driver.find_elements_by_css_selector("#comp-navTree div ul.level_1 li a")

print("sports size", len(sports_driver_list))
for sport in sports_driver_list:
  print("clicking in sports...")
  time.sleep(2)
  sport.click()

leagues_element_list = driver.find_elements_by_css_selector("#comp-navTree div ul.level_1 li a")
leagues_list = [x.get_attribute("href") for x in leagues_element_list]


list_a = leagues_list[:len(leagues_list)//2]
list_b = leagues_list[len(leagues_list)//2:]

i = 0

last_url = ''
print("Results: ", len(leagues_list))
for league_url in list_b:
  if last_url == league_url:
    continue
  last_url = league_url

  print("getting...", league_url)
  driver.get(league_url)
  time.sleep(3)

  league_name = ""
  m = re.search("sportsbook\/([^\/]+)", league_url)
  if m:
    league_name = m.group(1)

  matches_list = []
  matches = driver.find_elements_by_css_selector(".jq-compound-event-block .e_active .jq-event-row-cont")
  print("getting data...")
  for match in matches:
    matches_data = {}
    match_data_list = match.text.strip().splitlines()
    print('>>>>>>>>>>>>>')
    print(match_data_list)
    if len(match_data_list) < 6:
      break
    matches_data["home"] = match_data_list[2]
    matches_data["visitant"] = match_data_list[3]

    matches_data["home_odd"] = match_data_list[4]
    matches_data["draw_odd"] = match_data_list[5]
    matches_data["visitant_odd"] = match_data_list[6]

    matches_list.append(matches_data)

  data[league_name] = matches_list
  print("waiting...")
  main_page()
  time.sleep(5)
  i = i + 1

with open('rivalo.json', 'w', encoding='utf-8') as outfile:
  json.dump(data, outfile, ensure_ascii=False)

driver.close()
