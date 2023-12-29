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
import multiprocessing
import os
import json
from browserstack_sdk.bstack1l1l1l111l_opy_ import *
from bstack_utils.config import Config
from bstack_utils.messages import bstack1ll11l1l11_opy_
class bstack111l1l111_opy_:
    def __init__(self, args, logger, bstack11lllll11l_opy_, bstack11llllllll_opy_):
        self.args = args
        self.logger = logger
        self.bstack11lllll11l_opy_ = bstack11lllll11l_opy_
        self.bstack11llllllll_opy_ = bstack11llllllll_opy_
        self._prepareconfig = None
        self.Config = None
        self.runner = None
        self.bstack11l1ll111_opy_ = []
        self.bstack1l111111ll_opy_ = None
        self.bstack11111l1l_opy_ = []
        self.bstack11lllllll1_opy_ = self.bstack1ll111lll1_opy_()
        self.bstack1l1lll11_opy_ = -1
    def bstack1111ll11l_opy_(self, bstack11lllll1l1_opy_):
        self.parse_args()
        self.bstack11llllll11_opy_()
        self.bstack11lllll1ll_opy_(bstack11lllll1l1_opy_)
    @staticmethod
    def version():
        import pytest
        return pytest.__version__
    def bstack1l11111l11_opy_(self, arg):
        if arg in self.args:
            i = self.args.index(arg)
            self.args.pop(i + 1)
            self.args.pop(i)
    def parse_args(self):
        self.bstack1l1lll11_opy_ = -1
        if bstack1l1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ෠") in self.bstack11lllll11l_opy_:
            self.bstack1l1lll11_opy_ = int(self.bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"ࠫࡵࡧࡲࡢ࡮࡯ࡩࡱࡹࡐࡦࡴࡓࡰࡦࡺࡦࡰࡴࡰࠫ෡")])
        try:
            bstack1l11111111_opy_ = [bstack1l1l1_opy_ (u"ࠬ࠳࠭ࡥࡴ࡬ࡺࡪࡸࠧ෢"), bstack1l1l1_opy_ (u"࠭࠭࠮ࡲ࡯ࡹ࡬࡯࡮ࡴࠩ෣"), bstack1l1l1_opy_ (u"ࠧ࠮ࡲࠪ෤")]
            if self.bstack1l1lll11_opy_ >= 0:
                bstack1l11111111_opy_.extend([bstack1l1l1_opy_ (u"ࠨ࠯࠰ࡲࡺࡳࡰࡳࡱࡦࡩࡸࡹࡥࡴࠩ෥"), bstack1l1l1_opy_ (u"ࠩ࠰ࡲࠬ෦")])
            for arg in bstack1l11111111_opy_:
                self.bstack1l11111l11_opy_(arg)
        except Exception as exc:
            self.logger.error(str(exc))
    def get_args(self):
        return self.args
    def bstack11llllll11_opy_(self):
        bstack1l111111ll_opy_ = [os.path.normpath(item) for item in self.args]
        self.bstack1l111111ll_opy_ = bstack1l111111ll_opy_
        return bstack1l111111ll_opy_
    def bstack11l11l11_opy_(self):
        try:
            from _pytest.config import _prepareconfig
            from _pytest.config import Config
            from _pytest import runner
            import importlib
            bstack11llllll1l_opy_ = importlib.find_loader(bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࡢࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ෧"))
            self._prepareconfig = _prepareconfig
            self.Config = Config
            self.runner = runner
        except Exception as e:
            self.logger.warn(e, bstack1ll11l1l11_opy_)
    def bstack11lllll1ll_opy_(self, bstack11lllll1l1_opy_):
        bstack1l11lll11_opy_ = Config.get_instance()
        if bstack11lllll1l1_opy_:
            self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠫ࠲࠳ࡳ࡬࡫ࡳࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨ෨"))
            self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"࡚ࠬࡲࡶࡧࠪ෩"))
        if bstack1l11lll11_opy_.bstack11llll1lll_opy_():
            self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"࠭࠭࠮ࡵ࡮࡭ࡵ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ෪"))
            self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠧࡕࡴࡸࡩࠬ෫"))
        self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠨ࠯ࡳࠫ෬"))
        self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡱ࡮ࡸ࡫࡮ࡴࠧ෭"))
        self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠪ࠱࠲ࡪࡲࡪࡸࡨࡶࠬ෮"))
        self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ෯"))
        if self.bstack1l1lll11_opy_ > 1:
            self.bstack1l111111ll_opy_.append(bstack1l1l1_opy_ (u"ࠬ࠳࡮ࠨ෰"))
            self.bstack1l111111ll_opy_.append(str(self.bstack1l1lll11_opy_))
    def bstack11lllll111_opy_(self):
        bstack11111l1l_opy_ = []
        for spec in self.bstack11l1ll111_opy_:
            bstack1ll1ll1l1l_opy_ = [spec]
            bstack1ll1ll1l1l_opy_ += self.bstack1l111111ll_opy_
            bstack11111l1l_opy_.append(bstack1ll1ll1l1l_opy_)
        self.bstack11111l1l_opy_ = bstack11111l1l_opy_
        return bstack11111l1l_opy_
    def bstack1ll111lll1_opy_(self):
        try:
            from pytest_bdd import reporting
            self.bstack11lllllll1_opy_ = True
            return True
        except Exception as e:
            self.bstack11lllllll1_opy_ = False
        return self.bstack11lllllll1_opy_
    def bstack1lll11ll_opy_(self, bstack1l111111l1_opy_, bstack1111ll11l_opy_):
        bstack1111ll11l_opy_[bstack1l1l1_opy_ (u"࠭ࡃࡐࡐࡉࡍࡌ࠭෱")] = self.bstack11lllll11l_opy_
        multiprocessing.set_start_method(bstack1l1l1_opy_ (u"ࠧࡴࡲࡤࡻࡳ࠭ෲ"))
        if bstack1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫෳ") in self.bstack11lllll11l_opy_:
            bstack111111lll_opy_ = []
            manager = multiprocessing.Manager()
            bstack11ll1lll_opy_ = manager.list()
            for index, platform in enumerate(self.bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ෴")]):
                bstack111111lll_opy_.append(multiprocessing.Process(name=str(index),
                                                           target=bstack1l111111l1_opy_,
                                                           args=(self.bstack1l111111ll_opy_, bstack1111ll11l_opy_, bstack11ll1lll_opy_)))
            i = 0
            bstack1l1111111l_opy_ = len(self.bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭෵")])
            for t in bstack111111lll_opy_:
                os.environ[bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡑࡇࡔࡇࡑࡕࡑࡤࡏࡎࡅࡇ࡛ࠫ෶")] = str(i)
                os.environ[bstack1l1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭෷")] = json.dumps(self.bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ෸")][i % bstack1l1111111l_opy_])
                i += 1
                t.start()
            for t in bstack111111lll_opy_:
                t.join()
            return list(bstack11ll1lll_opy_)