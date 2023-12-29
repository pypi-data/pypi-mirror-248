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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
from urllib.parse import urlparse
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import bstack11ll11lll1_opy_, bstack1ll111l1l1_opy_, bstack11lllll1l_opy_, bstack1l1ll1lll_opy_
from bstack_utils.messages import bstack111111l1_opy_, bstack1l111111l_opy_
from bstack_utils.proxy import bstack1ll11l1l1l_opy_, bstack1l111lll1_opy_
from browserstack_sdk.bstack1l1lll1111_opy_ import *
from browserstack_sdk.bstack1l111lll11_opy_ import *
bstack1l11lll11_opy_ = Config.get_instance()
def bstack11lll111ll_opy_(config):
    return config[bstack1l1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪᄦ")]
def bstack11lll1llll_opy_(config):
    return config[bstack1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬᄧ")]
def bstack1111l111l_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11l1llllll_opy_(obj):
    values = []
    bstack11l1l1ll11_opy_ = re.compile(bstack1l1l1_opy_ (u"ࡵࠦࡣࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࡟ࡨ࠰ࠪࠢᄨ"), re.I)
    for key in obj.keys():
        if bstack11l1l1ll11_opy_.match(key):
            values.append(obj[key])
    return values
def bstack11l1ll11ll_opy_(config):
    tags = []
    tags.extend(bstack11l1llllll_opy_(os.environ))
    tags.extend(bstack11l1llllll_opy_(config))
    return tags
def bstack11l1lll111_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack11l1lll11l_opy_(bstack11l1l1l1ll_opy_):
    if not bstack11l1l1l1ll_opy_:
        return bstack1l1l1_opy_ (u"ࠫࠬᄩ")
    return bstack1l1l1_opy_ (u"ࠧࢁࡽࠡࠪࡾࢁ࠮ࠨᄪ").format(bstack11l1l1l1ll_opy_.name, bstack11l1l1l1ll_opy_.email)
def bstack11lll1111l_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack11ll11l111_opy_ = repo.common_dir
        info = {
            bstack1l1l1_opy_ (u"ࠨࡳࡩࡣࠥᄫ"): repo.head.commit.hexsha,
            bstack1l1l1_opy_ (u"ࠢࡴࡪࡲࡶࡹࡥࡳࡩࡣࠥᄬ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1l1l1_opy_ (u"ࠣࡤࡵࡥࡳࡩࡨࠣᄭ"): repo.active_branch.name,
            bstack1l1l1_opy_ (u"ࠤࡷࡥ࡬ࠨᄮ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࠨᄯ"): bstack11l1lll11l_opy_(repo.head.commit.committer),
            bstack1l1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡸࡪࡸ࡟ࡥࡣࡷࡩࠧᄰ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1l1l1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࠧᄱ"): bstack11l1lll11l_opy_(repo.head.commit.author),
            bstack1l1l1_opy_ (u"ࠨࡡࡶࡶ࡫ࡳࡷࡥࡤࡢࡶࡨࠦᄲ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1l1l1_opy_ (u"ࠢࡤࡱࡰࡱ࡮ࡺ࡟࡮ࡧࡶࡷࡦ࡭ࡥࠣᄳ"): repo.head.commit.message,
            bstack1l1l1_opy_ (u"ࠣࡴࡲࡳࡹࠨᄴ"): repo.git.rev_parse(bstack1l1l1_opy_ (u"ࠤ࠰࠱ࡸ࡮࡯ࡸ࠯ࡷࡳࡵࡲࡥࡷࡧ࡯ࠦᄵ")),
            bstack1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡰࡰࡢ࡫࡮ࡺ࡟ࡥ࡫ࡵࠦᄶ"): bstack11ll11l111_opy_,
            bstack1l1l1_opy_ (u"ࠦࡼࡵࡲ࡬ࡶࡵࡩࡪࡥࡧࡪࡶࡢࡨ࡮ࡸࠢᄷ"): subprocess.check_output([bstack1l1l1_opy_ (u"ࠧ࡭ࡩࡵࠤᄸ"), bstack1l1l1_opy_ (u"ࠨࡲࡦࡸ࠰ࡴࡦࡸࡳࡦࠤᄹ"), bstack1l1l1_opy_ (u"ࠢ࠮࠯ࡪ࡭ࡹ࠳ࡣࡰ࡯ࡰࡳࡳ࠳ࡤࡪࡴࠥᄺ")]).strip().decode(
                bstack1l1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧᄻ")),
            bstack1l1l1_opy_ (u"ࠤ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦᄼ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1l1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡶࡣࡸ࡯࡮ࡤࡧࡢࡰࡦࡹࡴࡠࡶࡤ࡫ࠧᄽ"): repo.git.rev_list(
                bstack1l1l1_opy_ (u"ࠦࢀࢃ࠮࠯ࡽࢀࠦᄾ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack11ll1111l1_opy_ = []
        for remote in remotes:
            bstack11l1l111ll_opy_ = {
                bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᄿ"): remote.name,
                bstack1l1l1_opy_ (u"ࠨࡵࡳ࡮ࠥᅀ"): remote.url,
            }
            bstack11ll1111l1_opy_.append(bstack11l1l111ll_opy_)
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅁ"): bstack1l1l1_opy_ (u"ࠣࡩ࡬ࡸࠧᅂ"),
            **info,
            bstack1l1l1_opy_ (u"ࠤࡵࡩࡲࡵࡴࡦࡵࠥᅃ"): bstack11ll1111l1_opy_
        }
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡳࡵࡻ࡬ࡢࡶ࡬ࡲ࡬ࠦࡇࡪࡶࠣࡱࡪࡺࡡࡥࡣࡷࡥࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳ࠼ࠣࡿࢂࠨᅄ").format(err))
        return {}
def bstack11lll11ll_opy_():
    env = os.environ
    if (bstack1l1l1_opy_ (u"ࠦࡏࡋࡎࡌࡋࡑࡗࡤ࡛ࡒࡍࠤᅅ") in env and len(env[bstack1l1l1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥᅆ")]) > 0) or (
            bstack1l1l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡉࡑࡐࡉࠧᅇ") in env and len(env[bstack1l1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨᅈ")]) > 0):
        return {
            bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᅉ"): bstack1l1l1_opy_ (u"ࠤࡍࡩࡳࡱࡩ࡯ࡵࠥᅊ"),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨᅋ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᅌ")),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢᅍ"): env.get(bstack1l1l1_opy_ (u"ࠨࡊࡐࡄࡢࡒࡆࡓࡅࠣᅎ")),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᅏ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᅐ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠤࡆࡍࠧᅑ")) == bstack1l1l1_opy_ (u"ࠥࡸࡷࡻࡥࠣᅒ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡇࡎࠨᅓ"))):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᅔ"): bstack1l1l1_opy_ (u"ࠨࡃࡪࡴࡦࡰࡪࡉࡉࠣᅕ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᅖ"): env.get(bstack1l1l1_opy_ (u"ࠣࡅࡌࡖࡈࡒࡅࡠࡄࡘࡍࡑࡊ࡟ࡖࡔࡏࠦᅗ")),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᅘ"): env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࡘࡃࡍࡇࡢࡎࡔࡈࠢᅙ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅚ"): env.get(bstack1l1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࠣᅛ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࠤᅜ")) == bstack1l1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧᅝ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࠣᅞ"))):
        return {
            bstack1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᅟ"): bstack1l1l1_opy_ (u"ࠥࡘࡷࡧࡶࡪࡵࠣࡇࡎࠨᅠ"),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᅡ"): env.get(bstack1l1l1_opy_ (u"࡚ࠧࡒࡂࡘࡌࡗࡤࡈࡕࡊࡎࡇࡣ࡜ࡋࡂࡠࡗࡕࡐࠧᅢ")),
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᅣ"): env.get(bstack1l1l1_opy_ (u"ࠢࡕࡔࡄ࡚ࡎ࡙࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᅤ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᅥ"): env.get(bstack1l1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅦ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࠨᅧ")) == bstack1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᅨ") and env.get(bstack1l1l1_opy_ (u"ࠧࡉࡉࡠࡐࡄࡑࡊࠨᅩ")) == bstack1l1l1_opy_ (u"ࠨࡣࡰࡦࡨࡷ࡭࡯ࡰࠣᅪ"):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅫ"): bstack1l1l1_opy_ (u"ࠣࡅࡲࡨࡪࡹࡨࡪࡲࠥᅬ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅭ"): None,
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᅮ"): None,
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᅯ"): None
        }
    if env.get(bstack1l1l1_opy_ (u"ࠧࡈࡉࡕࡄࡘࡇࡐࡋࡔࡠࡄࡕࡅࡓࡉࡈࠣᅰ")) and env.get(bstack1l1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡆࡓࡒࡓࡉࡕࠤᅱ")):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᅲ"): bstack1l1l1_opy_ (u"ࠣࡄ࡬ࡸࡧࡻࡣ࡬ࡧࡷࠦᅳ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᅴ"): env.get(bstack1l1l1_opy_ (u"ࠥࡆࡎ࡚ࡂࡖࡅࡎࡉ࡙ࡥࡇࡊࡖࡢࡌ࡙࡚ࡐࡠࡑࡕࡍࡌࡏࡎࠣᅵ")),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᅶ"): None,
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᅷ"): env.get(bstack1l1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᅸ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠢࡄࡋࠥᅹ")) == bstack1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᅺ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࠣᅻ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᅼ"): bstack1l1l1_opy_ (u"ࠦࡉࡸ࡯࡯ࡧࠥᅽ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᅾ"): env.get(bstack1l1l1_opy_ (u"ࠨࡄࡓࡑࡑࡉࡤࡈࡕࡊࡎࡇࡣࡑࡏࡎࡌࠤᅿ")),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆀ"): None,
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᆁ"): env.get(bstack1l1l1_opy_ (u"ࠤࡇࡖࡔࡔࡅࡠࡄࡘࡍࡑࡊ࡟ࡏࡗࡐࡆࡊࡘࠢᆂ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࠨᆃ")) == bstack1l1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤᆄ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࠣᆅ"))):
        return {
            bstack1l1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᆆ"): bstack1l1l1_opy_ (u"ࠢࡔࡧࡰࡥࡵ࡮࡯ࡳࡧࠥᆇ"),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᆈ"): env.get(bstack1l1l1_opy_ (u"ࠤࡖࡉࡒࡇࡐࡉࡑࡕࡉࡤࡕࡒࡈࡃࡑࡍ࡟ࡇࡔࡊࡑࡑࡣ࡚ࡘࡌࠣᆉ")),
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᆊ"): env.get(bstack1l1l1_opy_ (u"ࠦࡘࡋࡍࡂࡒࡋࡓࡗࡋ࡟ࡋࡑࡅࡣࡓࡇࡍࡆࠤᆋ")),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᆌ"): env.get(bstack1l1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࡡࡍࡓࡇࡥࡉࡅࠤᆍ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠢࡄࡋࠥᆎ")) == bstack1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨᆏ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡊࡍ࡙ࡒࡁࡃࡡࡆࡍࠧᆐ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᆑ"): bstack1l1l1_opy_ (u"ࠦࡌ࡯ࡴࡍࡣࡥࠦᆒ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆓ"): env.get(bstack1l1l1_opy_ (u"ࠨࡃࡊࡡࡍࡓࡇࡥࡕࡓࡎࠥᆔ")),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᆕ"): env.get(bstack1l1l1_opy_ (u"ࠣࡅࡌࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᆖ")),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᆗ"): env.get(bstack1l1l1_opy_ (u"ࠥࡇࡎࡥࡊࡐࡄࡢࡍࡉࠨᆘ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠦࡈࡏࠢᆙ")) == bstack1l1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥᆚ") and bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࠤᆛ"))):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆜ"): bstack1l1l1_opy_ (u"ࠣࡄࡸ࡭ࡱࡪ࡫ࡪࡶࡨࠦᆝ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆞ"): env.get(bstack1l1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡍࡌࡘࡊࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᆟ")),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᆠ"): env.get(bstack1l1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡏࡎ࡚ࡅࡠࡎࡄࡆࡊࡒࠢᆡ")) or env.get(bstack1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡓࡍࡕࡋࡌࡊࡐࡈࡣࡓࡇࡍࡆࠤᆢ")),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨᆣ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊࡋࡊࡖࡈࡣࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥᆤ"))
        }
    if bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡗࡊࡤࡈࡕࡊࡎࡇࠦᆥ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᆦ"): bstack1l1l1_opy_ (u"࡛ࠦ࡯ࡳࡶࡣ࡯ࠤࡘࡺࡵࡥ࡫ࡲࠤ࡙࡫ࡡ࡮ࠢࡖࡩࡷࡼࡩࡤࡧࡶࠦᆧ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᆨ"): bstack1l1l1_opy_ (u"ࠨࡻࡾࡽࢀࠦᆩ").format(env.get(bstack1l1l1_opy_ (u"ࠧࡔ࡛ࡖࡘࡊࡓ࡟ࡕࡇࡄࡑࡋࡕࡕࡏࡆࡄࡘࡎࡕࡎࡔࡇࡕ࡚ࡊࡘࡕࡓࡋࠪᆪ")), env.get(bstack1l1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡖࡒࡐࡌࡈࡇ࡙ࡏࡄࠨᆫ"))),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᆬ"): env.get(bstack1l1l1_opy_ (u"ࠥࡗ࡞࡙ࡔࡆࡏࡢࡈࡊࡌࡉࡏࡋࡗࡍࡔࡔࡉࡅࠤᆭ")),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᆮ"): env.get(bstack1l1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡌࡈࠧᆯ"))
        }
    if bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠨࡁࡑࡒ࡙ࡉ࡞ࡕࡒࠣᆰ"))):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆱ"): bstack1l1l1_opy_ (u"ࠣࡃࡳࡴࡻ࡫ࡹࡰࡴࠥᆲ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᆳ"): bstack1l1l1_opy_ (u"ࠥࡿࢂ࠵ࡰࡳࡱ࡭ࡩࡨࡺ࠯ࡼࡿ࠲ࡿࢂ࠵ࡢࡶ࡫࡯ࡨࡸ࠵ࡻࡾࠤᆴ").format(env.get(bstack1l1l1_opy_ (u"ࠫࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡕࡓࡎࠪᆵ")), env.get(bstack1l1l1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡂࡅࡆࡓ࡚ࡔࡔࡠࡐࡄࡑࡊ࠭ᆶ")), env.get(bstack1l1l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡒࡕࡓࡏࡋࡃࡕࡡࡖࡐ࡚ࡍࠧᆷ")), env.get(bstack1l1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠫᆸ"))),
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᆹ"): env.get(bstack1l1l1_opy_ (u"ࠤࡄࡔࡕ࡜ࡅ࡚ࡑࡕࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᆺ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤᆻ"): env.get(bstack1l1l1_opy_ (u"ࠦࡆࡖࡐࡗࡇ࡜ࡓࡗࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࠧᆼ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠧࡇ࡚ࡖࡔࡈࡣࡍ࡚ࡔࡑࡡࡘࡗࡊࡘ࡟ࡂࡉࡈࡒ࡙ࠨᆽ")) and env.get(bstack1l1l1_opy_ (u"ࠨࡔࡇࡡࡅ࡙ࡎࡒࡄࠣᆾ")):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᆿ"): bstack1l1l1_opy_ (u"ࠣࡃࡽࡹࡷ࡫ࠠࡄࡋࠥᇀ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇁ"): bstack1l1l1_opy_ (u"ࠥࡿࢂࢁࡽ࠰ࡡࡥࡹ࡮ࡲࡤ࠰ࡴࡨࡷࡺࡲࡴࡴࡁࡥࡹ࡮ࡲࡤࡊࡦࡀࡿࢂࠨᇂ").format(env.get(bstack1l1l1_opy_ (u"ࠫࡘ࡟ࡓࡕࡇࡐࡣ࡙ࡋࡁࡎࡈࡒ࡙ࡓࡊࡁࡕࡋࡒࡒࡘࡋࡒࡗࡇࡕ࡙ࡗࡏࠧᇃ")), env.get(bstack1l1l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡓࡖࡔࡐࡅࡄࡖࠪᇄ")), env.get(bstack1l1l1_opy_ (u"࠭ࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉ࠭ᇅ"))),
            bstack1l1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᇆ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡏࡄࠣᇇ")),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᇈ"): env.get(bstack1l1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡊࡆࠥᇉ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᇊ")), env.get(bstack1l1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡔࡈࡗࡔࡒࡖࡆࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦᇋ")), env.get(bstack1l1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡖࡓ࡚ࡘࡃࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࠥᇌ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧᇍ"): bstack1l1l1_opy_ (u"ࠣࡃ࡚ࡗࠥࡉ࡯ࡥࡧࡅࡹ࡮ࡲࡤࠣᇎ"),
            bstack1l1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧᇏ"): env.get(bstack1l1l1_opy_ (u"ࠥࡇࡔࡊࡅࡃࡗࡌࡐࡉࡥࡐࡖࡄࡏࡍࡈࡥࡂࡖࡋࡏࡈࡤ࡛ࡒࡍࠤᇐ")),
            bstack1l1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨᇑ"): env.get(bstack1l1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᇒ")),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᇓ"): env.get(bstack1l1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠧᇔ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡤࡸ࡭ࡱࡪࡎࡶ࡯ࡥࡩࡷࠨᇕ")):
        return {
            bstack1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᇖ"): bstack1l1l1_opy_ (u"ࠥࡆࡦࡳࡢࡰࡱࠥᇗ"),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᇘ"): env.get(bstack1l1l1_opy_ (u"ࠧࡨࡡ࡮ࡤࡲࡳࡤࡨࡵࡪ࡮ࡧࡖࡪࡹࡵ࡭ࡶࡶ࡙ࡷࡲࠢᇙ")),
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇚ"): env.get(bstack1l1l1_opy_ (u"ࠢࡣࡣࡰࡦࡴࡵ࡟ࡴࡪࡲࡶࡹࡐ࡯ࡣࡐࡤࡱࡪࠨᇛ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇜ"): env.get(bstack1l1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢᇝ"))
        }
    if env.get(bstack1l1l1_opy_ (u"࡛ࠥࡊࡘࡃࡌࡇࡕࠦᇞ")) or env.get(bstack1l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᇟ")):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᇠ"): bstack1l1l1_opy_ (u"ࠨࡗࡦࡴࡦ࡯ࡪࡸࠢᇡ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᇢ"): env.get(bstack1l1l1_opy_ (u"࡙ࠣࡈࡖࡈࡑࡅࡓࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧᇣ")),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᇤ"): bstack1l1l1_opy_ (u"ࠥࡑࡦ࡯࡮ࠡࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠥᇥ") if env.get(bstack1l1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࡤࡓࡁࡊࡐࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤ࡙ࡔࡂࡔࡗࡉࡉࠨᇦ")) else None,
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇧ"): env.get(bstack1l1l1_opy_ (u"ࠨࡗࡆࡔࡆࡏࡊࡘ࡟ࡈࡋࡗࡣࡈࡕࡍࡎࡋࡗࠦᇨ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠢࡈࡅࡓࡣࡕࡘࡏࡋࡇࡆࡘࠧᇩ")), env.get(bstack1l1l1_opy_ (u"ࠣࡉࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᇪ")), env.get(bstack1l1l1_opy_ (u"ࠤࡊࡓࡔࡍࡌࡆࡡࡆࡐࡔ࡛ࡄࡠࡒࡕࡓࡏࡋࡃࡕࠤᇫ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᇬ"): bstack1l1l1_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡈࡲ࡯ࡶࡦࠥᇭ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᇮ"): None,
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᇯ"): env.get(bstack1l1l1_opy_ (u"ࠢࡑࡔࡒࡎࡊࡉࡔࡠࡋࡇࠦᇰ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᇱ"): env.get(bstack1l1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᇲ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡗࡍࡏࡐࡑࡃࡅࡐࡊࠨᇳ")):
        return {
            bstack1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᇴ"): bstack1l1l1_opy_ (u"࡙ࠧࡨࡪࡲࡳࡥࡧࡲࡥࠣᇵ"),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᇶ"): env.get(bstack1l1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨᇷ")),
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥᇸ"): bstack1l1l1_opy_ (u"ࠤࡍࡳࡧࠦࠣࡼࡿࠥᇹ").format(env.get(bstack1l1l1_opy_ (u"ࠪࡗࡍࡏࡐࡑࡃࡅࡐࡊࡥࡊࡐࡄࡢࡍࡉ࠭ᇺ"))) if env.get(bstack1l1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠢᇻ")) else None,
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦᇼ"): env.get(bstack1l1l1_opy_ (u"ࠨࡓࡉࡋࡓࡔࡆࡈࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣᇽ"))
        }
    if bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠢࡏࡇࡗࡐࡎࡌ࡙ࠣᇾ"))):
        return {
            bstack1l1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨᇿ"): bstack1l1l1_opy_ (u"ࠤࡑࡩࡹࡲࡩࡧࡻࠥሀ"),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨሁ"): env.get(bstack1l1l1_opy_ (u"ࠦࡉࡋࡐࡍࡑ࡜ࡣ࡚ࡘࡌࠣሂ")),
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢሃ"): env.get(bstack1l1l1_opy_ (u"ࠨࡓࡊࡖࡈࡣࡓࡇࡍࡆࠤሄ")),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨህ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሆ"))
        }
    if bstack1l1111111_opy_(env.get(bstack1l1l1_opy_ (u"ࠤࡊࡍ࡙ࡎࡕࡃࡡࡄࡇ࡙ࡏࡏࡏࡕࠥሇ"))):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣለ"): bstack1l1l1_opy_ (u"ࠦࡌ࡯ࡴࡉࡷࡥࠤࡆࡩࡴࡪࡱࡱࡷࠧሉ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሊ"): bstack1l1l1_opy_ (u"ࠨࡻࡾ࠱ࡾࢁ࠴ࡧࡣࡵ࡫ࡲࡲࡸ࠵ࡲࡶࡰࡶ࠳ࢀࢃࠢላ").format(env.get(bstack1l1l1_opy_ (u"ࠧࡈࡋࡗࡌ࡚ࡈ࡟ࡔࡇࡕ࡚ࡊࡘ࡟ࡖࡔࡏࠫሌ")), env.get(bstack1l1l1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡔࡈࡔࡔ࡙ࡉࡕࡑࡕ࡝ࠬል")), env.get(bstack1l1l1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕ࡙ࡓࡥࡉࡅࠩሎ"))),
            bstack1l1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧሏ"): env.get(bstack1l1l1_opy_ (u"ࠦࡌࡏࡔࡉࡗࡅࡣ࡜ࡕࡒࡌࡈࡏࡓ࡜ࠨሐ")),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦሑ"): env.get(bstack1l1l1_opy_ (u"ࠨࡇࡊࡖࡋ࡙ࡇࡥࡒࡖࡐࡢࡍࡉࠨሒ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠢࡄࡋࠥሓ")) == bstack1l1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨሔ") and env.get(bstack1l1l1_opy_ (u"ࠤ࡙ࡉࡗࡉࡅࡍࠤሕ")) == bstack1l1l1_opy_ (u"ࠥ࠵ࠧሖ"):
        return {
            bstack1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሗ"): bstack1l1l1_opy_ (u"ࠧ࡜ࡥࡳࡥࡨࡰࠧመ"),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሙ"): bstack1l1l1_opy_ (u"ࠢࡩࡶࡷࡴ࠿࠵࠯ࡼࡿࠥሚ").format(env.get(bstack1l1l1_opy_ (u"ࠨࡘࡈࡖࡈࡋࡌࡠࡗࡕࡐࠬማ"))),
            bstack1l1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦሜ"): None,
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤም"): None,
        }
    if env.get(bstack1l1l1_opy_ (u"࡙ࠦࡋࡁࡎࡅࡌࡘ࡞ࡥࡖࡆࡔࡖࡍࡔࡔࠢሞ")):
        return {
            bstack1l1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥሟ"): bstack1l1l1_opy_ (u"ࠨࡔࡦࡣࡰࡧ࡮ࡺࡹࠣሠ"),
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥሡ"): None,
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሢ"): env.get(bstack1l1l1_opy_ (u"ࠤࡗࡉࡆࡓࡃࡊࡖ࡜ࡣࡕࡘࡏࡋࡇࡆࡘࡤࡔࡁࡎࡇࠥሣ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤሤ"): env.get(bstack1l1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡒ࡚ࡓࡂࡆࡔࠥሥ"))
        }
    if any([env.get(bstack1l1l1_opy_ (u"ࠧࡉࡏࡏࡅࡒ࡙ࡗ࡙ࡅࠣሦ")), env.get(bstack1l1l1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࡡࡘࡖࡑࠨሧ")), env.get(bstack1l1l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠧረ")), env.get(bstack1l1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡙ࡋࡁࡎࠤሩ"))]):
        return {
            bstack1l1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢሪ"): bstack1l1l1_opy_ (u"ࠥࡇࡴࡴࡣࡰࡷࡵࡷࡪࠨራ"),
            bstack1l1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢሬ"): None,
            bstack1l1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢር"): env.get(bstack1l1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሮ")) or None,
            bstack1l1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨሯ"): env.get(bstack1l1l1_opy_ (u"ࠣࡄࡘࡍࡑࡊ࡟ࡊࡆࠥሰ"), 0)
        }
    if env.get(bstack1l1l1_opy_ (u"ࠤࡊࡓࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢሱ")):
        return {
            bstack1l1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣሲ"): bstack1l1l1_opy_ (u"ࠦࡌࡵࡃࡅࠤሳ"),
            bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣሴ"): None,
            bstack1l1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣስ"): env.get(bstack1l1l1_opy_ (u"ࠢࡈࡑࡢࡎࡔࡈ࡟ࡏࡃࡐࡉࠧሶ")),
            bstack1l1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢሷ"): env.get(bstack1l1l1_opy_ (u"ࠤࡊࡓࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡄࡑࡘࡒ࡙ࡋࡒࠣሸ"))
        }
    if env.get(bstack1l1l1_opy_ (u"ࠥࡇࡋࡥࡂࡖࡋࡏࡈࡤࡏࡄࠣሹ")):
        return {
            bstack1l1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤሺ"): bstack1l1l1_opy_ (u"ࠧࡉ࡯ࡥࡧࡉࡶࡪࡹࡨࠣሻ"),
            bstack1l1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤሼ"): env.get(bstack1l1l1_opy_ (u"ࠢࡄࡈࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨሽ")),
            bstack1l1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥሾ"): env.get(bstack1l1l1_opy_ (u"ࠤࡆࡊࡤࡖࡉࡑࡇࡏࡍࡓࡋ࡟ࡏࡃࡐࡉࠧሿ")),
            bstack1l1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤቀ"): env.get(bstack1l1l1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤቁ"))
        }
    return {bstack1l1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦቂ"): None}
def get_host_info():
    return {
        bstack1l1l1_opy_ (u"ࠨࡨࡰࡵࡷࡲࡦࡳࡥࠣቃ"): platform.node(),
        bstack1l1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠤቄ"): platform.system(),
        bstack1l1l1_opy_ (u"ࠣࡶࡼࡴࡪࠨቅ"): platform.machine(),
        bstack1l1l1_opy_ (u"ࠤࡹࡩࡷࡹࡩࡰࡰࠥቆ"): platform.version(),
        bstack1l1l1_opy_ (u"ࠥࡥࡷࡩࡨࠣቇ"): platform.architecture()[0]
    }
def bstack1lll111l_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack11l1l111l1_opy_():
    if bstack1l11lll11_opy_.get_property(bstack1l1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬቈ")):
        return bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ቉")
    return bstack1l1l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴ࡟ࡨࡴ࡬ࡨࠬቊ")
def bstack11l11lllll_opy_(driver):
    info = {
        bstack1l1l1_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ቋ"): driver.capabilities,
        bstack1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡡ࡬ࡨࠬቌ"): driver.session_id,
        bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪቍ"): driver.capabilities.get(bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ቎"), None),
        bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭቏"): driver.capabilities.get(bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ቐ"), None),
        bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠨቑ"): driver.capabilities.get(bstack1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ቒ"), None),
    }
    if bstack11l1l111l1_opy_() == bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧቓ"):
        info[bstack1l1l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࠪቔ")] = bstack1l1l1_opy_ (u"ࠪࡥࡵࡶ࠭ࡢࡷࡷࡳࡲࡧࡴࡦࠩቕ") if bstack11l1l111_opy_() else bstack1l1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ቖ")
    return info
def bstack11l1l111_opy_():
    if bstack1l11lll11_opy_.get_property(bstack1l1l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ቗")):
        return True
    if bstack1l1111111_opy_(os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧቘ"), None)):
        return True
    return False
def bstack1ll11111ll_opy_(bstack11l1l11l11_opy_, url, data, config):
    headers = config.get(bstack1l1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ቙"), None)
    proxies = bstack1ll11l1l1l_opy_(config, url)
    auth = config.get(bstack1l1l1_opy_ (u"ࠨࡣࡸࡸ࡭࠭ቚ"), None)
    response = requests.request(
            bstack11l1l11l11_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1l1ll1l1ll_opy_(bstack1llllll11l_opy_, size):
    bstack1l1l1lll11_opy_ = []
    while len(bstack1llllll11l_opy_) > size:
        bstack111l1l11l_opy_ = bstack1llllll11l_opy_[:size]
        bstack1l1l1lll11_opy_.append(bstack111l1l11l_opy_)
        bstack1llllll11l_opy_ = bstack1llllll11l_opy_[size:]
    bstack1l1l1lll11_opy_.append(bstack1llllll11l_opy_)
    return bstack1l1l1lll11_opy_
def bstack11l1l11lll_opy_(message, bstack11l1ll111l_opy_=False):
    os.write(1, bytes(message, bstack1l1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨቛ")))
    os.write(1, bytes(bstack1l1l1_opy_ (u"ࠪࡠࡳ࠭ቜ"), bstack1l1l1_opy_ (u"ࠫࡺࡺࡦ࠮࠺ࠪቝ")))
    if bstack11l1ll111l_opy_:
        with open(bstack1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠲ࡵ࠱࠲ࡻ࠰ࠫ቞") + os.environ[bstack1l1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ቟")] + bstack1l1l1_opy_ (u"ࠧ࠯࡮ࡲ࡫ࠬበ"), bstack1l1l1_opy_ (u"ࠨࡣࠪቡ")) as f:
            f.write(message + bstack1l1l1_opy_ (u"ࠩ࡟ࡲࠬቢ"))
def bstack11l1l1111l_opy_():
    return os.environ[bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄ࡙࡙ࡕࡍࡂࡖࡌࡓࡓ࠭ባ")].lower() == bstack1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩቤ")
def bstack11lllllll_opy_(bstack11l1l1ll1l_opy_):
    return bstack1l1l1_opy_ (u"ࠬࢁࡽ࠰ࡽࢀࠫብ").format(bstack11ll11lll1_opy_, bstack11l1l1ll1l_opy_)
def bstack1l11lllll_opy_():
    return datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"࡚࠭ࠨቦ")
def bstack11ll111lll_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1l1l1_opy_ (u"࡛ࠧࠩቧ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1l1l1_opy_ (u"ࠨ࡜ࠪቨ")))).total_seconds() * 1000
def bstack11l1ll1l11_opy_(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫቩ")
def bstack11l11ll1ll_opy_(bstack11l11lll11_opy_):
    date_format = bstack1l1l1_opy_ (u"ࠪࠩ࡞ࠫ࡭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨቪ")
    bstack11l1l11ll1_opy_ = datetime.datetime.strptime(bstack11l11lll11_opy_, date_format)
    return bstack11l1l11ll1_opy_.isoformat() + bstack1l1l1_opy_ (u"ࠫ࡟࠭ቫ")
def bstack11ll111ll1_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬቬ")
    else:
        return bstack1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ቭ")
def bstack1l1111111_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1l1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬቮ")
def bstack11ll11l11l_opy_(val):
    return val.__str__().lower() == bstack1l1l1_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧቯ")
def bstack1l111llll1_opy_(bstack11l1ll1ll1_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack11l1ll1ll1_opy_ as e:
                print(bstack1l1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡿࢂࠦ࠭࠿ࠢࡾࢁ࠿ࠦࡻࡾࠤተ").format(func.__name__, bstack11l1ll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11l1llll1l_opy_(bstack11l1l1l1l1_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack11l1l1l1l1_opy_(cls, *args, **kwargs)
            except bstack11l1ll1ll1_opy_ as e:
                print(bstack1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥቱ").format(bstack11l1l1l1l1_opy_.__name__, bstack11l1ll1ll1_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11l1llll1l_opy_
    else:
        return decorator
def bstack1ll1llll11_opy_(bstack11lllll11l_opy_):
    if bstack1l1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቲ") in bstack11lllll11l_opy_ and bstack11ll11l11l_opy_(bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩታ")]):
        return False
    if bstack1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨቴ") in bstack11lllll11l_opy_ and bstack11ll11l11l_opy_(bstack11lllll11l_opy_[bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩት")]):
        return False
    return True
def bstack1l1l1ll1ll_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1l111l111_opy_(hub_url):
    if bstack1ll111l11l_opy_() <= version.parse(bstack1l1l1_opy_ (u"ࠨ࠵࠱࠵࠸࠴࠰ࠨቶ")):
        if hub_url != bstack1l1l1_opy_ (u"ࠩࠪቷ"):
            return bstack1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦቸ") + hub_url + bstack1l1l1_opy_ (u"ࠦ࠿࠾࠰࠰ࡹࡧ࠳࡭ࡻࡢࠣቹ")
        return bstack11lllll1l_opy_
    if hub_url != bstack1l1l1_opy_ (u"ࠬ࠭ቺ"):
        return bstack1l1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷ࠿࠵࠯ࠣቻ") + hub_url + bstack1l1l1_opy_ (u"ࠢ࠰ࡹࡧ࠳࡭ࡻࡢࠣቼ")
    return bstack1l1ll1lll_opy_
def bstack11ll1111ll_opy_():
    return isinstance(os.getenv(bstack1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑ࡛ࡗࡉࡘ࡚࡟ࡑࡎࡘࡋࡎࡔࠧች")), str)
def bstack11l111ll1_opy_(url):
    return urlparse(url).hostname
def bstack1ll1111ll1_opy_(hostname):
    for bstack1l1l1l111_opy_ in bstack1ll111l1l1_opy_:
        regex = re.compile(bstack1l1l1l111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11l11lll1l_opy_(bstack11l1l1l111_opy_, file_name, logger):
    bstack1llll1lll1_opy_ = os.path.join(os.path.expanduser(bstack1l1l1_opy_ (u"ࠩࢁࠫቾ")), bstack11l1l1l111_opy_)
    try:
        if not os.path.exists(bstack1llll1lll1_opy_):
            os.makedirs(bstack1llll1lll1_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1l1l1_opy_ (u"ࠪࢂࠬቿ")), bstack11l1l1l111_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1l1l1_opy_ (u"ࠫࡼ࠭ኀ")):
                pass
            with open(file_path, bstack1l1l1_opy_ (u"ࠧࡽࠫࠣኁ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack111111l1_opy_.format(str(e)))
def bstack11l1l11111_opy_(file_name, key, value, logger):
    file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ኂ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1llll11111_opy_ = json.load(open(file_path, bstack1l1l1_opy_ (u"ࠧࡳࡤࠪኃ")))
        else:
            bstack1llll11111_opy_ = {}
        bstack1llll11111_opy_[key] = value
        with open(file_path, bstack1l1l1_opy_ (u"ࠣࡹ࠮ࠦኄ")) as outfile:
            json.dump(bstack1llll11111_opy_, outfile)
def bstack11llll1l_opy_(file_name, logger):
    file_path = bstack11l11lll1l_opy_(bstack1l1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩኅ"), file_name, logger)
    bstack1llll11111_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1l1l1_opy_ (u"ࠪࡶࠬኆ")) as bstack11llllll_opy_:
            bstack1llll11111_opy_ = json.load(bstack11llllll_opy_)
    return bstack1llll11111_opy_
def bstack1l1ll1l111_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡨ࡬ࡰࡪࡀࠠࠨኇ") + file_path + bstack1l1l1_opy_ (u"ࠬࠦࠧኈ") + str(e))
def bstack1ll111l11l_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1l1l1_opy_ (u"ࠨ࠼ࡏࡑࡗࡗࡊ࡚࠾ࠣ኉")
def bstack111llll1l_opy_(config):
    if bstack1l1l1_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠭ኊ") in config:
        del (config[bstack1l1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧኋ")])
        return False
    if bstack1ll111l11l_opy_() < version.parse(bstack1l1l1_opy_ (u"ࠩ࠶࠲࠹࠴࠰ࠨኌ")):
        return False
    if bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠪ࠸࠳࠷࠮࠶ࠩኍ")):
        return True
    if bstack1l1l1_opy_ (u"ࠫࡺࡹࡥࡘ࠵ࡆࠫ኎") in config and config[bstack1l1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬ኏")] is False:
        return False
    else:
        return True
def bstack1lll1ll1_opy_(args_list, bstack11ll11l1l1_opy_):
    index = -1
    for value in bstack11ll11l1l1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack1l11ll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack1l11ll1ll1_opy_ = bstack1l11ll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1l1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ነ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧኑ"), exception=exception)
    def bstack11llll1ll1_opy_(self):
        if self.result != bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨኒ"):
            return None
        if bstack1l1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧና") in self.exception_type:
            return bstack1l1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦኔ")
        return bstack1l1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧን")
    def bstack11ll11111l_opy_(self):
        if self.result != bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬኖ"):
            return None
        if self.bstack1l11ll1ll1_opy_:
            return self.bstack1l11ll1ll1_opy_
        return bstack11l11llll1_opy_(self.exception)
def bstack11l11llll1_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack11ll111l11_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1lllll11l_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1111l1_opy_(config, logger):
    try:
        import playwright
        bstack11ll111111_opy_ = playwright.__file__
        bstack11l1ll1111_opy_ = os.path.split(bstack11ll111111_opy_)
        bstack11l1ll11l1_opy_ = bstack11l1ll1111_opy_[0] + bstack1l1l1_opy_ (u"࠭࠯ࡥࡴ࡬ࡺࡪࡸ࠯ࡱࡣࡦ࡯ࡦ࡭ࡥ࠰࡮࡬ࡦ࠴ࡩ࡬ࡪ࠱ࡦࡰ࡮࠴ࡪࡴࠩኗ")
        os.environ[bstack1l1l1_opy_ (u"ࠧࡈࡎࡒࡆࡆࡒ࡟ࡂࡉࡈࡒ࡙ࡥࡈࡕࡖࡓࡣࡕࡘࡏ࡙࡛ࠪኘ")] = bstack1l111lll1_opy_(config)
        with open(bstack11l1ll11l1_opy_, bstack1l1l1_opy_ (u"ࠨࡴࠪኙ")) as f:
            bstack11ll111l1_opy_ = f.read()
            bstack11l1l1lll1_opy_ = bstack1l1l1_opy_ (u"ࠩࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠨኚ")
            bstack11l1l1l11l_opy_ = bstack11ll111l1_opy_.find(bstack11l1l1lll1_opy_)
            if bstack11l1l1l11l_opy_ == -1:
              process = subprocess.Popen(bstack1l1l1_opy_ (u"ࠥࡲࡵࡳࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡩ࡯ࡳࡧࡧ࡬࠮ࡣࡪࡩࡳࡺࠢኛ"), shell=True, cwd=bstack11l1ll1111_opy_[0])
              process.wait()
              bstack11l1l11l1l_opy_ = bstack1l1l1_opy_ (u"ࠫࠧࡻࡳࡦࠢࡶࡸࡷ࡯ࡣࡵࠤ࠾ࠫኜ")
              bstack11l1llll11_opy_ = bstack1l1l1_opy_ (u"ࠧࠨࠢࠡ࡞ࠥࡹࡸ࡫ࠠࡴࡶࡵ࡭ࡨࡺ࡜ࠣ࠽ࠣࡧࡴࡴࡳࡵࠢࡾࠤࡧࡵ࡯ࡵࡵࡷࡶࡦࡶࠠࡾࠢࡀࠤࡷ࡫ࡱࡶ࡫ࡵࡩ࠭࠭ࡧ࡭ࡱࡥࡥࡱ࠳ࡡࡨࡧࡱࡸࠬ࠯࠻ࠡ࡫ࡩࠤ࠭ࡶࡲࡰࡥࡨࡷࡸ࠴ࡥ࡯ࡸ࠱ࡋࡑࡕࡂࡂࡎࡢࡅࡌࡋࡎࡕࡡࡋࡘ࡙ࡖ࡟ࡑࡔࡒ࡜࡞࠯ࠠࡣࡱࡲࡸࡸࡺࡲࡢࡲࠫ࠭ࡀࠦࠢࠣࠤኝ")
              bstack11l1lll1l1_opy_ = bstack11ll111l1_opy_.replace(bstack11l1l11l1l_opy_, bstack11l1llll11_opy_)
              with open(bstack11l1ll11l1_opy_, bstack1l1l1_opy_ (u"࠭ࡷࠨኞ")) as f:
                f.write(bstack11l1lll1l1_opy_)
    except Exception as e:
        logger.error(bstack1l111111l_opy_.format(str(e)))
def bstack1llll11l1_opy_():
  try:
    bstack11ll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭࠰࡭ࡷࡴࡴࠧኟ"))
    bstack11l1ll1lll_opy_ = []
    if os.path.exists(bstack11ll11l1ll_opy_):
      with open(bstack11ll11l1ll_opy_) as f:
        bstack11l1ll1lll_opy_ = json.load(f)
      os.remove(bstack11ll11l1ll_opy_)
    return bstack11l1ll1lll_opy_
  except:
    pass
  return []
def bstack11lll11l1_opy_(bstack1lllll1l1_opy_):
  try:
    bstack11l1ll1lll_opy_ = []
    bstack11ll11l1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨአ"))
    if os.path.exists(bstack11ll11l1ll_opy_):
      with open(bstack11ll11l1ll_opy_) as f:
        bstack11l1ll1lll_opy_ = json.load(f)
    bstack11l1ll1lll_opy_.append(bstack1lllll1l1_opy_)
    with open(bstack11ll11l1ll_opy_, bstack1l1l1_opy_ (u"ࠩࡺࠫኡ")) as f:
        json.dump(bstack11l1ll1lll_opy_, f)
  except:
    pass
def bstack1llll1111_opy_(logger, bstack11ll111l1l_opy_ = False):
  try:
    test_name = os.environ.get(bstack1l1l1_opy_ (u"ࠪࡔ࡞࡚ࡅࡔࡖࡢࡘࡊ࡙ࡔࡠࡐࡄࡑࡊ࠭ኢ"), bstack1l1l1_opy_ (u"ࠫࠬኣ"))
    if test_name == bstack1l1l1_opy_ (u"ࠬ࠭ኤ"):
        test_name = threading.current_thread().__dict__.get(bstack1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹࡈࡤࡥࡡࡷࡩࡸࡺ࡟࡯ࡣࡰࡩࠬእ"), bstack1l1l1_opy_ (u"ࠧࠨኦ"))
    bstack11l1ll1l1l_opy_ = bstack1l1l1_opy_ (u"ࠨ࠮ࠣࠫኧ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack11ll111l1l_opy_:
        bstack1l1lll111l_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩከ"), bstack1l1l1_opy_ (u"ࠪ࠴ࠬኩ"))
        bstack1l1ll1l11l_opy_ = {bstack1l1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩኪ"): test_name, bstack1l1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫካ"): bstack11l1ll1l1l_opy_, bstack1l1l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬኬ"): bstack1l1lll111l_opy_}
        bstack11l1lllll1_opy_ = []
        bstack11l1lll1ll_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࡟ࡱࡲࡳࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ክ"))
        if os.path.exists(bstack11l1lll1ll_opy_):
            with open(bstack11l1lll1ll_opy_) as f:
                bstack11l1lllll1_opy_ = json.load(f)
        bstack11l1lllll1_opy_.append(bstack1l1ll1l11l_opy_)
        with open(bstack11l1lll1ll_opy_, bstack1l1l1_opy_ (u"ࠨࡹࠪኮ")) as f:
            json.dump(bstack11l1lllll1_opy_, f)
    else:
        bstack1l1ll1l11l_opy_ = {bstack1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧኯ"): test_name, bstack1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩኰ"): bstack11l1ll1l1l_opy_, bstack1l1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ኱"): str(multiprocessing.current_process().name)}
        if bstack1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩኲ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1l1ll1l11l_opy_)
  except Exception as e:
      logger.warn(bstack1l1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡲࡼࡸࡪࡹࡴࠡࡨࡸࡲࡳ࡫࡬ࠡࡦࡤࡸࡦࡀࠠࡼࡿࠥኳ").format(e))
def bstack11l11ll1l_opy_(error_message, test_name, index, logger):
  try:
    bstack11l1l1llll_opy_ = []
    bstack1l1ll1l11l_opy_ = {bstack1l1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬኴ"): test_name, bstack1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧኵ"): error_message, bstack1l1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨ኶"): index}
    bstack11l11ll1l1_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࡡࡨࡶࡷࡵࡲࡠ࡮࡬ࡷࡹ࠴ࡪࡴࡱࡱࠫ኷"))
    if os.path.exists(bstack11l11ll1l1_opy_):
        with open(bstack11l11ll1l1_opy_) as f:
            bstack11l1l1llll_opy_ = json.load(f)
    bstack11l1l1llll_opy_.append(bstack1l1ll1l11l_opy_)
    with open(bstack11l11ll1l1_opy_, bstack1l1l1_opy_ (u"ࠫࡼ࠭ኸ")) as f:
        json.dump(bstack11l1l1llll_opy_, f)
  except Exception as e:
    logger.warn(bstack1l1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡵࡷࡳࡷ࡫ࠠࡳࡱࡥࡳࡹࠦࡦࡶࡰࡱࡩࡱࠦࡤࡢࡶࡤ࠾ࠥࢁࡽࠣኹ").format(e))
def bstack1111lll11_opy_(bstack1l1l1l1l_opy_, name, logger):
  try:
    bstack1l1ll1l11l_opy_ = {bstack1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫኺ"): name, bstack1l1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ኻ"): bstack1l1l1l1l_opy_, bstack1l1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧኼ"): str(threading.current_thread()._name)}
    return bstack1l1ll1l11l_opy_
  except Exception as e:
    logger.warn(bstack1l1l1_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡹࡴࡰࡴࡨࠤࡧ࡫ࡨࡢࡸࡨࠤ࡫ࡻ࡮࡯ࡧ࡯ࠤࡩࡧࡴࡢ࠼ࠣࡿࢂࠨኽ").format(e))
  return
def bstack1lll11l1ll_opy_(framework):
    if framework.lower() == bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪኾ"):
        return bstack111l1l111_opy_.version()
    elif framework.lower() == bstack1l1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ኿"):
        return RobotHandler.version()
    elif framework.lower() == bstack1l1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬዀ"):
        import behave
        return behave.__version__
    else:
        return bstack1l1l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧ዁")