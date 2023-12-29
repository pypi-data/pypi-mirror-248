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
from urllib.parse import urlparse
from bstack_utils.messages import bstack11l111l1l1_opy_
def bstack1111llllll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1111llll11_opy_(bstack1111lllll1_opy_, bstack1111lll1l1_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1111lllll1_opy_):
        with open(bstack1111lllll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1111llllll_opy_(bstack1111lllll1_opy_):
        pac = get_pac(url=bstack1111lllll1_opy_)
    else:
        raise Exception(bstack1l1l1_opy_ (u"ࠩࡓࡥࡨࠦࡦࡪ࡮ࡨࠤࡩࡵࡥࡴࠢࡱࡳࡹࠦࡥࡹ࡫ࡶࡸ࠿ࠦࡻࡾࠩᎏ").format(bstack1111lllll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1l1l1_opy_ (u"ࠥ࠼࠳࠾࠮࠹࠰࠻ࠦ᎐"), 80))
        bstack1111llll1l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1111llll1l_opy_ = bstack1l1l1_opy_ (u"ࠫ࠵࠴࠰࠯࠲࠱࠴ࠬ᎑")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1111lll1l1_opy_, bstack1111llll1l_opy_)
    return proxy_url
def bstack1lll1l111l_opy_(config):
    return bstack1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨ᎒") in config or bstack1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪ᎓") in config
def bstack1l111lll1_opy_(config):
    if not bstack1lll1l111l_opy_(config):
        return
    if config.get(bstack1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪ᎔")):
        return config.get(bstack1l1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫ᎕"))
    if config.get(bstack1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭᎖")):
        return config.get(bstack1l1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࡒࡵࡳࡽࡿࠧ᎗"))
def bstack1ll11l1l1l_opy_(config, bstack1111lll1l1_opy_):
    proxy = bstack1l111lll1_opy_(config)
    proxies = {}
    if config.get(bstack1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧ᎘")) or config.get(bstack1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩ᎙")):
        if proxy.endswith(bstack1l1l1_opy_ (u"࠭࠮ࡱࡣࡦࠫ᎚")):
            proxies = bstack1111l11ll_opy_(proxy, bstack1111lll1l1_opy_)
        else:
            proxies = {
                bstack1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸ࠭᎛"): proxy
            }
    return proxies
def bstack1111l11ll_opy_(bstack1111lllll1_opy_, bstack1111lll1l1_opy_):
    proxies = {}
    global bstack111l111111_opy_
    if bstack1l1l1_opy_ (u"ࠨࡒࡄࡇࡤࡖࡒࡐ࡚࡜ࠫ᎜") in globals():
        return bstack111l111111_opy_
    try:
        proxy = bstack1111llll11_opy_(bstack1111lllll1_opy_, bstack1111lll1l1_opy_)
        if bstack1l1l1_opy_ (u"ࠤࡇࡍࡗࡋࡃࡕࠤ᎝") in proxy:
            proxies = {}
        elif bstack1l1l1_opy_ (u"ࠥࡌ࡙࡚ࡐࠣ᎞") in proxy or bstack1l1l1_opy_ (u"ࠦࡍ࡚ࡔࡑࡕࠥ᎟") in proxy or bstack1l1l1_opy_ (u"࡙ࠧࡏࡄࡍࡖࠦᎠ") in proxy:
            bstack1111lll1ll_opy_ = proxy.split(bstack1l1l1_opy_ (u"ࠨࠠࠣᎡ"))
            if bstack1l1l1_opy_ (u"ࠢ࠻࠱࠲ࠦᎢ") in bstack1l1l1_opy_ (u"ࠣࠤᎣ").join(bstack1111lll1ll_opy_[1:]):
                proxies = {
                    bstack1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᎤ"): bstack1l1l1_opy_ (u"ࠥࠦᎥ").join(bstack1111lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎦ"): str(bstack1111lll1ll_opy_[0]).lower() + bstack1l1l1_opy_ (u"ࠧࡀ࠯࠰ࠤᎧ") + bstack1l1l1_opy_ (u"ࠨࠢᎨ").join(bstack1111lll1ll_opy_[1:])
                }
        elif bstack1l1l1_opy_ (u"ࠢࡑࡔࡒ࡜࡞ࠨᎩ") in proxy:
            bstack1111lll1ll_opy_ = proxy.split(bstack1l1l1_opy_ (u"ࠣࠢࠥᎪ"))
            if bstack1l1l1_opy_ (u"ࠤ࠽࠳࠴ࠨᎫ") in bstack1l1l1_opy_ (u"ࠥࠦᎬ").join(bstack1111lll1ll_opy_[1:]):
                proxies = {
                    bstack1l1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࠪᎭ"): bstack1l1l1_opy_ (u"ࠧࠨᎮ").join(bstack1111lll1ll_opy_[1:])
                }
            else:
                proxies = {
                    bstack1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᎯ"): bstack1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࠣᎰ") + bstack1l1l1_opy_ (u"ࠣࠤᎱ").join(bstack1111lll1ll_opy_[1:])
                }
        else:
            proxies = {
                bstack1l1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࠨᎲ"): proxy
            }
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠥࡷࡴࡳࡥࠡࡧࡵࡶࡴࡸࠢᎳ"), bstack11l111l1l1_opy_.format(bstack1111lllll1_opy_, str(e)))
    bstack111l111111_opy_ = proxies
    return proxies