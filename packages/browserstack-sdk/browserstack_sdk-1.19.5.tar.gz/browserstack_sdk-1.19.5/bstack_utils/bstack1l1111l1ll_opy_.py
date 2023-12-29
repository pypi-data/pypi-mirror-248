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
from uuid import uuid4
from bstack_utils.helper import bstack1l11lllll_opy_, bstack11ll111lll_opy_
from bstack_utils.bstack1111l1ll1_opy_ import bstack1111ll1lll_opy_
class bstack1l1111ll11_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack1l111l1lll_opy_=None, framework=None, tags=[], scope=[], bstack11111l111l_opy_=None, bstack1111111ll1_opy_=True, bstack11111l1111_opy_=None, bstack1l1l11ll1l_opy_=None, result=None, duration=None, bstack1l11111l1l_opy_=None, meta={}):
        self.bstack1l11111l1l_opy_ = bstack1l11111l1l_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1111111ll1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack1l111l1lll_opy_ = bstack1l111l1lll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack11111l111l_opy_ = bstack11111l111l_opy_
        self.bstack11111l1111_opy_ = bstack11111l1111_opy_
        self.bstack1l1l11ll1l_opy_ = bstack1l1l11ll1l_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack1l111l1ll1_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11111l11ll_opy_(self):
        bstack1111111lll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᐝ"): bstack1111111lll_opy_,
            bstack1l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᐞ"): bstack1111111lll_opy_,
            bstack1l1l1_opy_ (u"࠭ࡶࡤࡡࡩ࡭ࡱ࡫ࡰࡢࡶ࡫ࠫᐟ"): bstack1111111lll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1l1l1_opy_ (u"ࠢࡖࡰࡨࡼࡵ࡫ࡣࡵࡧࡧࠤࡦࡸࡧࡶ࡯ࡨࡲࡹࡀࠠࠣᐠ") + key)
            setattr(self, key, val)
    def bstack111111l111_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐡ"): self.name,
            bstack1l1l1_opy_ (u"ࠩࡥࡳࡩࡿࠧᐢ"): {
                bstack1l1l1_opy_ (u"ࠪࡰࡦࡴࡧࠨᐣ"): bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫᐤ"),
                bstack1l1l1_opy_ (u"ࠬࡩ࡯ࡥࡧࠪᐥ"): self.code
            },
            bstack1l1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᐦ"): self.scope,
            bstack1l1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬᐧ"): self.tags,
            bstack1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᐨ"): self.framework,
            bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐩ"): self.bstack1l111l1lll_opy_
        }
    def bstack111111llll_opy_(self):
        return {
         bstack1l1l1_opy_ (u"ࠪࡱࡪࡺࡡࠨᐪ"): self.meta
        }
    def bstack111111l1l1_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡖࡪࡸࡵ࡯ࡒࡤࡶࡦࡳࠧᐫ"): {
                bstack1l1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡣࡳࡧ࡭ࡦࠩᐬ"): self.bstack11111l111l_opy_
            }
        }
    def bstack11111l1ll1_opy_(self, bstack11111l11l1_opy_, details):
        step = next(filter(lambda st: st[bstack1l1l1_opy_ (u"࠭ࡩࡥࠩᐭ")] == bstack11111l11l1_opy_, self.meta[bstack1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐮ")]), None)
        step.update(details)
    def bstack11111l1l11_opy_(self, bstack11111l11l1_opy_):
        step = next(filter(lambda st: st[bstack1l1l1_opy_ (u"ࠨ࡫ࡧࠫᐯ")] == bstack11111l11l1_opy_, self.meta[bstack1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᐰ")]), None)
        step.update({
            bstack1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᐱ"): bstack1l11lllll_opy_()
        })
    def bstack1l11l1llll_opy_(self, bstack11111l11l1_opy_, result, duration=None):
        bstack11111l1111_opy_ = bstack1l11lllll_opy_()
        if bstack11111l11l1_opy_ is not None and self.meta.get(bstack1l1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᐲ")):
            step = next(filter(lambda st: st[bstack1l1l1_opy_ (u"ࠬ࡯ࡤࠨᐳ")] == bstack11111l11l1_opy_, self.meta[bstack1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐴ")]), None)
            step.update({
                bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᐵ"): bstack11111l1111_opy_,
                bstack1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᐶ"): duration if duration else bstack11ll111lll_opy_(step[bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᐷ")], bstack11111l1111_opy_),
                bstack1l1l1_opy_ (u"ࠪࡶࡪࡹࡵ࡭ࡶࠪᐸ"): result.result,
                bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᐹ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack11111l1lll_opy_):
        if self.meta.get(bstack1l1l1_opy_ (u"ࠬࡹࡴࡦࡲࡶࠫᐺ")):
            self.meta[bstack1l1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᐻ")].append(bstack11111l1lll_opy_)
        else:
            self.meta[bstack1l1l1_opy_ (u"ࠧࡴࡶࡨࡴࡸ࠭ᐼ")] = [ bstack11111l1lll_opy_ ]
    def bstack111111l1ll_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᐽ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack111111l111_opy_(),
            **self.bstack11111l11ll_opy_(),
            **self.bstack111111llll_opy_()
        }
    def bstack111111ll11_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᐾ"): self.bstack11111l1111_opy_,
            bstack1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᐿ"): self.duration,
            bstack1l1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫᑀ"): self.result.result
        }
        if data[bstack1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᑁ")] == bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᑂ"):
            data[bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᑃ")] = self.result.bstack11llll1ll1_opy_()
            data[bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᑄ")] = [{bstack1l1l1_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬᑅ"): self.result.bstack11ll11111l_opy_()}]
        return data
    def bstack1111111l1l_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᑆ"): self.bstack1l111l1ll1_opy_(),
            **self.bstack111111l111_opy_(),
            **self.bstack11111l11ll_opy_(),
            **self.bstack111111ll11_opy_(),
            **self.bstack111111llll_opy_()
        }
    def bstack1l11l11lll_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1l1l1_opy_ (u"ࠫࡘࡺࡡࡳࡶࡨࡨࠬᑇ") in event:
            return self.bstack111111l1ll_opy_()
        elif bstack1l1l1_opy_ (u"ࠬࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᑈ") in event:
            return self.bstack1111111l1l_opy_()
    def bstack1l11l11l1l_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack11111l1111_opy_ = time if time else bstack1l11lllll_opy_()
        self.duration = duration if duration else bstack11ll111lll_opy_(self.bstack1l111l1lll_opy_, self.bstack11111l1111_opy_)
        if result:
            self.result = result
class bstack1l11lllll1_opy_(bstack1l1111ll11_opy_):
    def __init__(self, hooks=[], bstack1l111ll111_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack1l111ll111_opy_ = bstack1l111ll111_opy_
        super().__init__(*args, **kwargs, bstack1l1l11ll1l_opy_=bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࠫᑉ"))
    @classmethod
    def bstack111111l11l_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1l1l1_opy_ (u"ࠧࡪࡦࠪᑊ"): id(step),
                bstack1l1l1_opy_ (u"ࠨࡶࡨࡼࡹ࠭ᑋ"): step.name,
                bstack1l1l1_opy_ (u"ࠩ࡮ࡩࡾࡽ࡯ࡳࡦࠪᑌ"): step.keyword,
            })
        return bstack1l11lllll1_opy_(
            **kwargs,
            meta={
                bstack1l1l1_opy_ (u"ࠪࡪࡪࡧࡴࡶࡴࡨࠫᑍ"): {
                    bstack1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᑎ"): feature.name,
                    bstack1l1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪᑏ"): feature.filename,
                    bstack1l1l1_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᑐ"): feature.description
                },
                bstack1l1l1_opy_ (u"ࠧࡴࡥࡨࡲࡦࡸࡩࡰࠩᑑ"): {
                    bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᑒ"): scenario.name
                },
                bstack1l1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᑓ"): steps,
                bstack1l1l1_opy_ (u"ࠪࡩࡽࡧ࡭ࡱ࡮ࡨࡷࠬᑔ"): bstack1111ll1lll_opy_(test)
            }
        )
    def bstack11111l1l1l_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᑕ"): self.hooks
        }
    def bstack111111lll1_opy_(self):
        if self.bstack1l111ll111_opy_:
            return {
                bstack1l1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠫᑖ"): self.bstack1l111ll111_opy_
            }
        return {}
    def bstack1111111l1l_opy_(self):
        return {
            **super().bstack1111111l1l_opy_(),
            **self.bstack11111l1l1l_opy_()
        }
    def bstack111111l1ll_opy_(self):
        return {
            **super().bstack111111l1ll_opy_(),
            **self.bstack111111lll1_opy_()
        }
    def bstack1l11l11l1l_opy_(self):
        return bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨᑗ")
class bstack1l1111ll1l_opy_(bstack1l1111ll11_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        super().__init__(*args, **kwargs, bstack1l1l11ll1l_opy_=bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᑘ"))
    def bstack1l11l1l1ll_opy_(self):
        return self.hook_type
    def bstack111111ll1l_opy_(self):
        return {
            bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡴࡺࡲࡨࠫᑙ"): self.hook_type
        }
    def bstack1111111l1l_opy_(self):
        return {
            **super().bstack1111111l1l_opy_(),
            **self.bstack111111ll1l_opy_()
        }
    def bstack111111l1ll_opy_(self):
        return {
            **super().bstack111111l1ll_opy_(),
            **self.bstack111111ll1l_opy_()
        }
    def bstack1l11l11l1l_opy_(self):
        return bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࠫᑚ")