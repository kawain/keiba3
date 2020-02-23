import time
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select

url = ""
url2 = ""

# 起動
driver = webdriver.Chrome()

# 待ち時間
driver.implicitly_wait(20)

# 指定urlを開く
driver.get(url)

#
# 最初のページ
#

# select データ6年 2019-2015年 2014年は過去履歴用
element = driver.find_element_by_name("start_year")
start_year = Select(element)
start_year.select_by_value("2014")

element = driver.find_element_by_name("start_mon")
start_mon = Select(element)
start_mon.select_by_value("1")

element = driver.find_element_by_name("end_year")
end_year = Select(element)
end_year.select_by_value("2020")

element = driver.find_element_by_name("end_mon")
end_mon = Select(element)
end_mon.select_by_value("2")

# checkbox
driver.find_element_by_id("check_Jyo_01").click()
driver.find_element_by_id("check_Jyo_02").click()
driver.find_element_by_id("check_Jyo_03").click()
driver.find_element_by_id("check_Jyo_04").click()
driver.find_element_by_id("check_Jyo_05").click()
driver.find_element_by_id("check_Jyo_06").click()
driver.find_element_by_id("check_Jyo_07").click()
driver.find_element_by_id("check_Jyo_08").click()
driver.find_element_by_id("check_Jyo_09").click()
driver.find_element_by_id("check_Jyo_10").click()

driver.find_element_by_id("check_grade_1").click()
driver.find_element_by_id("check_grade_2").click()
driver.find_element_by_id("check_grade_3").click()
driver.find_element_by_id("check_grade_4").click()
driver.find_element_by_id("check_grade_5").click()
driver.find_element_by_id("check_grade_6").click()
driver.find_element_by_id("check_grade_7").click()
driver.find_element_by_id("check_grade_8").click()
driver.find_element_by_id("check_grade_9").click()
driver.find_element_by_id("check_grade_10").click()

# select
element = driver.find_element_by_name("list")
list_ = Select(element)
list_.select_by_value("100")

# ボタンを押すためにスクロールする
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# .button の検索を探してクリックする
element = driver.find_elements_by_css_selector(".button")
for v in element:
    if v.get_attribute("value") == "検索":
        v.click()
        break


# 正規表現コンパイル
pattern = r'href="(/race/\d+?/)" title'
prog = re.compile(pattern, flags=(re.MULTILINE | re.DOTALL))

# 正規表現コンパイル
pattern2 = r"javascript:paging\('(.*?)'\)"
prog2 = re.compile(pattern2, flags=(re.MULTILINE | re.DOTALL))

# リンクを入れるリスト
url_list = []

next_page = 0


def find_next(html):
    global next_page

    # 次ページがあるかないか
    result2 = prog2.findall(html)
    for v in result2:
        if int(v) > next_page:
            next_page = int(v)
            # 次ページに行く
            driver.execute_script(f"paging('{next_page}')")
            return False

    return True


#
# 次ページ…がある間繰り返し
#
while True:
    # 待つ
    time.sleep(5)

    # 次ページのソースを取得
    html = driver.page_source

    # リンクを取得
    result = prog.findall(html)
    if result:
        for v in result:
            url_list.append(url2 + v)

    if find_next(html):
        break

driver.close()
driver.quit()


# 保存する
with open("./urls.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(url_list))


print(f"{len(url_list)}件のリンクを保存しました")
