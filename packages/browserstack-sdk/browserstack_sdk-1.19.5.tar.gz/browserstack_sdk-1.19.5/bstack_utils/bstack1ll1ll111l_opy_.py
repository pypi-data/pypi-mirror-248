# coding: UTF-8
import sys
bstack11_opy_ = sys.version_info [0] == 2
bstack1l11l11_opy_ = 2048
bstack1ll1l1_opy_ = 7
def bstack1l1l1_opy_ (bstack1ll11l_opy_):
    global bstack11ll1ll_opy_
    bstack1ll_opy_ = ord (bstack1ll11l_opy_ [-1])
    bstack1111ll1_opy_ = bstack1ll11l_opy_ [:-1]
    bstack1lllll_opy_ = bstack1ll_opy_ % len (bstack1111ll1_opy_)
    bstack1lll1ll_opy_ = bstack1111ll1_opy_ [:bstack1lllll_opy_] + bstack1111ll1_opy_ [bstack1lllll_opy_:]
    if bstack11_opy_:
        bstack1111ll_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11l11_opy_ - (bstack1ll1l1l_opy_ + bstack1ll_opy_) % bstack1ll1l1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1lll1ll_opy_)])
    else:
        bstack1111ll_opy_ = str () .join ([chr (ord (char) - bstack1l11l11_opy_ - (bstack1ll1l1l_opy_ + bstack1ll_opy_) % bstack1ll1l1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1lll1ll_opy_)])
    return eval (bstack1111ll_opy_)
class bstack11ll11111_opy_:
    def __init__(self, handler):
        self._11111lllll_opy_ = None
        self.handler = handler
        self._11111lll1l_opy_ = self.bstack11111lll11_opy_()
        self.patch()
    def patch(self):
        self._11111lllll_opy_ = self._11111lll1l_opy_.execute
        self._11111lll1l_opy_.execute = self.bstack11111llll1_opy_()
    def bstack11111llll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1l1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࠨᏧ"), driver_command)
            response = self._11111lllll_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1l1l1_opy_ (u"ࠢࡢࡨࡷࡩࡷࠨᏨ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._11111lll1l_opy_.execute = self._11111lllll_opy_
    @staticmethod
    def bstack11111lll11_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver