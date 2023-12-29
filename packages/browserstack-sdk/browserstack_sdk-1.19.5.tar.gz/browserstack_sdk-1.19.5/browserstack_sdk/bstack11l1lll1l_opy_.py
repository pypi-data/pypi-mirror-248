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
import json
import logging
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11l1111_opy_ = {}
        bstack1l1l111ll1_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭೭"), bstack1l1l1_opy_ (u"࠭ࠧ೮"))
        if not bstack1l1l111ll1_opy_:
            return bstack1l11l1111_opy_
        try:
            bstack1l1l111lll_opy_ = json.loads(bstack1l1l111ll1_opy_)
            if bstack1l1l1_opy_ (u"ࠢࡰࡵࠥ೯") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠣࡱࡶࠦ೰")] = bstack1l1l111lll_opy_[bstack1l1l1_opy_ (u"ࠤࡲࡷࠧೱ")]
            if bstack1l1l1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢೲ") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢೳ") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೴")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥ೵"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥ೶")))
            if bstack1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤ೷") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢ೸") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣ೹")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧ೺"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥ೻")))
            if bstack1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣ೼") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣ೽") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤ೾")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦ೿"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦഀ")))
            if bstack1l1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦഁ") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤം") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥഃ")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢഄ"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧഅ")))
            if bstack1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦആ") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤഇ") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥഈ")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢഉ"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧഊ")))
            if bstack1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥഋ") in bstack1l1l111lll_opy_ or bstack1l1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥഌ") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ഍")] = bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨഎ"), bstack1l1l111lll_opy_.get(bstack1l1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨഏ")))
            if bstack1l1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢഐ") in bstack1l1l111lll_opy_:
                bstack1l11l1111_opy_[bstack1l1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣ഑")] = bstack1l1l111lll_opy_[bstack1l1l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤഒ")]
        except Exception as error:
            logger.error(bstack1l1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢഓ") +  str(error))
        return bstack1l11l1111_opy_