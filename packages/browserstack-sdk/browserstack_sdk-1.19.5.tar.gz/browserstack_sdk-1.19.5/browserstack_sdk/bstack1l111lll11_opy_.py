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
import os
class RobotHandler():
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llllllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack1l11ll111l_opy_(bstack11llll1l11_opy_):
        bstack11llll1l1l_opy_ = []
        if bstack11llll1l11_opy_:
            tokens = str(os.path.basename(bstack11llll1l11_opy_)).split(bstack1l1l1_opy_ (u"ࠢࡠࠤ෹"))
            camelcase_name = bstack1l1l1_opy_ (u"ࠣࠢࠥ෺").join(t.title() for t in tokens)
            suite_name, bstack1l1l111ll_opy_ = os.path.splitext(camelcase_name)
            bstack11llll1l1l_opy_.append(suite_name)
        return bstack11llll1l1l_opy_
    @staticmethod
    def bstack11llll1ll1_opy_(typename):
        if bstack1l1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ෻") in typename:
            return bstack1l1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ෼")
        return bstack1l1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ෽")