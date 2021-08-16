from bs4 import BeautifulSoup
import requests
import requests.packages.urllib3
import re
import math
from tqdm import tqdm


class BookingCrawler:
    def __init__(self):
        requests.packages.urllib3.disable_warnings()
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/92.0.4515.107 Safari/537.36'}
        return

    def crawler_comment(self, country, hotel_name):
        hotel_url = f"https://www.booking.com//reviews/{country}/hotel/{hotel_name}.zh-tw.html" + \
                    "?r_lang=all;customer_type=total;order=completed_asc;rows=25"
        hotel = {}

        try:
            o = []
            hotel_res = requests.get(hotel_url, headers=self.headers, timeout=5)
            search_hotel_result = BeautifulSoup(hotel_res.text, 'lxml')
            comment_total_count_string = search_hotel_result.find("p", class_="review_list_score_count").string
            comment_total_count = re.sub("\D", "", comment_total_count_string)
            hotel_name = search_hotel_result.find("a", class_="standalone_header_hotel_link").string
            hotel['name'] = hotel_name

            # 跑分頁回圈
            for page in tqdm(range(1, (math.ceil(int(comment_total_count) / 25) + 1))):

                get_url = hotel_url + str(";page=") + str(page)

                loop_hotel_page_res = requests.get(str(get_url), headers=self.headers, verify=False)
                loop_hotel_page_result = BeautifulSoup(loop_hotel_page_res.text, 'lxml')

                # 留言姓名
                comment_name = [name.get_text().replace('\n', "").replace('\r', "") for name in
                                loop_hotel_page_result.find_all(
                                    "p", class_="reviewer_name")]

                # 國籍
                comment_country = [country.get_text().strip('\n') for country in loop_hotel_page_result.find_all(
                    "span", class_="reviewer_country")]

                # 留言推薦
                comment_user_review_count = [re.sub("\D", "", item_user_review_count.get_text().strip(
                    '\n')) for item_user_review_count in loop_hotel_page_result.find_all("div", class_="review_item_user_review_count")]

                # 評分
                comment_review_score_badge = [score_val.get_text().replace('\n', "").replace(
                    '\r', "") for score_val in
                    loop_hotel_page_result.find_all("div", class_="review_item_header_score_container")]

                # 留言標題
                comment_content_container = [content_container.get_text().replace('\n', "").replace(
                    '\r', "") for content_container in
                    loop_hotel_page_result.find_all("div", class_="review_item_header_content_container")]

                # 填寫日期
                insertdate = [re.sub("\D", "", insert_date.get_text(
                )) for insert_date in loop_hotel_page_result.find_all("p", class_="review_item_date")]

                # 標籤
                tag = loop_hotel_page_result.find_all(
                    "ul", class_="review_item_info_tags")

                # 評語
                comment_content = loop_hotel_page_result.find_all(
                    "div", class_="review_item_review_content")

                # 到後面沒資料停止
                if len(comment_name) == 0:
                    break
                else:
                    # 迴圈跑
                    index = 0  # 跑其他list 資料index
                    for comment_contents in comment_content:
                        z = len(o)  # 尋找相同陣列 key
                        # 第一次的陣列 append
                        o.append([comment_name[index]])  # 姓名
                        o[z].append(comment_country[index])  # 國籍
                        o[z].append(
                            comment_user_review_count[index])  # 推薦數
                        o[z].append(
                            comment_review_score_badge[index])  # 評分
                        o[z].append(
                            comment_content_container[index])  # 留言標題
                        o[z].append(insertdate[index])  # 時間

                        # 標籤住房
                        tags = tag[index].find_all(
                            "li", class_='review_info_tag')
                        tag_vla_list = [tag_val.get_text().replace('•', "").replace(
                            '\n', "").replace('\r', "") for tag_val in tags]
                        tag_vla = ",".join(tag_vla_list)
                        o[z].append(tag_vla)

                        # 壞留言
                        if comment_contents.find("p", class_='review_neg') is None:
                            bad_val = ""
                        else:
                            bad_val = comment_contents.find(
                                "p", class_='review_neg').get_text().replace('\n', "").replace('\r', "")
                        o[z].append(bad_val)

                        # 好留言
                        if comment_contents.find("p", class_='review_pos') is None:
                            good_val = ""
                        else:
                            good_val = comment_contents.find(
                                "p", class_='review_pos').get_text().replace('\n', "").replace('\r', "")
                        o[z].append(good_val)

                        index = index + 1
            hotel['comment'] = o
        except requests.exceptions.RequestException as e:
            print(e)

        return hotel
