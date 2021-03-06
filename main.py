import csv
import os
import tkinter.ttk as ttk
from tkinter import *
from threading import Thread

from BookingCrawler import BookingCrawler

languageList = {'所有語言': 'all', '中文': 'zh'}


def crawler_comment(country, hotel, language):
    if country != "" and hotel != "" and language != "":
        bc = BookingCrawler()
        hotel = bc.crawler_comment(country, hotel, languageList[language])

        directory = "data/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = directory + hotel['name'] + '.csv'
        with open(filename, 'w', encoding="utf_8_sig", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["姓名", "國籍", "留言數", "評分", "留言標題", "住宿日期", "標籤", "壞留言", "好留言"])
            for lists in hotel['comment']:
                writer.writerow(lists)

        result_string = "完成"
    else:
        result_string = "國家以及飯店名稱不能為空"

    resultString.set(result_string)


def thread(args):
    t = Thread(target=crawler_comment, args=args)
    t.start()


app = Tk()
app.geometry('300x150')

labelCountry = Label(app, text="國家")
labelCountry.grid(column=0, row=0, sticky=W)
labelHotelName = Label(app, text="飯店英文名稱")
labelHotelName.grid(column=0, row=1, sticky=W)
labelLanguage = Label(app, text="選擇語言")
labelLanguage.grid(column=0, row=2, sticky=W)

countryString = StringVar()
hotelNameString = StringVar()
languageString = StringVar()

entryCountry = Entry(app, width=25, textvariable=countryString)
entryHotelName = Entry(app, width=25, textvariable=hotelNameString)
comboboxLanguage = ttk.Combobox(app, width=22, state='readonly', values=list(languageList.keys()),
                                textvariable=languageString)

entryCountry.grid(column=1, row=0, padx=10)
entryHotelName.grid(column=1, row=1, padx=10)
comboboxLanguage.grid(column=1, row=2, padx=10)

entryCountry.insert(0, "tw")
entryHotelName.insert(0, "hong-fu-you-ya-shang-lu")
comboboxLanguage.set('中文')

crawlerButton = Button(app, text="開始爬取", command=lambda: thread(
    (
        countryString.get(),
        hotelNameString.get(),
        languageString.get())
    )
)
crawlerButton.grid(column=0, row=3, pady=10, sticky=W)

resultString = StringVar()
resultLabel = Label(app, textvariable=resultString)
resultLabel.grid(column=1, row=3, padx=10, sticky=W)

app.mainloop()
