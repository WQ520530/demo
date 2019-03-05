import requests
import json
import urllib.parse
import pymysql
import time
from yanzhengma import RClient
from PIL import Image
import re
import httplib2

class HuanQiu:
    def __init__(self):
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }
        super(HuanQiu,self).__init__()

    def first_page(self,url):
        #获取session
        session = requests.session()
        #访问登陆首页获取session
        respons = session.get(url=url,headers = self.headers)
        time.sleep(1)
        #通过相同session信息访问验证码生成路径获取验证码信息
        result = session.post('https://life-seller.gegejia.com/api/auth/login/validcode',headers = self.headers)
        # print(result)
        res_content = json.loads(result.content.decode())
        #获取验证码拼接路径和验证码id
        img_url= 'data:image/jpeg;base64,' + res_content['data']['base64Validcode']
        img_codeid = res_content['data']['validcodeId']
        #保存验证码
        img_path = './validationcode_img.png'
        urllib.request.urlretrieve(img_url,img_path)
        img_result = Image.open(img_path)
        print(img_result)
        # print(1)
        #调用验证码接口识别验证图片
        res = RClient('scrapy', 'scrapy123', '1', 'b40ffbee5c1cf4e38028c197eb2fc751').open_img(img_path)
        #携带参数进行登陆请求
        post_data = dict(
            password= "密码",
            username='账号',
            validcode=str(res),
            validcodeId=str(img_codeid)
        )

        data = json.dumps(post_data)

        self.headers["Content-Type"] = "application/json;charset=UTF-8"

        login_response = session.post('https://life-seller.gegejia.com/api/auth/loginWithValidcode',data=data,headers=self.headers)
        try:
            token = json.loads(login_response.content.decode())['data']['token']
            print('验证码识别成功，登陆完成')
            # print(token)

        except Exception as e:
            print('验证码识别失败，正在重新登陆')
            self.first_page('https://life-seller.gegejia.com/#/login')

        headers = {
            'authority': 'life-seller.gegejia.com',
            'method': 'POST',
            'path': '/api/order/list',
            'scheme': 'https',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-length': '175',
            'content-type': 'application/json;charset=UTF-8',
            # 'cookie': 'SERVERID=4088d0150bcb2c8835229653f81b10a7|1550739133|1550737059',
            'origin': 'https://life-seller.gegejia.com',
            'referer': 'https://life-seller.gegejia.com/',
            'token':token,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }
        # print(headers)


        #列表页获取page_number


        # print(login_response.content.decode())
        data_post = dict(
            logisticsNumber= 'null',
            mobileNumber= 'null',
            orderNumber= 'null',
            page= 1,
            pageSize= 20,
            payTimeEnd= 'null',
            payTimeStart= 'null',
            receiver= 'null',
            status= "null",
            userAccountId= 'null',
        )
        data_post = json.dumps(data_post)
        # print(data_post)
        list_page = session.post('https://life-seller.gegejia.com/api/order/list',data=data_post,headers=headers)
        print(json.loads(list_page.content.decode()))

        # login_response = session.post('https://life-seller.gegejia.com/api/auth/loginWithValidcode',data=json.dumps(post_data),headers=self.headers)
        # print(login_response.content.decode())

if __name__ == '__main__':
    hq = HuanQiu()
    hq.first_page(url='https://life-seller.gegejia.com/#/login')



