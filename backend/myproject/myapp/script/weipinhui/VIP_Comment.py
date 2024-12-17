import requests,csv,time
from multiprocessing.dummy import Pool
'''
cookie中的中文去掉
修改params中的api_key,spuId
postTime为时间戳
'''


class VIP_Comment_Spider():
    def main(self):
        # for params in self.Params_list():
        #     self.Get_Comment_Data(params)
        pool = Pool(3)
        pool.map(self.Get_Comment_Data,self.Params_list()) #获取数据

    def Params_list(self):
        start_page=input("请输入开始页数：")
        end_page=input("请输入结束页数：")
        params_list=[]
        for i in range(int(start_page),int(end_page)+1):
            params = {
                "api_key": "70f71280d5d547b2a7bb370a529aeea1",
                "spuId": "1183397626621612032",
                "page": i,
                "pageSize": 10
            }
            params_list.append(params)
        return params_list

    def Get_Comment_Data(self,params):
        time.sleep(0.5)
        head = {
            "referer":"https://detail.vip.com/",
            "cookie":'vip_address=%7B%22pid%22%3A%22101103%22%2C%22cid%22%3A%22101103105%22%2C%22pname%22%3A%22%5Cu6cb3%5Cu5317%5Cu7701%22%2C%22cname%22%3A%22%5Cu90a2%5Cu53f0%5Cu5e02%22%7D; vip_province=101103;vip_city_code=101103105; vip_wh=VIP_BJ; vip_ipver=31; VIP_QR_FIRST=1; mars_pid=0; VipUINFO=luc:a|suc:a|bct:c_new|hct:c_new|bdts:0|bcts:0|kfts:0|c10:0|rcabt:0|p2:0|p3:1|p4:0|p5:0|ul:3105; user_class=a; mars_sid=5528875c0fcb6ced432cbf6453620746; PHPSESSID=9a9efg11n3nah9ua0jjtt0gr13; vip_tracker_source_from=; visit_id=79608CF64D5AB73A0AF5DBC01F4EE468; vip_access_times={"list":6,"detail":4}; pg_session_no=17; mars_cid=1616550262960_63ea57943137d7888115c8b5935ca173',
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
        }
        url="https://mapi.vip.com/vips-mobile/rest/content/reputation/queryBySpuId_for_pc?"
        text=requests.get(url=url,headers=head,params=params).json()
        for da in text["data"]:
            dic={}
            try:
                dic["authorName"]=da["reputationUser"]["authorName"]
            except:
                dic["authorName"]=""
            try:
                dic["vips"]=da["reputationUser"]["vips"]
            except:
                dic["vips"]=""
            try:
                dic["brandName"]=da["reputationProduct"]["brandName"]
            except:
                dic["brandName"]=""
            try:
                dic["discountTips"]=da["reputationProduct"]["discountTips"]
            except:
                dic["discountTips"]=""
            try:
                dic["goodsName"]=da["reputationProduct"]["goodsName"]
            except:
                dic["goodsName"]=""
            try:
                dic["vipShopPrice"]=da["reputationProduct"]["vipShopPrice"]
            except:
                dic["vipShopPrice"]=""
            try:
                dic["content"]=da["reputation"]["content"]
            except:
                dic["content"]=""
            try:
                dic["impresses"]=da["reputation"]["impresses"]
            except:
                dic["impresses"]=""
            try:
                dic["usefulCount"]=da["reputation"]["usefulCount"]
            except:
                dic["usefulCount"]=""
            try:
                dic["postTime"]=da["reputation"]["postTime"]
            except:
                dic["postTime"]=""
            with open(".//comment.csv", "a+", encoding="utf-8") as f:
                writer = csv.DictWriter(f, dic.keys())
                writer.writerow(dic)


if __name__ == "__main__":
    Spider=VIP_Comment_Spider()
    Spider.main()