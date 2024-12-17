import requests
import json
import csv
from multiprocessing.dummy import Pool


def Get_Comment_Url():
    urls=[]
    start_page = input("请输入起始页数：")
    end_page = input("请输入结束页数：")
    for i in range(int(start_page),int(end_page)+1):
        url="https://review.suning.com/ajax/cluster_review_lists/cluster-37644362-000000012234208643-0000000000-total-%d-default-10-----reviewList.htm?callback=reviewList"%(i)
        urls.append(url)
    return urls

def Get_Comment_Data(url):
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }
    text=requests.get(url,headers=head).text.replace("reviewList(","").replace(")","")
    data=json.loads(text)
    for da in data["commodityReviews"]:
        dic={}
        try:
            dic["nickName"]=da["userInfo"]["nickName"]
        except:
            dic["nickName"]=""
        try:
            dic["levelName"]=da["userInfo"]["levelName"]
        except:
            dic["levelName"]=""
        try:
            dic["isVip"]=da["userInfo"]["isVip"]
        except:
            dic["isVip"]=""
        try:
            dic["charaterDesc1"]=da["commodityInfo"]["charaterDesc1"]
        except:
            dic["charaterDesc1"]=""
        try:
            dic["charaterDesc2"]=da["commodityInfo"]["charaterDesc2"]
        except:
            dic["charaterDesc2"]=""
        try:
            dic["content"]=da["content"]
        except:
            dic["content"]=""
        try:
            dic["publishTime"]=da["publishTime"]
        except:
            dic["publishTime"]=""
        with open(".//comment.csv", "a+", encoding="utf-8") as f:
            writer = csv.DictWriter(f, dic.keys())
            writer.writerow(dic)

if __name__ == '__main__':
    pool=Pool(3)
    pool.map(Get_Comment_Data,Get_Comment_Url())
