import random
from AioSpider import tools


class VisitorPool:

    def __init__(self):
        self.cookies = {}
    
    def get_cookie(self):
        cid = random.choices([i for i in self.cookies.keys()])
        return self.cookies[cid]
    
    def add_cookie(self, cookie):
        
        cid = tools.make_md5(cookie)
        
        if cid in self.cookies:
            return 
        
        self.cookies[cid] = cookie
