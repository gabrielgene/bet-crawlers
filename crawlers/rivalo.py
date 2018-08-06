import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool
import re
import time

all_urls = [
  "https://www.rivalo.com/en/sportsbook/football/gbbab/",
  "https://www.rivalo.com/en/sportsbook/football/gbbab/",
  "https://www.rivalo.com/en/sportsbook/football-brazil/gbdcab/",
  "https://www.rivalo.com/en/sportsbook/football-international-clubs/gdjdcab/",
  "https://www.rivalo.com/en/sportsbook/football-europa-league/ggiajba/",
  "https://www.rivalo.com/en/sportsbook/football-champions-league/ggiaiba/",
  "https://www.rivalo.com/en/sportsbook/football-mexico/gbccab/",
  "https://www.rivalo.com/en/sportsbook/football-china/gjjcab/",
  "https://www.rivalo.com/en/sportsbook/football-peru/gcacab/",
  "https://www.rivalo.com/en/sportsbook/football-bolivia/gdhjcab/",
  "https://www.rivalo.com/en/sportsbook/football-colombia/gchecab/",
  "https://www.rivalo.com/en/sportsbook/football-japan/gfccab/",
  "https://www.rivalo.com/en/sportsbook/football-australia/gdecab/",
  "https://www.rivalo.com/en/sportsbook/football-russia/gcbcab/",
  "https://www.rivalo.com/en/sportsbook/football-international-youth/gdjccab/",
  "https://www.rivalo.com/en/sportsbook/football-iceland/gbacab/",
  "https://www.rivalo.com/en/sportsbook/football-germany/gdacab/",
  "https://www.rivalo.com/en/sportsbook/football-austria/gbhcab/",
  "https://www.rivalo.com/en/sportsbook/football-england/gbcab/",
  "https://www.rivalo.com/en/sportsbook/football-spain/gdccab/",
  "https://www.rivalo.com/en/sportsbook/football-italy/gdbcab/",
  "https://www.rivalo.com/en/sportsbook/football-france/ghcab/",
  "https://www.rivalo.com/en/sportsbook/football-turkey/gegcab/",
  "https://www.rivalo.com/en/sportsbook/football-germany-amateur/gbcccab/",
  "https://www.rivalo.com/en/sportsbook/football-portugal/geecab/",
  "https://www.rivalo.com/en/sportsbook/football-denmark/gicab/",
  "https://www.rivalo.com/en/sportsbook/football-switzerland/gcfcab/",
  "https://www.rivalo.com/en/sportsbook/football-uefa-nations-league/gbjahgba/",
  "https://www.rivalo.com/en/sportsbook/football-sweden/gjcab/",
  "https://www.rivalo.com/en/sportsbook/football-netherlands/gdfcab/",
  "https://www.rivalo.com/en/sportsbook/football-belgium/gddcab/",
  "https://www.rivalo.com/en/sportsbook/football-norway/gfcab/",
  "https://www.rivalo.com/en/sportsbook/football-scotland/gcccab/",
  "https://www.rivalo.com/en/sportsbook/football-argentina/geicab/",
  "https://www.rivalo.com/en/sportsbook/football-croatia/gbecab/",
  "https://www.rivalo.com/en/sportsbook/football-finland/gbjcab/",
  "https://www.rivalo.com/en/sportsbook/football-usa/gcgcab/",
  "https://www.rivalo.com/en/sportsbook/football-czech-republic/gbicab/",
  "https://www.rivalo.com/en/sportsbook/football-slovenia/gcecab/",
  "https://www.rivalo.com/en/sportsbook/football-montenegro/gdigcab/",
  "https://www.rivalo.com/en/sportsbook/football-poland/gehcab/",
  "https://www.rivalo.com/en/sportsbook/football-romania/ghhcab/",
  "https://www.rivalo.com/en/sportsbook/football-bulgaria/ghicab/",
  "https://www.rivalo.com/en/sportsbook/football-slovakia/gcdcab/",
  "https://www.rivalo.com/en/sportsbook/football-ukraine/gigcab/",
  "https://www.rivalo.com/en/sportsbook/football-hungary/gbbcab/",
  "https://www.rivalo.com/en/sportsbook/football-estonia/gjccab/",
  "https://www.rivalo.com/en/sportsbook/football-lithuania/gbgacab/",
  "https://www.rivalo.com/en/sportsbook/football-latvia/gbgdcab/",
  "https://www.rivalo.com/en/sportsbook/football-ireland/gfbcab/",
  "https://www.rivalo.com/en/sportsbook/football-northern-ireland/gbdacab/",
  "https://www.rivalo.com/en/sportsbook/football-serbia/gbfccab/",
  "https://www.rivalo.com/en/sportsbook/football-wales/gbdbcab/",
  "https://www.rivalo.com/en/sportsbook/football-georgia/gchacab/",
  "https://www.rivalo.com/en/sportsbook/football-costa-rica/gcijcab/",
  "https://www.rivalo.com/en/sportsbook/football-chile/gejcab/",
  "https://www.rivalo.com/en/sportsbook/football-ecuador/gbgfcab/",
  "https://www.rivalo.com/en/sportsbook/football-paraguay/gciacab/",
  "https://www.rivalo.com/en/sportsbook/football-uruguay/gfhcab/",
  "https://www.rivalo.com/en/sportsbook/football-venezuela/gcibcab/",
  "https://www.rivalo.com/en/sportsbook/football-south-korea/gcjbcab/",
  "https://www.rivalo.com/en/sportsbook/football-iran/gdabcab/",
  "https://www.rivalo.com/en/sportsbook/football-qatar/gdfdcab/",
  "https://www.rivalo.com/en/sportsbook/football-south-africa/gdcccab/",
  "https://www.rivalo.com/en/sportsbook/football-egypt/gdafcab/",
  "https://www.rivalo.com/en/sportsbook/football-england-amateur/gcfccab/",
  "https://www.rivalo.com/en/sportsbook/football-denmark-amateur/gjfcab/",
  "https://www.rivalo.com/en/sportsbook/football-austria-amateur/gjhcab/",
  "https://www.rivalo.com/en/sportsbook/football-norway-amateure/gjecab/",
  "https://www.rivalo.com/en/sportsbook/football-finnland-amateure/gcahcab/",
  "https://www.rivalo.com/en/sportsbook/basketball/gcbab/",
  "https://www.rivalo.com/en/sportsbook/basketball-usa/gbfcab/",
  "https://www.rivalo.com/en/sportsbook/basketball-germany/gbbbcab/",
  "https://www.rivalo.com/en/sportsbook/basketball-international/gbadcab/",
  "https://www.rivalo.com/en/sportsbook/basketball-turkey/gbbccab/",
  "https://www.rivalo.com/en/sportsbook/basketball-brazil/gcgdcab/",
  "https://www.rivalo.com/en/sportsbook/basketball-australia/gbbdcab/",
  "https://www.rivalo.com/en/sportsbook/basketball-new-zealand/gcfddba/",
  "https://www.rivalo.com/en/sportsbook/basketball-venezuela/gfgeaba/",
  "https://www.rivalo.com/en/sportsbook/basketball-dominican-rep/gbeciiba/",
  "https://www.rivalo.com/en/sportsbook/basketball-bolivia/gbifbdba/",
  "https://www.rivalo.com/en/sportsbook/tennis/gfbab/",
  "https://www.rivalo.com/en/sportsbook/tennis/gfbab/",
  "https://www.rivalo.com/en/sportsbook/tennis-atp/gdcab/",
  "https://www.rivalo.com/en/sportsbook/tennis-wta/ggcab/",
  "https://www.rivalo.com/en/sportsbook/tennis-challenger/ghccab/",
  "https://www.rivalo.com/en/sportsbook/tennis-federation-cup/ghecab/",
  "https://www.rivalo.com/en/sportsbook/tennis-davis-cup/ghgcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey/gebab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey/gebab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-germany/gebcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-usa/gdhcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-russia/gbabcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-international/gfgcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-austria/ggfcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-switzerland/gfecab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-finland/geacab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-sweden/gdjcab/",
  "https://www.rivalo.com/en/sportsbook/ice-hockey-norway/gdicab/",
  "https://www.rivalo.com/en/sportsbook/handball/ggbab/",
  "https://www.rivalo.com/en/sportsbook/handball/ggbab/",
  "https://www.rivalo.com/en/sportsbook/handball-germany/gfdcab/",
  "https://www.rivalo.com/en/sportsbook/handball-international/ghdcab/",
  "https://www.rivalo.com/en/sportsbook/handball-france/gbcbcab/",
  "https://www.rivalo.com/en/sportsbook/handball-spain/ghbcab/",
  "https://www.rivalo.com/en/sportsbook/handball-brazil/gbihhcba/",
  "https://www.rivalo.com/en/sportsbook/volleyball/gcdbab/",
  "https://www.rivalo.com/en/sportsbook/volleyball/gcdbab/",
  "https://www.rivalo.com/en/sportsbook/volleyball-international/gbdgcab/",
  "https://www.rivalo.com/en/sportsbook/baseball/gdbab/",
  "https://www.rivalo.com/en/sportsbook/baseball-usa/gbgcab/",
  "https://www.rivalo.com/en/sportsbook/baseball-mexico/gecgcab/",
  "https://www.rivalo.com/en/sportsbook/motorsport/gbbbab/",
  "https://www.rivalo.com/en/sportsbook/motorsport-formula-1/gdgcab/",
  "https://www.rivalo.com/en/sportsbook/motorsport-bikes/gfacab/",
  "https://www.rivalo.com/en/sportsbook/motorsport-nascar/gbfacab/",
  "https://www.rivalo.com/en/sportsbook/motorsport-rally/giecab/",
  "https://www.rivalo.com/en/sportsbook/boxing/gdiheddjgeehaigjbhid/",
  "https://www.rivalo.com/en/sportsbook/boxing/gdiheddjgeehaigjbhid/",
  "https://www.rivalo.com/en/sportsbook/boxing-free-fighting/gbbhba/",
  "https://www.rivalo.com/en/sportsbook/boxing-international/gdiheebedhcejcbidbeh/",
  "https://www.rivalo.com/en/sportsbook/darts/gccbab/",
  "https://www.rivalo.com/en/sportsbook/darts-international/gbaecab/",
  "https://www.rivalo.com/en/sportsbook/wc-2022/gcfjhifiiaccchbgccdg/",
  "https://www.rivalo.com/en/sportsbook/wc-2022-outright-markets/gjaaaba/",
  "https://www.rivalo.com/en/sportsbook/futsal/gcjbab/",
  "https://www.rivalo.com/en/sportsbook/futsal-brazil/gcaccab/",
  "https://www.rivalo.com/en/sportsbook/euro-2020/gjjdiba/",
  "https://www.rivalo.com/en/sportsbook/euro-2020-outright-markets/gjjejba/",
  "https://www.rivalo.com/en/sportsbook/cycling/gbhbab/",
  "https://www.rivalo.com/en/sportsbook/cycling-vuelta-a-espana/gghebba/",
  "https://www.rivalo.com/en/sportsbook/cycling-international/gjgcab/",
  "https://www.rivalo.com/en/sportsbook/rugby/gbcbab/",
  "https://www.rivalo.com/en/sportsbook/rugby-rugby-league/gidcab/",
  "https://www.rivalo.com/en/sportsbook/rugby-rugby-union/giccab/",
  "https://www.rivalo.com/en/sportsbook/snooker/gbjbab/",
  "https://www.rivalo.com/en/sportsbook/snooker-international/gffcab/",
  "https://www.rivalo.com/en/sportsbook/american-football/gbgbab/",
  "https://www.rivalo.com/en/sportsbook/american-football-usa/gedcab/",
  "https://www.rivalo.com/en/sportsbook/american-football-canada/gjdcab/",
  "https://www.rivalo.com/en/sportsbook/athletics-european-championships-2018/gbifchba/",
  "https://www.rivalo.com/en/sportsbook/athletics-european-championships-2018-men/gbifciba/",
  "https://www.rivalo.com/en/sportsbook/athletics-european-championships-2018-women/gbifdbba/",
  "https://www.rivalo.com/en/sportsbook/beach-volley/gdebab/",
  "https://www.rivalo.com/en/sportsbook/beach-volley/gdebab/",
  "https://www.rivalo.com/en/sportsbook/beach-volley-international/gcjacab/",
  "https://www.rivalo.com/en/sportsbook/table-tennis/gcabab/",
  "https://www.rivalo.com/en/sportsbook/table-tennis/gcabab/",
  "https://www.rivalo.com/en/sportsbook/table-tennis-international/giicab/",
  "https://www.rivalo.com/en/sportsbook/field-hockey/gcebab/",
  "https://www.rivalo.com/en/sportsbook/field-hockey-international/gbggcab/",
  "https://www.rivalo.com/en/sportsbook/aussie-rules/gbdbab/",
  "https://www.rivalo.com/en/sportsbook/aussie-rules-australia/gihcab/",
  "https://www.rivalo.com/en/sportsbook/pesapallo/ggbbab/",
  "https://www.rivalo.com/en/sportsbook/pesapallo-finland/gfjhcab/",
  "https://www.rivalo.com/en/sportsbook/badminton/gdbbab/",
  "https://www.rivalo.com/en/sportsbook/badminton/gdbbab/",
  "https://www.rivalo.com/en/sportsbook/badminton-international/gcfjcab/",
  "https://www.rivalo.com/en/sportsbook/cricket/gcbbab/",
  "https://www.rivalo.com/en/sportsbook/cricket/gcbbab/",
  "https://www.rivalo.com/en/sportsbook/cricket-australia/gejbcab/",
  "https://www.rivalo.com/en/sportsbook/cricket-england/gijcab/",
  "https://www.rivalo.com/en/sportsbook/cricket-international/gbafcab/",
  "https://www.rivalo.com/en/sportsbook/cricket-india/gejhcab/",
  "https://www.rivalo.com/en/sportsbook/golf/gjbab/"
]

main_url = "https://www.rivalo.com/en/sportsbook"


def instance_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    return webdriver.Chrome(chrome_options=chrome_options)


def main_page(browser, main_url):
    print('getting...', main_url)
    browser.get(main_url)


def get_leagues_list():
    browser = instance_browser()
    main_page(browser, main_url)
    browser.find_element_by_css_selector("#jq-further-0").click()
    sports_list = browser.find_elements_by_css_selector(
        "#comp-navTree div ul.level_1 li a")

    print("sports size", len(sports_list))
    for sport in sports_list:
        print("clicking in sports...")
        time.sleep(2)
        sport.click()

    leagues_element_list = browser.find_elements_by_css_selector(
        "#comp-navTree div ul.level_1 li a")
    leagues_list = [x.get_attribute("href") for x in leagues_element_list]
    browser.close()
    return leagues_list


def split_list(old_list):
    new_list = []
    new_list.append(old_list[:len(old_list)//2])
    new_list.append(old_list[len(old_list)//2:])
    return new_list


def write_file(name, data):
    with open(name + ".json", 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)


def is_hour(item):
    pattern = re.compile("\d{2}:\d{2}")
    if pattern.match(item):
        return True
    else:
        return False


def running_crawler(league_url, current_item, total_items):
    data = {}
    browser = instance_browser()
    main_page(browser, main_url)
    print("Running item: " + str(current_item) + " of " + str(total_items))
    print("getting...", league_url)
    browser.get(league_url)
    league_name = ""
    m = re.search("sportsbook\/([^\/]+)", league_url)
    if m:
        league_name = m.group(1)

    matches_list = []
    matches = browser.find_elements_by_css_selector(
        ".jq-compound-event-block .e_active .jq-event-row-cont"
    )
    load_mores = browser.find_elements_by_css_selector(
        ".jq-compound-event-block .e_active .jq-event-row-cont .t_more"
    )

    if len(load_mores) == 0:
        print("getting data...")

        for idx, match in enumerate(matches):
            match_rows = []
            matches_data = {}
            home = None
            visitant = None
            home_odd = None
            draw_odd = None
            visitant_odd = None

            match_data_list = match.text.strip().splitlines()
            match_len = len(match_data_list)
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print("league", league_url)
            print(match_data_list)

            if match_len < 6:
                continue

            if is_hour(match_data_list[0]):
                home = match_data_list[1]
                visitant = match_data_list[2]
                home_odd = match_data_list[3]
                visitant_odd = match_data_list[4]
            else:
                home = match_data_list[0]
                visitant = match_data_list[1]
                home_odd = match_data_list[2]
                draw_odd = match_data_list[3]
                visitant_odd = match_data_list[4]

            load_mores[idx].click()
            time.sleep(2)
            if idx == 0:
                load_more_heads = browser.find_elements_by_css_selector(
                    ".jq-compound-event-block .e_active .jq-event-row-cont .t_more_head"
                )[1:]
                for more_rows in load_more_heads:
                    more_rows.click()
                    time.sleep(1)

            load_match_rows = match.find_elements_by_css_selector(
                ".sp_bets .border_ccc div.t_more_row"
            )
            print("scouts: ", len(load_match_rows))

            for row in load_match_rows:
                if row.text.strip() != "":
                    print(row.text.strip().splitlines())
                    match_data_rows = row.text.strip().splitlines()
                    match_rows.append(match_data_rows)

            load_mores[idx].click()
            time.sleep(1)

            matches_data["home"] = home
            matches_data["visitant"] = visitant
            matches_data["home_odd"] = home_odd
            matches_data["draw_odd"] = draw_odd
            matches_data["visitant_odd"] = visitant_odd
            matches_data["debug"] = match_data_list
            matches_data["scout_rows"] = match_rows
            matches_list.append(matches_data)

        data[league_name] = matches_list
        data["url"] = league_url
        write_file(league_name, data)
    browser.close()


if __name__ == '__main__':
    start_time = time.time()
    # urls = get_leagues_list()
    # write_file("_league", urls)
    pool = Pool(processes=8)
    # urls = [
        #   "https://www.rivalo.com/en/sportsbook/golf/gjbab/",
            # "https://www.rivalo.com/en/sportsbook/football/gbbab/",
    #     "https://www.rivalo.com/en/sportsbook/football-germany-amateur/gbcccab/",
    #         "https://www.rivalo.com/en/sportsbook/american-football-canada/gjdcab/"
    # ]
    pool_list = []
    urls_len = len(all_urls)
    # urls_len = len(urls)
    for idx, item in enumerate(all_urls):
    # for idx, item in enumerate(urls):
        print(item)
        result = pool.apply_async(running_crawler, (item, idx, urls_len))
        pool_list.append(result)
    pool.close()
    pool.join()
    [x.get() for x in pool_list]
    print("--- %s seconds ---" % (time.time() - start_time))
