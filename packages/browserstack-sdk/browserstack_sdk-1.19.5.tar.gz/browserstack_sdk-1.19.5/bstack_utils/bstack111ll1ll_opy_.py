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
import json
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11l11lll1l_opy_, bstack11l111ll1_opy_, bstack1lllll11l_opy_, bstack1ll1111ll1_opy_, \
    bstack11l1l11111_opy_
def bstack111lll1ll_opy_(bstack11111ll111_opy_):
    for driver in bstack11111ll111_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack11ll11ll_opy_(driver, status, reason=bstack1l1l1_opy_ (u"ࠨࠩᏩ")):
    bstack1l11lll11_opy_ = Config.get_instance()
    if bstack1l11lll11_opy_.bstack11llll1lll_opy_():
        return
    bstack1llll1l11_opy_ = bstack1lll1111ll_opy_(bstack1l1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬᏪ"), bstack1l1l1_opy_ (u"ࠪࠫᏫ"), status, reason, bstack1l1l1_opy_ (u"ࠫࠬᏬ"), bstack1l1l1_opy_ (u"ࠬ࠭Ꮽ"))
    driver.execute_script(bstack1llll1l11_opy_)
def bstack11l1l11l_opy_(page, status, reason=bstack1l1l1_opy_ (u"࠭ࠧᏮ")):
    try:
        if page is None:
            return
        bstack1l11lll11_opy_ = Config.get_instance()
        if bstack1l11lll11_opy_.bstack11llll1lll_opy_():
            return
        bstack1llll1l11_opy_ = bstack1lll1111ll_opy_(bstack1l1l1_opy_ (u"ࠧࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡴࡶࡵࠪᏯ"), bstack1l1l1_opy_ (u"ࠨࠩᏰ"), status, reason, bstack1l1l1_opy_ (u"ࠩࠪᏱ"), bstack1l1l1_opy_ (u"ࠪࠫᏲ"))
        page.evaluate(bstack1l1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᏳ"), bstack1llll1l11_opy_)
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡳࡵࡣࡷࡹࡸࠦࡦࡰࡴࠣࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠠࡼࡿࠥᏴ"), e)
def bstack1lll1111ll_opy_(type, name, status, reason, bstack1lll1l11ll_opy_, bstack1lll1l111_opy_):
    bstack1llllll11_opy_ = {
        bstack1l1l1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭Ᏽ"): type,
        bstack1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᏶"): {}
    }
    if type == bstack1l1l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪ᏷"):
        bstack1llllll11_opy_[bstack1l1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᏸ")][bstack1l1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩᏹ")] = bstack1lll1l11ll_opy_
        bstack1llllll11_opy_[bstack1l1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᏺ")][bstack1l1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪᏻ")] = json.dumps(str(bstack1lll1l111_opy_))
    if type == bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧᏼ"):
        bstack1llllll11_opy_[bstack1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᏽ")][bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭᏾")] = name
    if type == bstack1l1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ᏿"):
        bstack1llllll11_opy_[bstack1l1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᐀")][bstack1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᐁ")] = status
        if status == bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᐂ") and str(reason) != bstack1l1l1_opy_ (u"ࠨࠢᐃ"):
            bstack1llllll11_opy_[bstack1l1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᐄ")][bstack1l1l1_opy_ (u"ࠨࡴࡨࡥࡸࡵ࡮ࠨᐅ")] = json.dumps(str(reason))
    bstack1l1l1111_opy_ = bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧᐆ").format(json.dumps(bstack1llllll11_opy_))
    return bstack1l1l1111_opy_
def bstack1lll1l1lll_opy_(url, config, logger, bstack1ll1ll1l11_opy_=False):
    hostname = bstack11l111ll1_opy_(url)
    is_private = bstack1ll1111ll1_opy_(hostname)
    try:
        if is_private or bstack1ll1ll1l11_opy_:
            file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᐇ"), bstack1l1l1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᐈ"), logger)
            if os.environ.get(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡑࡕࡃࡂࡎࡢࡒࡔ࡚࡟ࡔࡇࡗࡣࡊࡘࡒࡐࡔࠪᐉ")) and eval(
                    os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᐊ"))):
                return
            if (bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫᐋ") in config and not config[bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᐌ")]):
                os.environ[bstack1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᐍ")] = str(True)
                bstack11111ll11l_opy_ = {bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬᐎ"): hostname}
                bstack11l1l11111_opy_(bstack1l1l1_opy_ (u"ࠫ࠳ࡨࡳࡵࡣࡦ࡯࠲ࡩ࡯࡯ࡨ࡬࡫࠳ࡰࡳࡰࡰࠪᐏ"), bstack1l1l1_opy_ (u"ࠬࡴࡵࡥࡩࡨࡣࡱࡵࡣࡢ࡮ࠪᐐ"), bstack11111ll11l_opy_, logger)
    except Exception as e:
        pass
def bstack1ll111l111_opy_(caps, bstack11111ll1ll_opy_):
    if bstack1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᐑ") in caps:
        caps[bstack1l1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᐒ")][bstack1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࠧᐓ")] = True
        if bstack11111ll1ll_opy_:
            caps[bstack1l1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᐔ")][bstack1l1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᐕ")] = bstack11111ll1ll_opy_
    else:
        caps[bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡰࡴࡩࡡ࡭ࠩᐖ")] = True
        if bstack11111ll1ll_opy_:
            caps[bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ᐗ")] = bstack11111ll1ll_opy_
def bstack1111ll11ll_opy_(bstack1l11llllll_opy_):
    bstack11111ll1l1_opy_ = bstack1lllll11l_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡗࡹࡧࡴࡶࡵࠪᐘ"), bstack1l1l1_opy_ (u"ࠧࠨᐙ"))
    if bstack11111ll1l1_opy_ == bstack1l1l1_opy_ (u"ࠨࠩᐚ") or bstack11111ll1l1_opy_ == bstack1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᐛ"):
        threading.current_thread().testStatus = bstack1l11llllll_opy_
    else:
        if bstack1l11llllll_opy_ == bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᐜ"):
            threading.current_thread().testStatus = bstack1l11llllll_opy_