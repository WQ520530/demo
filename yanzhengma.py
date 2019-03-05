# coding:utf-8
import requests
import json
import time
import json


import requests
from hashlib import md5
import hashlib

class RClient(object):

    def __init__(self, username, password, soft_id, soft_key):
        self.username = username
        self.password = md5(password.encode()).hexdigest()
        self.soft_id = soft_id
        self.soft_key = soft_key
        self.base_params = {
            'username': self.username,
            'password': self.password,
            'softid': self.soft_id,
            'softkey': self.soft_key,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'User-Agent': 'ben',
        }

    def open_img(self,file_path):
        im = open(file_path,'rb').read()
        return self.rk_create(im,3040)


    def rk_create(self, im, im_type, timeout=60,):
        """
        im: 图片字节
        im_type: 题目类型
        """
        params = {
            'typeid': im_type,
            'timeout': timeout,
        }
        params.update(self.base_params)
        files = {'image': ('a.jpg', im)}
        r = requests.post('http://api.ruokuai.com/create.json', data=params, files=files, headers=self.headers)
        # print(r.json())
        print(r.json()['Result'])
        return r.json()['Result']

    def rk_report_error(self, im_id):
        """
        im_id:报错题目的ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://api.ruokuai.com/reporterror.json', data=params, headers=self.headers)
        print(r.json())
        return r.json()


if __name__ == '__main__':
    rc = RClient('账号', '密码', '1', 'key')
    rc.open_img('file_path')
