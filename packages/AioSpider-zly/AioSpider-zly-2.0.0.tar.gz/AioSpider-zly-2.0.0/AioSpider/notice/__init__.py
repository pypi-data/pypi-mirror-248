from .robot import WechatRobot, DingdingRobot, EmailRobot
from AioSpider.server import notice


class Message():

    def __init__(self):
        self.spider = None
        self._wechat = WechatRobot()
        self._dingding = DingdingRobot()
        self._email = EmailRobot()

    def set_spider_name(self, name):
        self.spider = name
    
    def add_wechat_robot(self, *args, **kwargs):
        self._wechat.add_robot(*args, **kwargs)
    
    def add_dingding_robot(self, *args, **kwargs):
        self._dingding.add_robot(*args, **kwargs)
    
    def add_email_robot(self, *args, **kwargs):
        self._email.add_robot(*args, **kwargs)
        
    def _get_platform(self, to):
        if to in self._wechat:
            return 'WECHAT'
        elif to in self._dingding:
            return 'DINGDING'
        elif to in self._email:
            return 'EMAIL'
        else:
            return 'DATA'

    def debug(self, msg, platform=True, to='system', action='DATA_COMMIT', *args, **kwargs):
        
        if platform:
            notice.create_notice(
                self.spider, message, level='DEBUG', platform=self._get_platform(to), action=action, env='DEV'
            )
        if to in self._wechat:
            self._wechat.info(msg, to)
            return
        if to in self._dingding:
            self._dingding.info(msg, to)
            return
        if to in self._email:
            self._email.info(msg, to)
            return

    def info(self, msg, platform=True, to='system', action='DATA_COMMIT', *args, **kwargs):

        if platform:
            notice.create_notice(
                self.spider, msg, level='INFO', platform=self._get_platform(to), action=action, env='DEV'
            )
        if to in self._wechat:
            self._wechat.info(msg, to)
            return
        if to in self._dingding:
            self._dingding.info(msg, to)
            return
        if to in self._email:
            self._email.info(msg, to)
            return

    def warning(self, msg, platform=True, to='system', action='DATA_COMMIT', *args, **kwargs):
        
        if platform:
            notice.create_notice(
                self.spider, msg, level='WARNING', platform=self._get_platform(to), action=action, env='DEV'
            )
        if to in self._wechat:
            self._wechat.info(msg, to)
            return
        if to in self._dingding:
            self._dingding.info(msg, to)
            return
        if to in self._email:
            self._email.info(msg, to)
            return

    def error(self, msg, platform=True, to='system', action='DATA_COMMIT', *args, **kwargs):
        
        if platform:
            notice.create_notice(
                self.spider, msg, level='ERROR', platform=self._get_platform(to), action=action, env='DEV'
            )
        if to in self._wechat:
            self._wechat.info(msg, to)
            return
        if to in self._dingding:
            self._dingding.info(msg, to)
            return

    def critical(self, msg, platform=True, to='system', action='DATA_COMMIT', *args, **kwargs):
        
        if platform:
            notice.create_notice(
                self.spider, msg, level='CRITICAL', platform=self._get_platform(to), action=action, env='DEV'
            )
        if to in self._wechat:
            self._wechat.info(msg, to)
            return
        if to in self._dingding:
            self._dingding.info(msg, to)
            return
        if to in self._email:
            self._email.info(msg, to)
            return