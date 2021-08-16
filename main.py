import csv
import os
from tkinter import *

from BookingCrawler import BookingCrawler


def crawler_comment():
    if countryString.get() != "" and hotelNameString != "":
        bc = BookingCrawler()
        hotel = bc.crawler_comment(countryString.get(), hotelNameString.get())

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


app = Tk()
app.geometry('300x150')

labelCountry = Label(app, text="國家")
labelCountry.grid(column=0, row=0, sticky=W)
labelHotelName = Label(app, text="飯店英文名稱")
labelHotelName.grid(column=0, row=1, sticky=W)

countryString = StringVar()
hotelNameString = StringVar()

entryCountry = Entry(app, width=25, textvariable=countryString)
entryHotelName = Entry(app, width=25, textvariable=hotelNameString)

entryCountry.grid(column=1, row=0, padx=10)
entryHotelName.grid(column=1, row=1, padx=10)

entryCountry.insert(0, "tw")
entryHotelName.insert(0, "hong-fu-you-ya-shang-lu")

crawlerButton = Button(app, text="開始爬取", command=crawler_comment)
crawlerButton.grid(column=0, row=2, pady=10, sticky=W)

resultString = StringVar()
resultLabel = Label(app, textvariable=resultString)
resultLabel.grid(column=1, row=2, padx=10, sticky=W)

app.mainloop()
