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
conf = {
    bstack1l1l1_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧປ"): False,
    bstack1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪຜ"): True,
    bstack1l1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡠࡵࡨࡷࡸ࡯࡯࡯ࡡࡶࡸࡦࡺࡵࡴࠩຝ"): False
}
class Config(object):
    instance = None
    def __init__(self):
        self._11ll1l1l1l_opy_ = conf
    @classmethod
    def get_instance(cls):
        if cls.instance:
            return cls.instance
        return Config()
    def get_property(self, property_name):
        return self._11ll1l1l1l_opy_.get(property_name, None)
    def bstack1ll111l11_opy_(self, property_name, bstack11ll1l1ll1_opy_):
        self._11ll1l1l1l_opy_[property_name] = bstack11ll1l1ll1_opy_
    def bstack1l111l11_opy_(self, val):
        self._11ll1l1l1l_opy_[bstack1l1l1_opy_ (u"ࠫࡸࡱࡩࡱࡡࡶࡩࡸࡹࡩࡰࡰࡢࡷࡹࡧࡴࡶࡵࠪພ")] = bool(val)
    def bstack11llll1lll_opy_(self):
        return self._11ll1l1l1l_opy_.get(bstack1l1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡢࡷࡪࡹࡳࡪࡱࡱࡣࡸࡺࡡࡵࡷࡶࠫຟ"), False)