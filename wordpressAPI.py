# -*- coding: utf-8 -*-
import _config as conf
import requests
import json

class Wordpy():
    def __init__(self, token):
        self.token = token
        self.headers = {
            'Authorization': 'Bearer ' + self.token
        }
        self.media_headers = {
            'Authorization': 'Bearer ' + self.token,
            'content-type': 'mutipart/form-data'
        }

        self.set_id()
        self.set_site_id()

    def set_id(self):
        user = self.users()
        self.id = user['ID']
        return self.id

    def set_site_id(self):
        # get user site link
        user = self.users()
        get_url = user['meta']['links']['site']

        r = requests.get(get_url, headers=self.headers)
        res = json.loads(r.text)
        self.site_id = res['ID']
        return self.site_id

    # GET /me
    def users(self):
        r = requests.get('https://public-api.wordpress.com/rest/v1/me/?pretty=1', headers=self.headers)
        res = json.loads(r.text)
        return res

    # POST /sites/$site/posts/new
    def create_post(self, title=None, categories=None, content=None, img=None):
        # prepare data
        payload = dict()
        payload['title'] = title
        payload['categories'] = categories
        payload['content'] = content
        

        imgload = dict()
        if img != None:
            imgload['media[]'] = open(img, 'rb')

        # build post url
        post_url = 'https://public-api.wordpress.com/rest/v1/sites/' + str(self.site_id) + '/posts/new'
        r = requests.post(post_url, data=payload,  files=imgload, headers=self.headers)
        return r.text


if __name__ == '__main__':
    wordpy = Wordpy(conf.FOLSOM_TOKEN)
    print wordpy.users()
    print conf.FOLSOM_ID
    print wordpy.create_post(title='myPost', categories='식사', content='2월1일 저녘', img='./img/doge.jpg')

