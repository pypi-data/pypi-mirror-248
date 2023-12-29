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
import atexit
import datetime
import inspect
import logging
import os
import signal
import sys
import threading
from uuid import uuid4
from bstack_utils.percy_sdk import PercySDK
import tempfile
import pytest
from packaging import version
from browserstack_sdk.__init__ import (bstack1lll1l1l1_opy_, bstack1lllllll1l_opy_, update, bstack1l1l1ll1l1_opy_,
                                       bstack1lll1l1l_opy_, bstack1ll1ll1ll1_opy_, bstack1lll11l11l_opy_, bstack1l111l1ll_opy_,
                                       bstack1l1lll111_opy_, bstack1ll111l1ll_opy_, bstack1l11ll1l_opy_, bstack1lll1lll1l_opy_,
                                       bstack1lll111l1l_opy_, getAccessibilityResults, getAccessibilityResultsSummary)
from browserstack_sdk._version import __version__
from bstack_utils.capture import bstack1l1111l1l1_opy_
from bstack_utils.config import Config
from bstack_utils.constants import bstack1lll111l11_opy_, bstack11l11111_opy_, bstack1llll1llll_opy_, bstack1l1llllll_opy_, \
    bstack111lllll1_opy_
from bstack_utils.helper import bstack1lllll11l_opy_, bstack1lll111l_opy_, bstack11l1l1111l_opy_, bstack1l11lllll_opy_, \
    bstack11ll111ll1_opy_, \
    bstack11l1lll111_opy_, bstack1ll111l11l_opy_, bstack1l111l111_opy_, bstack11ll1111ll_opy_, bstack1l1l1ll1ll_opy_, Notset, \
    bstack111llll1l_opy_, bstack11ll111lll_opy_, bstack11l11llll1_opy_, Result, bstack11l1ll1l11_opy_, bstack11ll111l11_opy_, bstack1l111llll1_opy_, \
    bstack11lll11l1_opy_, bstack1llll1111_opy_, bstack1l1111111_opy_
from bstack_utils.bstack11l111llll_opy_ import bstack11l11ll111_opy_
from bstack_utils.messages import bstack1l11ll1ll_opy_, bstack111lll111_opy_, bstack111llllll_opy_, bstack1ll11llll_opy_, bstack1ll11l1l11_opy_, \
    bstack1l111111l_opy_, bstack1l1llll1ll_opy_, bstack1l1llll111_opy_, bstack11l11llll_opy_, bstack111l11ll1_opy_, \
    bstack1ll1ll11ll_opy_, bstack1ll1llll1_opy_
from bstack_utils.proxy import bstack1l111lll1_opy_, bstack1111l11ll_opy_
from bstack_utils.bstack1111l1ll1_opy_ import bstack1111l1lll1_opy_, bstack1111l1llll_opy_, bstack1111ll111l_opy_, bstack1111ll1ll1_opy_, \
    bstack1111ll11l1_opy_, bstack1111l1ll1l_opy_, bstack1111ll1l1l_opy_, bstack1l1111ll1_opy_, bstack1111lll111_opy_
from bstack_utils.bstack1ll1ll111l_opy_ import bstack11ll11111_opy_
from bstack_utils.bstack111ll1ll_opy_ import bstack1lll1111ll_opy_, bstack1lll1l1lll_opy_, bstack1ll111l111_opy_, \
    bstack11ll11ll_opy_, bstack11l1l11l_opy_
from bstack_utils.bstack1l1111l1ll_opy_ import bstack1l11lllll1_opy_
from bstack_utils.bstack1l11l1l1_opy_ import bstack1ll1l1llll_opy_
import bstack_utils.bstack1l11l1l11_opy_ as bstack11llllll1_opy_
bstack111l1l1l_opy_ = None
bstack11l1l1l1_opy_ = None
bstack1lll11ll11_opy_ = None
bstack111l1ll1l_opy_ = None
bstack1ll11lll11_opy_ = None
bstack1ll1llllll_opy_ = None
bstack1lllll1l11_opy_ = None
bstack1lllll111l_opy_ = None
bstack1llll111l_opy_ = None
bstack111ll111_opy_ = None
bstack1l1l1llll_opy_ = None
bstack1ll1lllll_opy_ = None
bstack111ll11ll_opy_ = None
bstack1lll111ll_opy_ = bstack1l1l1_opy_ (u"ࠬ࠭ᔯ")
CONFIG = {}
bstack1111111ll_opy_ = False
bstack11l1ll11_opy_ = bstack1l1l1_opy_ (u"࠭ࠧᔰ")
bstack1lll1111_opy_ = bstack1l1l1_opy_ (u"ࠧࠨᔱ")
bstack1l1111l1l_opy_ = False
bstack1l1l11ll11_opy_ = []
bstack1lllll1l1l_opy_ = bstack11l11111_opy_
bstack1lllll1ll1l_opy_ = bstack1l1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨᔲ")
bstack1lllll1llll_opy_ = False
bstack1l1ll11lll_opy_ = {}
logger = logging.getLogger(__name__)
logging.basicConfig(level=bstack1lllll1l1l_opy_,
                    format=bstack1l1l1_opy_ (u"ࠩ࡟ࡲࠪ࠮ࡡࡴࡥࡷ࡭ࡲ࡫ࠩࡴࠢ࡞ࠩ࠭ࡴࡡ࡮ࡧࠬࡷࡢࡡࠥࠩ࡮ࡨࡺࡪࡲ࡮ࡢ࡯ࡨ࠭ࡸࡣࠠ࠮ࠢࠨࠬࡲ࡫ࡳࡴࡣࡪࡩ࠮ࡹࠧᔳ"),
                    datefmt=bstack1l1l1_opy_ (u"ࠪࠩࡍࡀࠥࡎ࠼ࠨࡗࠬᔴ"),
                    stream=sys.stdout)
store = {
    bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᔵ"): []
}
bstack1lllll111ll_opy_ = False
def bstack1ll1lll1l_opy_():
    global CONFIG
    global bstack1lllll1l1l_opy_
    if bstack1l1l1_opy_ (u"ࠬࡲ࡯ࡨࡎࡨࡺࡪࡲࠧᔶ") in CONFIG:
        bstack1lllll1l1l_opy_ = bstack1lll111l11_opy_[CONFIG[bstack1l1l1_opy_ (u"࠭࡬ࡰࡩࡏࡩࡻ࡫࡬ࠨᔷ")]]
        logging.getLogger().setLevel(bstack1lllll1l1l_opy_)
try:
    from playwright.sync_api import (
        BrowserContext,
        Page
    )
except:
    pass
import json
_1l111l111l_opy_ = {}
current_test_uuid = None
def bstack1l1lllll1_opy_(page, bstack11l11l1ll_opy_):
    try:
        page.evaluate(bstack1l1l1_opy_ (u"ࠢࡠࠢࡀࡂࠥࢁࡽࠣᔸ"),
                      bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠤ࠯ࠤࠧࡧࡲࡨࡷࡰࡩࡳࡺࡳࠣ࠼ࠣࡿࠧࡴࡡ࡮ࡧࠥ࠾ࠬᔹ") + json.dumps(
                          bstack11l11l1ll_opy_) + bstack1l1l1_opy_ (u"ࠤࢀࢁࠧᔺ"))
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠥࡩࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠦࡳࡦࡵࡶ࡭ࡴࡴࠠ࡯ࡣࡰࡩࠥࢁࡽࠣᔻ"), e)
def bstack1ll1l1l111_opy_(page, message, level):
    try:
        page.evaluate(bstack1l1l1_opy_ (u"ࠦࡤࠦ࠽࠿ࠢࡾࢁࠧᔼ"), bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪᔽ") + json.dumps(
            message) + bstack1l1l1_opy_ (u"࠭ࠬࠣ࡮ࡨࡺࡪࡲࠢ࠻ࠩᔾ") + json.dumps(level) + bstack1l1l1_opy_ (u"ࠧࡾࡿࠪᔿ"))
    except Exception as e:
        print(bstack1l1l1_opy_ (u"ࠣࡧࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࡦࡴ࡮ࡰࡶࡤࡸ࡮ࡵ࡮ࠡࡽࢀࠦᕀ"), e)
def pytest_configure(config):
    bstack1l11lll11_opy_ = Config.get_instance()
    config.args = bstack1ll1l1llll_opy_.bstack11111111l1_opy_(config.args)
    bstack1l11lll11_opy_.bstack1l111l11_opy_(bstack1l1111111_opy_(config.getoption(bstack1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡓࡦࡵࡶ࡭ࡴࡴࡓࡵࡣࡷࡹࡸ࠭ᕁ"))))
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    bstack1llll1l1111_opy_ = item.config.getoption(bstack1l1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᕂ"))
    plugins = item.config.getoption(bstack1l1l1_opy_ (u"ࠦࡵࡲࡵࡨ࡫ࡱࡷࠧᕃ"))
    report = outcome.get_result()
    bstack1llll1l1l11_opy_(item, call, report)
    if bstack1l1l1_opy_ (u"ࠧࡶࡹࡵࡧࡶࡸࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡴࡱࡻࡧࡪࡰࠥᕄ") not in plugins or bstack1l1l1ll1ll_opy_():
        return
    summary = []
    driver = getattr(item, bstack1l1l1_opy_ (u"ࠨ࡟ࡥࡴ࡬ࡺࡪࡸࠢᕅ"), None)
    page = getattr(item, bstack1l1l1_opy_ (u"ࠢࡠࡲࡤ࡫ࡪࠨᕆ"), None)
    try:
        if (driver == None):
            driver = threading.current_thread().bstackSessionDriver
    except:
        pass
    item._driver = driver
    if (driver is not None):
        bstack1llll1llll1_opy_(item, report, summary, bstack1llll1l1111_opy_)
    if (page is not None):
        bstack1llll1lll11_opy_(item, report, summary, bstack1llll1l1111_opy_)
def bstack1llll1llll1_opy_(item, report, summary, bstack1llll1l1111_opy_):
    if report.when == bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶࠧᕇ") and report.skipped:
        bstack1111lll111_opy_(report)
    if report.when in [bstack1l1l1_opy_ (u"ࠤࡶࡩࡹࡻࡰࠣᕈ"), bstack1l1l1_opy_ (u"ࠥࡸࡪࡧࡲࡥࡱࡺࡲࠧᕉ")]:
        return
    if not bstack11l1l1111l_opy_():
        return
    try:
        if (str(bstack1llll1l1111_opy_).lower() != bstack1l1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩᕊ")):
            item._driver.execute_script(
                bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡹࡥࡵࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡱࡥࡲ࡫ࠢ࠻ࠢࠪᕋ") + json.dumps(
                    report.nodeid) + bstack1l1l1_opy_ (u"࠭ࡽࡾࠩᕌ"))
        os.environ[bstack1l1l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᕍ")] = report.nodeid
    except Exception as e:
        summary.append(
            bstack1l1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧ࠽ࠤࢀ࠶ࡽࠣᕎ").format(e)
        )
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᕏ")))
    bstack1ll111ll_opy_ = bstack1l1l1_opy_ (u"ࠥࠦᕐ")
    bstack1111lll111_opy_(report)
    if not passed:
        try:
            bstack1ll111ll_opy_ = report.longrepr.reprcrash
        except Exception as e:
            summary.append(
                bstack1l1l1_opy_ (u"ࠦ࡜ࡇࡒࡏࡋࡑࡋ࠿ࠦࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥ࡬ࡡࡪ࡮ࡸࡶࡪࠦࡲࡦࡣࡶࡳࡳࡀࠠࡼ࠲ࢀࠦᕑ").format(e)
            )
        try:
            if (threading.current_thread().bstackTestErrorMessages == None):
                threading.current_thread().bstackTestErrorMessages = []
        except Exception as e:
            threading.current_thread().bstackTestErrorMessages = []
        threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111ll_opy_))
    if not report.skipped:
        passed = report.passed or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠧࡽࡡࡴࡺࡩࡥ࡮ࡲࠢᕒ")))
        bstack1ll111ll_opy_ = bstack1l1l1_opy_ (u"ࠨࠢᕓ")
        if not passed:
            try:
                bstack1ll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1_opy_ (u"ࠢࡘࡃࡕࡒࡎࡔࡇ࠻ࠢࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡪࡥࡵࡧࡵࡱ࡮ࡴࡥࠡࡨࡤ࡭ࡱࡻࡲࡦࠢࡵࡩࡦࡹ࡯࡯࠼ࠣࡿ࠵ࢃࠢᕔ").format(e)
                )
            try:
                if (threading.current_thread().bstackTestErrorMessages == None):
                    threading.current_thread().bstackTestErrorMessages = []
            except Exception as e:
                threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(str(bstack1ll111ll_opy_))
        try:
            if passed:
                item._driver.execute_script(
                    bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠢࡢࡥࡷ࡭ࡴࡴࠢ࠻ࠢࠥࡥࡳࡴ࡯ࡵࡣࡷࡩࠧ࠲ࠠ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽ࡟ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤ࠯ࠤࡡࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠦࡩࡧࡴࡢࠤ࠽ࠤࠬᕕ")
                    + json.dumps(bstack1l1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠣࠥᕖ"))
                    + bstack1l1l1_opy_ (u"ࠥࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࢃ࡜ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࢂࠨᕗ")
                )
            else:
                item._driver.execute_script(
                    bstack1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻ࡝ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡡ࡯ࡰࡲࡸࡦࡺࡥࠣ࠮ࠣࡠࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࠬࠡ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠣࡦࡤࡸࡦࠨ࠺ࠡࠩᕘ")
                    + json.dumps(str(bstack1ll111ll_opy_))
                    + bstack1l1l1_opy_ (u"ࠧࡢࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡾ࡞ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡽࠣᕙ")
                )
        except Exception as e:
            summary.append(bstack1l1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡦࡴ࡮ࡰࡶࡤࡸࡪࡀࠠࡼ࠲ࢀࠦᕚ").format(e))
def bstack1lllll1l111_opy_(test_name, error_message):
    try:
        bstack1llll11llll_opy_ = []
        bstack1l1lll111l_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡋࡑࡈࡊ࡞ࠧᕛ"), bstack1l1l1_opy_ (u"ࠨ࠲ࠪᕜ"))
        bstack1l1ll1l11l_opy_ = {bstack1l1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧᕝ"): test_name, bstack1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᕞ"): error_message, bstack1l1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪᕟ"): bstack1l1lll111l_opy_}
        bstack1lllll11l11_opy_ = os.path.join(tempfile.gettempdir(), bstack1l1l1_opy_ (u"ࠬࡶࡷࡠࡲࡼࡸࡪࡹࡴࡠࡧࡵࡶࡴࡸ࡟࡭࡫ࡶࡸ࠳ࡰࡳࡰࡰࠪᕠ"))
        if os.path.exists(bstack1lllll11l11_opy_):
            with open(bstack1lllll11l11_opy_) as f:
                bstack1llll11llll_opy_ = json.load(f)
        bstack1llll11llll_opy_.append(bstack1l1ll1l11l_opy_)
        with open(bstack1lllll11l11_opy_, bstack1l1l1_opy_ (u"࠭ࡷࠨᕡ")) as f:
            json.dump(bstack1llll11llll_opy_, f)
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡩࡷࡹࡩࡴࡶ࡬ࡲ࡬ࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡴࡾࡺࡥࡴࡶࠣࡩࡷࡸ࡯ࡳࡵ࠽ࠤࠬᕢ") + str(e))
def bstack1llll1lll11_opy_(item, report, summary, bstack1llll1l1111_opy_):
    if report.when in [bstack1l1l1_opy_ (u"ࠣࡵࡨࡸࡺࡶࠢᕣ"), bstack1l1l1_opy_ (u"ࠤࡷࡩࡦࡸࡤࡰࡹࡱࠦᕤ")]:
        return
    if (str(bstack1llll1l1111_opy_).lower() != bstack1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᕥ")):
        bstack1l1lllll1_opy_(item._page, report.nodeid)
    passed = report.passed or report.skipped or (report.failed and hasattr(report, bstack1l1l1_opy_ (u"ࠦࡼࡧࡳࡹࡨࡤ࡭ࡱࠨᕦ")))
    bstack1ll111ll_opy_ = bstack1l1l1_opy_ (u"ࠧࠨᕧ")
    bstack1111lll111_opy_(report)
    if not report.skipped:
        if not passed:
            try:
                bstack1ll111ll_opy_ = report.longrepr.reprcrash
            except Exception as e:
                summary.append(
                    bstack1l1l1_opy_ (u"ࠨࡗࡂࡔࡑࡍࡓࡍ࠺ࠡࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠࡧࡣ࡬ࡰࡺࡸࡥࠡࡴࡨࡥࡸࡵ࡮࠻ࠢࡾ࠴ࢂࠨᕨ").format(e)
                )
        try:
            if passed:
                bstack11l1l11l_opy_(getattr(item, bstack1l1l1_opy_ (u"ࠧࡠࡲࡤ࡫ࡪ࠭ᕩ"), None), bstack1l1l1_opy_ (u"ࠣࡲࡤࡷࡸ࡫ࡤࠣᕪ"))
            else:
                error_message = bstack1l1l1_opy_ (u"ࠩࠪᕫ")
                if bstack1ll111ll_opy_:
                    bstack1ll1l1l111_opy_(item._page, str(bstack1ll111ll_opy_), bstack1l1l1_opy_ (u"ࠥࡩࡷࡸ࡯ࡳࠤᕬ"))
                    bstack11l1l11l_opy_(getattr(item, bstack1l1l1_opy_ (u"ࠫࡤࡶࡡࡨࡧࠪᕭ"), None), bstack1l1l1_opy_ (u"ࠧ࡬ࡡࡪ࡮ࡨࡨࠧᕮ"), str(bstack1ll111ll_opy_))
                    error_message = str(bstack1ll111ll_opy_)
                else:
                    bstack11l1l11l_opy_(getattr(item, bstack1l1l1_opy_ (u"࠭࡟ࡱࡣࡪࡩࠬᕯ"), None), bstack1l1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢᕰ"))
                bstack1lllll1l111_opy_(report.nodeid, error_message)
        except Exception as e:
            summary.append(bstack1l1l1_opy_ (u"࡙ࠣࡄࡖࡓࡏࡎࡈ࠼ࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡵࡱࡦࡤࡸࡪࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡴࡶࡤࡸࡺࡹ࠺ࠡࡽ࠳ࢁࠧᕱ").format(e))
try:
    from typing import Generator
    import pytest_playwright.pytest_playwright as p
    @pytest.fixture
    def page(context: BrowserContext, request: pytest.FixtureRequest) -> Generator[Page, None, None]:
        page = context.new_page()
        request.node._page = page
        yield page
except:
    pass
def pytest_addoption(parser):
    parser.addoption(bstack1l1l1_opy_ (u"ࠤ࠰࠱ࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪࠨᕲ"), default=bstack1l1l1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤᕳ"), help=bstack1l1l1_opy_ (u"ࠦࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡩࠠࡴࡧࡷࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡴࡡ࡮ࡧࠥᕴ"))
    parser.addoption(bstack1l1l1_opy_ (u"ࠧ࠳࠭ࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠦᕵ"), default=bstack1l1l1_opy_ (u"ࠨࡆࡢ࡮ࡶࡩࠧᕶ"), help=bstack1l1l1_opy_ (u"ࠢࡂࡷࡷࡳࡲࡧࡴࡪࡥࠣࡷࡪࡺࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡰࡤࡱࡪࠨᕷ"))
    try:
        import pytest_selenium.pytest_selenium
    except:
        parser.addoption(bstack1l1l1_opy_ (u"ࠣ࠯࠰ࡨࡷ࡯ࡶࡦࡴࠥᕸ"), action=bstack1l1l1_opy_ (u"ࠤࡶࡸࡴࡸࡥࠣᕹ"), default=bstack1l1l1_opy_ (u"ࠥࡧ࡭ࡸ࡯࡮ࡧࠥᕺ"),
                         help=bstack1l1l1_opy_ (u"ࠦࡉࡸࡩࡷࡧࡵࠤࡹࡵࠠࡳࡷࡱࠤࡹ࡫ࡳࡵࡵࠥᕻ"))
def bstack1l111ll11l_opy_(log):
    if not (log[bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᕼ")] and log[bstack1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᕽ")].strip()):
        return
    active = bstack1l11l1l11l_opy_()
    log = {
        bstack1l1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᕾ"): log[bstack1l1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧᕿ")],
        bstack1l1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᖀ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠪ࡞ࠬᖁ"),
        bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖂ"): log[bstack1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖃ")],
    }
    if active:
        if active[bstack1l1l1_opy_ (u"࠭ࡴࡺࡲࡨࠫᖄ")] == bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࠬᖅ"):
            log[bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᖆ")] = active[bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖇ")]
        elif active[bstack1l1l1_opy_ (u"ࠪࡸࡾࡶࡥࠨᖈ")] == bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࠩᖉ"):
            log[bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᖊ")] = active[bstack1l1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᖋ")]
    bstack1ll1l1llll_opy_.bstack1l1111lll1_opy_([log])
def bstack1l11l1l11l_opy_():
    if len(store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡪࡲࡳࡰࡥࡵࡶ࡫ࡧࠫᖌ")]) > 0 and store[bstack1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡ࡫ࡳࡴࡱ࡟ࡶࡷ࡬ࡨࠬᖍ")][-1]:
        return {
            bstack1l1l1_opy_ (u"ࠩࡷࡽࡵ࡫ࠧᖎ"): bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࠨᖏ"),
            bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᖐ"): store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᖑ")][-1]
        }
    if store.get(bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᖒ"), None):
        return {
            bstack1l1l1_opy_ (u"ࠧࡵࡻࡳࡩࠬᖓ"): bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹ࠭ᖔ"),
            bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᖕ"): store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᖖ")]
        }
    return None
bstack1l11111ll1_opy_ = bstack1l1111l1l1_opy_(bstack1l111ll11l_opy_)
def pytest_runtest_call(item):
    try:
        global CONFIG
        global bstack1lllll1llll_opy_
        if bstack1lllll1llll_opy_:
            driver = getattr(item, bstack1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᖗ"), None)
            bstack111l1ll11_opy_ = bstack11llllll1_opy_.bstack1ll1l1lll_opy_(CONFIG, bstack11l1lll111_opy_(item.own_markers))
            item._a11y_started = bstack11llllll1_opy_.bstack1l11111ll_opy_(driver, bstack111l1ll11_opy_)
        if not bstack1ll1l1llll_opy_.on() or bstack1lllll1ll1l_opy_ != bstack1l1l1_opy_ (u"ࠬࡶࡹࡵࡧࡶࡸࠬᖘ"):
            return
        global current_test_uuid, bstack1l11111ll1_opy_
        bstack1l11111ll1_opy_.start()
        bstack1l11l1ll11_opy_ = {
            bstack1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᖙ"): uuid4().__str__(),
            bstack1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᖚ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠨ࡜ࠪᖛ")
        }
        current_test_uuid = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᖜ")]
        store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᖝ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᖞ")]
        threading.current_thread().current_test_uuid = current_test_uuid
        _1l111l111l_opy_[item.nodeid] = {**_1l111l111l_opy_[item.nodeid], **bstack1l11l1ll11_opy_}
        bstack1llll1ll11l_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭ᖟ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡸࡵ࡯ࡶࡨࡷࡹࡥࡣࡢ࡮࡯࠾ࠥࢁࡽࠨᖠ"), str(err))
def pytest_runtest_setup(item):
    global bstack1lllll111ll_opy_
    threading.current_thread().percySessionName = item.nodeid
    if bstack11ll1111ll_opy_():
        atexit.register(bstack111lll1ll_opy_)
        if not bstack1lllll111ll_opy_:
            bstack1lllll1ll11_opy_ = [signal.SIGINT, signal.SIGTERM, signal.SIGHUP, signal.SIGQUIT]
            for s in bstack1lllll1ll11_opy_:
                signal.signal(s, bstack1lllll11111_opy_)
            bstack1lllll111ll_opy_ = True
        try:
            item.config.hook.pytest_selenium_runtest_makereport = bstack1111l1lll1_opy_
        except Exception as err:
            threading.current_thread().testStatus = bstack1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᖡ")
    try:
        if not bstack1ll1l1llll_opy_.on():
            return
        bstack1l11111ll1_opy_.start()
        uuid = uuid4().__str__()
        bstack1l11l1ll11_opy_ = {
            bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖢ"): uuid,
            bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖣ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠪ࡞ࠬᖤ"),
            bstack1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᖥ"): bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᖦ"),
            bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᖧ"): bstack1l1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖨ"),
            bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᖩ"): bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᖪ")
        }
        threading.current_thread().current_hook_uuid = uuid
        store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡ࡬ࡸࡪࡳࠧᖫ")] = item
        store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤ࡮࡯ࡰ࡭ࡢࡹࡺ࡯ࡤࠨᖬ")] = [uuid]
        if not _1l111l111l_opy_.get(item.nodeid, None):
            _1l111l111l_opy_[item.nodeid] = {bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᖭ"): [], bstack1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᖮ"): []}
        _1l111l111l_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᖯ")].append(bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖰ")])
        _1l111l111l_opy_[item.nodeid + bstack1l1l1_opy_ (u"ࠩ࠰ࡷࡪࡺࡵࡱࠩᖱ")] = bstack1l11l1ll11_opy_
        bstack1lllll1l1ll_opy_(item, bstack1l11l1ll11_opy_, bstack1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᖲ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡶࡺࡴࡴࡦࡵࡷࡣࡸ࡫ࡴࡶࡲ࠽ࠤࢀࢃࠧᖳ"), str(err))
def pytest_runtest_teardown(item):
    try:
        global bstack1l1ll11lll_opy_
        if CONFIG.get(bstack1l1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫᖴ"), False):
            if CONFIG.get(bstack1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡈࡧࡰࡵࡷࡵࡩࡒࡵࡤࡦࠩᖵ"), bstack1l1l1_opy_ (u"ࠢࡢࡷࡷࡳࠧᖶ")) == bstack1l1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥᖷ"):
                bstack1lllll11l1l_opy_ = bstack1lllll11l_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬᖸ"), None)
                bstack1l1l111l1_opy_ = bstack1lllll11l1l_opy_ + bstack1l1l1_opy_ (u"ࠥ࠱ࡹ࡫ࡳࡵࡥࡤࡷࡪࠨᖹ")
                driver = getattr(item, bstack1l1l1_opy_ (u"ࠫࡤࡪࡲࡪࡸࡨࡶࠬᖺ"), None)
                PercySDK.screenshot(driver, bstack1l1l111l1_opy_)
        if getattr(item, bstack1l1l1_opy_ (u"ࠬࡥࡡ࠲࠳ࡼࡣࡸࡺࡡࡳࡶࡨࡨࠬᖻ"), False):
            logger.info(bstack1l1l1_opy_ (u"ࠨࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠤࡕࡸ࡯ࡤࡧࡶࡷ࡮ࡴࡧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡩࡴࠢࡸࡲࡩ࡫ࡲࡸࡣࡼ࠲ࠥࠨᖼ"))
            driver = getattr(item, bstack1l1l1_opy_ (u"ࠧࡠࡦࡵ࡭ࡻ࡫ࡲࠨᖽ"), None)
            bstack11lll1ll11_opy_ = item.cls.__name__ if not item.cls is None else None
            bstack11llllll1_opy_.bstack11l111l11_opy_(driver, bstack11lll1ll11_opy_, item.name, item.module.__name__, item.path, bstack1l1ll11lll_opy_)
        if not bstack1ll1l1llll_opy_.on():
            return
        bstack1l11l1ll11_opy_ = {
            bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ࠭ᖾ"): uuid4().__str__(),
            bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᖿ"): datetime.datetime.utcnow().isoformat() + bstack1l1l1_opy_ (u"ࠪ࡞ࠬᗀ"),
            bstack1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᗁ"): bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᗂ"),
            bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡹࡿࡰࡦࠩᗃ"): bstack1l1l1_opy_ (u"ࠧࡂࡈࡗࡉࡗࡥࡅࡂࡅࡋࠫᗄ"),
            bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᗅ"): bstack1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࠫᗆ")
        }
        _1l111l111l_opy_[item.nodeid + bstack1l1l1_opy_ (u"ࠪ࠱ࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᗇ")] = bstack1l11l1ll11_opy_
        bstack1lllll1l1ll_opy_(item, bstack1l11l1ll11_opy_, bstack1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᗈ"))
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡵࡿࡴࡦࡵࡷࡣࡷࡻ࡮ࡵࡧࡶࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࠺ࠡࡽࢀࠫᗉ"), str(err))
@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    if not bstack1ll1l1llll_opy_.on():
        yield
        return
    start_time = datetime.datetime.now()
    if bstack1111ll1ll1_opy_(fixturedef.argname):
        store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡪࡶࡨࡱࠬᗊ")] = request.node
    elif bstack1111ll11l1_opy_(fixturedef.argname):
        store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡥ࡯ࡥࡸࡹ࡟ࡪࡶࡨࡱࠬᗋ")] = request.node
    outcome = yield
    try:
        fixture = {
            bstack1l1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᗌ"): fixturedef.argname,
            bstack1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᗍ"): bstack11ll111ll1_opy_(outcome),
            bstack1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࠬᗎ"): (datetime.datetime.now() - start_time).total_seconds() * 1000
        }
        bstack1llll1ll1l1_opy_ = store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡺࡥࡴࡶࡢ࡭ࡹ࡫࡭ࠨᗏ")]
        if not _1l111l111l_opy_.get(bstack1llll1ll1l1_opy_.nodeid, None):
            _1l111l111l_opy_[bstack1llll1ll1l1_opy_.nodeid] = {bstack1l1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᗐ"): []}
        _1l111l111l_opy_[bstack1llll1ll1l1_opy_.nodeid][bstack1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᗑ")].append(fixture)
    except Exception as err:
        logger.debug(bstack1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰࡺࡶࡨࡷࡹࡥࡦࡪࡺࡷࡹࡷ࡫࡟ࡴࡧࡷࡹࡵࡀࠠࡼࡿࠪᗒ"), str(err))
if bstack1l1l1ll1ll_opy_() and bstack1ll1l1llll_opy_.on():
    def pytest_bdd_before_step(request, step):
        try:
            _1l111l111l_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᗓ")].bstack11111l1l11_opy_(id(step))
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲ࠽ࠤࢀࢃࠧᗔ"), str(err))
    def pytest_bdd_step_error(request, step, exception):
        try:
            _1l111l111l_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡦࡤࡸࡦ࠭ᗕ")].bstack1l11l1llll_opy_(id(step), Result.failed(exception=exception))
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡴࡶࡨࡴࡤ࡫ࡲࡳࡱࡵ࠾ࠥࢁࡽࠨᗖ"), str(err))
    def pytest_bdd_after_step(request, step):
        try:
            bstack1l1111l1ll_opy_: bstack1l11lllll1_opy_ = _1l111l111l_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡨࡦࡺࡡࠨᗗ")]
            bstack1l1111l1ll_opy_.bstack1l11l1llll_opy_(id(step), Result.passed())
        except Exception as err:
            print(bstack1l1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡶࡹࡵࡧࡶࡸࡤࡨࡤࡥࡡࡶࡸࡪࡶ࡟ࡦࡴࡵࡳࡷࡀࠠࡼࡿࠪᗘ"), str(err))
    def pytest_bdd_before_scenario(request, feature, scenario):
        global bstack1lllll1ll1l_opy_
        try:
            if not bstack1ll1l1llll_opy_.on() or bstack1lllll1ll1l_opy_ != bstack1l1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠫᗙ"):
                return
            global bstack1l11111ll1_opy_
            bstack1l11111ll1_opy_.start()
            if not _1l111l111l_opy_.get(request.node.nodeid, None):
                _1l111l111l_opy_[request.node.nodeid] = {}
            bstack1l1111l1ll_opy_ = bstack1l11lllll1_opy_.bstack111111l11l_opy_(
                scenario, feature, request.node,
                name=bstack1111l1ll1l_opy_(request.node, scenario),
                bstack1l111l1lll_opy_=bstack1l11lllll_opy_(),
                file_path=feature.filename,
                scope=[feature.name],
                framework=bstack1l1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᗚ"),
                tags=bstack1111ll1l1l_opy_(feature, scenario)
            )
            _1l111l111l_opy_[request.node.nodeid][bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᗛ")] = bstack1l1111l1ll_opy_
            bstack1lllll1lll1_opy_(bstack1l1111l1ll_opy_.uuid)
            bstack1ll1l1llll_opy_.bstack1l11l11111_opy_(bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᗜ"), bstack1l1111l1ll_opy_)
        except Exception as err:
            print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶࡢࡦࡩࡪ࡟ࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰ࠼ࠣࡿࢂ࠭ᗝ"), str(err))
def bstack1llll1l11l1_opy_(bstack1lllll1111l_opy_):
    if bstack1lllll1111l_opy_ in store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᗞ")]:
        store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡩࡱࡲ࡯ࡤࡻࡵࡪࡦࠪᗟ")].remove(bstack1lllll1111l_opy_)
def bstack1lllll1lll1_opy_(bstack1llll1l1l1l_opy_):
    store[bstack1l1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫᗠ")] = bstack1llll1l1l1l_opy_
    threading.current_thread().current_test_uuid = bstack1llll1l1l1l_opy_
@bstack1ll1l1llll_opy_.bstack1111111l11_opy_
def bstack1llll1l1l11_opy_(item, call, report):
    global bstack1lllll1ll1l_opy_
    try:
        if report.when == bstack1l1l1_opy_ (u"ࠨࡥࡤࡰࡱ࠭ᗡ"):
            bstack1l11111ll1_opy_.reset()
        if report.when == bstack1l1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧᗢ"):
            if bstack1lllll1ll1l_opy_ == bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᗣ"):
                _1l111l111l_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᗤ")] = bstack11l1ll1l11_opy_(report.stop)
                bstack1llll1ll11l_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᗥ"), report, call)
                store[bstack1l1l1_opy_ (u"࠭ࡣࡶࡴࡵࡩࡳࡺ࡟ࡵࡧࡶࡸࡤࡻࡵࡪࡦࠪᗦ")] = None
            elif bstack1lllll1ll1l_opy_ == bstack1l1l1_opy_ (u"ࠢࡱࡻࡷࡩࡸࡺ࠭ࡣࡦࡧࠦᗧ"):
                bstack1l1111l1ll_opy_ = _1l111l111l_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᗨ")]
                bstack1l1111l1ll_opy_.set(hooks=_1l111l111l_opy_[item.nodeid].get(bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࡳࠨᗩ"), []))
                exception, bstack1l11ll1ll1_opy_ = None, None
                if call.excinfo:
                    exception = call.excinfo.value
                    bstack1l11ll1ll1_opy_ = [call.excinfo.exconly(), report.longreprtext]
                bstack1l1111l1ll_opy_.stop(time=bstack11l1ll1l11_opy_(report.stop), result=Result(result=report.outcome, exception=exception, bstack1l11ll1ll1_opy_=bstack1l11ll1ll1_opy_))
                bstack1ll1l1llll_opy_.bstack1l11l11111_opy_(bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᗪ"), _1l111l111l_opy_[item.nodeid][bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡧࡥࡹࡧࠧᗫ")])
        elif report.when in [bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᗬ"), bstack1l1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮ࠨᗭ")]:
            bstack1l11ll1l1l_opy_ = item.nodeid + bstack1l1l1_opy_ (u"ࠧ࠮ࠩᗮ") + report.when
            if report.skipped:
                hook_type = bstack1l1l1_opy_ (u"ࠨࡄࡈࡊࡔࡘࡅࡠࡇࡄࡇࡍ࠭ᗯ") if report.when == bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨᗰ") else bstack1l1l1_opy_ (u"ࠪࡅࡋ࡚ࡅࡓࡡࡈࡅࡈࡎࠧᗱ")
                _1l111l111l_opy_[bstack1l11ll1l1l_opy_] = {
                    bstack1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᗲ"): uuid4().__str__(),
                    bstack1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᗳ"): datetime.datetime.utcfromtimestamp(report.start).isoformat() + bstack1l1l1_opy_ (u"࡚࠭ࠨᗴ"),
                    bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᗵ"): hook_type
                }
            _1l111l111l_opy_[bstack1l11ll1l1l_opy_][bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᗶ")] = datetime.datetime.utcfromtimestamp(report.stop).isoformat() + bstack1l1l1_opy_ (u"ࠩ࡝ࠫᗷ")
            bstack1llll1l11l1_opy_(_1l111l111l_opy_[bstack1l11ll1l1l_opy_][bstack1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᗸ")])
            bstack1lllll1l1ll_opy_(item, _1l111l111l_opy_[bstack1l11ll1l1l_opy_], bstack1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᗹ"), report, call)
            if report.when == bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᗺ"):
                if report.outcome == bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᗻ"):
                    bstack1l11l1ll11_opy_ = {
                        bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᗼ"): uuid4().__str__(),
                        bstack1l1l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬᗽ"): bstack1l11lllll_opy_(),
                        bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᗾ"): bstack1l11lllll_opy_()
                    }
                    _1l111l111l_opy_[item.nodeid] = {**_1l111l111l_opy_[item.nodeid], **bstack1l11l1ll11_opy_}
                    bstack1llll1ll11l_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫᗿ"))
                    bstack1llll1ll11l_opy_(item, _1l111l111l_opy_[item.nodeid], bstack1l1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭ᘀ"), report, call)
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡭ࡧ࡮ࡥ࡮ࡨࡣࡴ࠷࠱ࡺࡡࡷࡩࡸࡺ࡟ࡦࡸࡨࡲࡹࡀࠠࡼࡿࠪᘁ"), str(err))
def bstack1lllll111l1_opy_(test, bstack1l11l1ll11_opy_, result=None, call=None, bstack1l1l11ll1l_opy_=None, outcome=None):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    bstack1l1111l1ll_opy_ = {
        bstack1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᘂ"): bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘃ")],
        bstack1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᘄ"): bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺࠧᘅ"),
        bstack1l1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᘆ"): test.name,
        bstack1l1l1_opy_ (u"ࠫࡧࡵࡤࡺࠩᘇ"): {
            bstack1l1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࠪᘈ"): bstack1l1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᘉ"),
            bstack1l1l1_opy_ (u"ࠧࡤࡱࡧࡩࠬᘊ"): inspect.getsource(test.obj)
        },
        bstack1l1l1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᘋ"): test.name,
        bstack1l1l1_opy_ (u"ࠩࡶࡧࡴࡶࡥࠨᘌ"): test.name,
        bstack1l1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᘍ"): bstack1ll1l1llll_opy_.bstack1l11ll111l_opy_(test),
        bstack1l1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧᘎ"): file_path,
        bstack1l1l1_opy_ (u"ࠬࡲ࡯ࡤࡣࡷ࡭ࡴࡴࠧᘏ"): file_path,
        bstack1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᘐ"): bstack1l1l1_opy_ (u"ࠧࡱࡧࡱࡨ࡮ࡴࡧࠨᘑ"),
        bstack1l1l1_opy_ (u"ࠨࡸࡦࡣ࡫࡯࡬ࡦࡲࡤࡸ࡭࠭ᘒ"): file_path,
        bstack1l1l1_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭ᘓ"): bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧᘔ")],
        bstack1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᘕ"): bstack1l1l1_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬᘖ"),
        bstack1l1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡘࡥࡳࡷࡱࡔࡦࡸࡡ࡮ࠩᘗ"): {
            bstack1l1l1_opy_ (u"ࠧࡳࡧࡵࡹࡳࡥ࡮ࡢ࡯ࡨࠫᘘ"): test.nodeid
        },
        bstack1l1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ᘙ"): bstack11l1lll111_opy_(test.own_markers)
    }
    if bstack1l1l11ll1l_opy_ in [bstack1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᘚ"), bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᘛ")]:
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠫࡲ࡫ࡴࡢࠩᘜ")] = {
            bstack1l1l1_opy_ (u"ࠬ࡬ࡩࡹࡶࡸࡶࡪࡹࠧᘝ"): bstack1l11l1ll11_opy_.get(bstack1l1l1_opy_ (u"࠭ࡦࡪࡺࡷࡹࡷ࡫ࡳࠨᘞ"), [])
        }
    if bstack1l1l11ll1l_opy_ == bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔ࡭࡬ࡴࡵ࡫ࡤࠨᘟ"):
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘠ")] = bstack1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᘡ")
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡴࠩᘢ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡵࠪᘣ")]
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᘤ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘥ")]
    if result:
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘦ")] = result.outcome
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࡢ࡭ࡳࡥ࡭ࡴࠩᘧ")] = result.duration * 1000
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᘨ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘩ")]
        if result.failed:
            bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᘪ")] = bstack1ll1l1llll_opy_.bstack11llll1ll1_opy_(call.excinfo.typename)
            bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᘫ")] = bstack1ll1l1llll_opy_.bstack1llllllll11_opy_(call.excinfo, result)
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᘬ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᘭ")]
    if outcome:
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘮ")] = bstack11ll111ll1_opy_(outcome)
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠩࡧࡹࡷࡧࡴࡪࡱࡱࡣ࡮ࡴ࡟࡮ࡵࠪᘯ")] = 0
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᘰ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘱ")]
        if bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᘲ")] == bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᘳ"):
            bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡺࡸࡥࡠࡶࡼࡴࡪ࠭ᘴ")] = bstack1l1l1_opy_ (u"ࠨࡗࡱ࡬ࡦࡴࡤ࡭ࡧࡧࡉࡷࡸ࡯ࡳࠩᘵ")  # bstack1llll1lllll_opy_
            bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡵࡳࡧࠪᘶ")] = [{bstack1l1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᘷ"): [bstack1l1l1_opy_ (u"ࠫࡸࡵ࡭ࡦࠢࡨࡶࡷࡵࡲࠨᘸ")]}]
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡶࠫᘹ")] = bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡷࠬᘺ")]
    return bstack1l1111l1ll_opy_
def bstack1llll1l111l_opy_(test, bstack1l11ll1111_opy_, bstack1l1l11ll1l_opy_, result, call, outcome, bstack1llll1ll1ll_opy_):
    file_path = os.path.relpath(test.fspath.strpath, start=os.getcwd())
    hook_type = bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡺࡹࡱࡧࠪᘻ")]
    hook_name = bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥ࡮ࡢ࡯ࡨࠫᘼ")]
    hook_data = {
        bstack1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᘽ"): bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᘾ")],
        bstack1l1l1_opy_ (u"ࠫࡹࡿࡰࡦࠩᘿ"): bstack1l1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࠪᙀ"),
        bstack1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᙁ"): bstack1l1l1_opy_ (u"ࠧࡼࡿࠪᙂ").format(bstack1111l1llll_opy_(hook_name)),
        bstack1l1l1_opy_ (u"ࠨࡤࡲࡨࡾ࠭ᙃ"): {
            bstack1l1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࠧᙄ"): bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᙅ"),
            bstack1l1l1_opy_ (u"ࠫࡨࡵࡤࡦࠩᙆ"): None
        },
        bstack1l1l1_opy_ (u"ࠬࡹࡣࡰࡲࡨࠫᙇ"): test.name,
        bstack1l1l1_opy_ (u"࠭ࡳࡤࡱࡳࡩࡸ࠭ᙈ"): bstack1ll1l1llll_opy_.bstack1l11ll111l_opy_(test, hook_name),
        bstack1l1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪᙉ"): file_path,
        bstack1l1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࠪᙊ"): file_path,
        bstack1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙋ"): bstack1l1l1_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫᙌ"),
        bstack1l1l1_opy_ (u"ࠫࡻࡩ࡟ࡧ࡫࡯ࡩࡵࡧࡴࡩࠩᙍ"): file_path,
        bstack1l1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩᙎ"): bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᙏ")],
        bstack1l1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᙐ"): bstack1l1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴ࠮ࡥࡸࡧࡺࡳࡢࡦࡴࠪᙑ") if bstack1lllll1ll1l_opy_ == bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩ࠭ᙒ") else bstack1l1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪᙓ"),
        bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡷࡽࡵ࡫ࠧᙔ"): hook_type
    }
    bstack1lllll11lll_opy_ = bstack1l1l1111ll_opy_(_1l111l111l_opy_.get(test.nodeid, None))
    if bstack1lllll11lll_opy_:
        hook_data[bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡪࡦࠪᙕ")] = bstack1lllll11lll_opy_
    if result:
        hook_data[bstack1l1l1_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭ᙖ")] = result.outcome
        hook_data[bstack1l1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᙗ")] = result.duration * 1000
        hook_data[bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙘ")] = bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧᙙ")]
        if result.failed:
            hook_data[bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᙚ")] = bstack1ll1l1llll_opy_.bstack11llll1ll1_opy_(call.excinfo.typename)
            hook_data[bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᙛ")] = bstack1ll1l1llll_opy_.bstack1llllllll11_opy_(call.excinfo, result)
    if outcome:
        hook_data[bstack1l1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬᙜ")] = bstack11ll111ll1_opy_(outcome)
        hook_data[bstack1l1l1_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࡠ࡫ࡱࡣࡲࡹࠧᙝ")] = 100
        hook_data[bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙞ")] = bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭ᙟ")]
        if hook_data[bstack1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙠ")] == bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᙡ"):
            hook_data[bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᙢ")] = bstack1l1l1_opy_ (u"࡛ࠬ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷ࠭ᙣ")  # bstack1llll1lllll_opy_
            hook_data[bstack1l1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡹࡷ࡫ࠧᙤ")] = [{bstack1l1l1_opy_ (u"ࠧࡣࡣࡦ࡯ࡹࡸࡡࡤࡧࠪᙥ"): [bstack1l1l1_opy_ (u"ࠨࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠬᙦ")]}]
    if bstack1llll1ll1ll_opy_:
        hook_data[bstack1l1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᙧ")] = bstack1llll1ll1ll_opy_.result
        hook_data[bstack1l1l1_opy_ (u"ࠪࡨࡺࡸࡡࡵ࡫ࡲࡲࡤ࡯࡮ࡠ࡯ࡶࠫᙨ")] = bstack11ll111lll_opy_(bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨᙩ")], bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙪ")])
        hook_data[bstack1l1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᙫ")] = bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸࠬᙬ")]
        if hook_data[bstack1l1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ᙭")] == bstack1l1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩ᙮"):
            hook_data[bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡶࡴࡨࡣࡹࡿࡰࡦࠩᙯ")] = bstack1ll1l1llll_opy_.bstack11llll1ll1_opy_(bstack1llll1ll1ll_opy_.exception_type)
            hook_data[bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࠬᙰ")] = [{bstack1l1l1_opy_ (u"ࠬࡨࡡࡤ࡭ࡷࡶࡦࡩࡥࠨᙱ"): bstack11l11llll1_opy_(bstack1llll1ll1ll_opy_.exception)}]
    return hook_data
def bstack1llll1ll11l_opy_(test, bstack1l11l1ll11_opy_, bstack1l1l11ll1l_opy_, result=None, call=None, outcome=None):
    bstack1l1111l1ll_opy_ = bstack1lllll111l1_opy_(test, bstack1l11l1ll11_opy_, result, call, bstack1l1l11ll1l_opy_, outcome)
    driver = getattr(test, bstack1l1l1_opy_ (u"࠭࡟ࡥࡴ࡬ࡺࡪࡸࠧᙲ"), None)
    if bstack1l1l11ll1l_opy_ == bstack1l1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨᙳ") and driver:
        bstack1l1111l1ll_opy_[bstack1l1l1_opy_ (u"ࠨ࡫ࡱࡸࡪ࡭ࡲࡢࡶ࡬ࡳࡳࡹࠧᙴ")] = bstack1ll1l1llll_opy_.bstack1l1111llll_opy_(driver)
    if bstack1l1l11ll1l_opy_ == bstack1l1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖ࡯࡮ࡶࡰࡦࡦࠪᙵ"):
        bstack1l1l11ll1l_opy_ = bstack1l1l1_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬᙶ")
    bstack1l11111lll_opy_ = {
        bstack1l1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᙷ"): bstack1l1l11ll1l_opy_,
        bstack1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᙸ"): bstack1l1111l1ll_opy_
    }
    bstack1ll1l1llll_opy_.bstack1l111ll1l1_opy_(bstack1l11111lll_opy_)
def bstack1lllll1l1ll_opy_(test, bstack1l11l1ll11_opy_, bstack1l1l11ll1l_opy_, result=None, call=None, outcome=None, bstack1llll1ll1ll_opy_=None):
    hook_data = bstack1llll1l111l_opy_(test, bstack1l11l1ll11_opy_, bstack1l1l11ll1l_opy_, result, call, outcome, bstack1llll1ll1ll_opy_)
    bstack1l11111lll_opy_ = {
        bstack1l1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪᙹ"): bstack1l1l11ll1l_opy_,
        bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᙺ"): hook_data
    }
    bstack1ll1l1llll_opy_.bstack1l111ll1l1_opy_(bstack1l11111lll_opy_)
def bstack1l1l1111ll_opy_(bstack1l11l1ll11_opy_):
    if not bstack1l11l1ll11_opy_:
        return None
    if bstack1l11l1ll11_opy_.get(bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡤࡢࡶࡤࠫᙻ"), None):
        return getattr(bstack1l11l1ll11_opy_[bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡥࡣࡷࡥࠬᙼ")], bstack1l1l1_opy_ (u"ࠪࡹࡺ࡯ࡤࠨᙽ"), None)
    return bstack1l11l1ll11_opy_.get(bstack1l1l1_opy_ (u"ࠫࡺࡻࡩࡥࠩᙾ"), None)
@pytest.fixture(autouse=True)
def second_fixture(caplog, request):
    yield
    try:
        if not bstack1ll1l1llll_opy_.on():
            return
        places = [bstack1l1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࠫᙿ"), bstack1l1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫ "), bstack1l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࠩᚁ")]
        bstack1l1l11111l_opy_ = []
        for bstack1llll1ll111_opy_ in places:
            records = caplog.get_records(bstack1llll1ll111_opy_)
            bstack1llll1l1ll1_opy_ = bstack1l1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᚂ") if bstack1llll1ll111_opy_ == bstack1l1l1_opy_ (u"ࠩࡦࡥࡱࡲࠧᚃ") else bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᚄ")
            bstack1llll1lll1l_opy_ = request.node.nodeid + (bstack1l1l1_opy_ (u"ࠫࠬᚅ") if bstack1llll1ll111_opy_ == bstack1l1l1_opy_ (u"ࠬࡩࡡ࡭࡮ࠪᚆ") else bstack1l1l1_opy_ (u"࠭࠭ࠨᚇ") + bstack1llll1ll111_opy_)
            bstack1llll1l1l1l_opy_ = bstack1l1l1111ll_opy_(_1l111l111l_opy_.get(bstack1llll1lll1l_opy_, None))
            if not bstack1llll1l1l1l_opy_:
                continue
            for record in records:
                if bstack11ll111l11_opy_(record.message):
                    continue
                bstack1l1l11111l_opy_.append({
                    bstack1l1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᚈ"): datetime.datetime.utcfromtimestamp(record.created).isoformat() + bstack1l1l1_opy_ (u"ࠨ࡜ࠪᚉ"),
                    bstack1l1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨᚊ"): record.levelname,
                    bstack1l1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᚋ"): record.message,
                    bstack1llll1l1ll1_opy_: bstack1llll1l1l1l_opy_
                })
        if len(bstack1l1l11111l_opy_) > 0:
            bstack1ll1l1llll_opy_.bstack1l1111lll1_opy_(bstack1l1l11111l_opy_)
    except Exception as err:
        print(bstack1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡪࡩ࡯࡯ࡦࡢࡪ࡮ࡾࡴࡶࡴࡨ࠾ࠥࢁࡽࠨᚌ"), str(err))
def bstack111l111ll_opy_(sequence, driver_command, response=None):
    if sequence == bstack1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᚍ"):
        if driver_command == bstack1l1l1_opy_ (u"࠭ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠪᚎ"):
            bstack1ll1l1llll_opy_.bstack1ll11111l1_opy_({
                bstack1l1l1_opy_ (u"ࠧࡪ࡯ࡤ࡫ࡪ࠭ᚏ"): response[bstack1l1l1_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧᚐ")],
                bstack1l1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᚑ"): store[bstack1l1l1_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧᚒ")]
            })
def bstack111lll1ll_opy_():
    global bstack1l1l11ll11_opy_
    bstack1ll1l1llll_opy_.bstack1l11l1l111_opy_()
    for driver in bstack1l1l11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1lllll11111_opy_(*args):
    global bstack1l1l11ll11_opy_
    bstack1ll1l1llll_opy_.bstack1l11l1l111_opy_()
    for driver in bstack1l1l11ll11_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1ll1lll1_opy_(self, *args, **kwargs):
    bstack1l11111l1_opy_ = bstack111l1l1l_opy_(self, *args, **kwargs)
    bstack1ll1l1llll_opy_.bstack111l111l_opy_(self)
    return bstack1l11111l1_opy_
def bstack11111ll1_opy_(framework_name):
    global bstack1lll111ll_opy_
    global bstack1111l1lll_opy_
    bstack1lll111ll_opy_ = framework_name
    logger.info(bstack1ll1llll1_opy_.format(bstack1lll111ll_opy_.split(bstack1l1l1_opy_ (u"ࠫ࠲࠭ᚓ"))[0]))
    try:
        from selenium import webdriver
        from selenium.webdriver.common.service import Service
        from selenium.webdriver.remote.webdriver import WebDriver
        if bstack11l1l1111l_opy_():
            Service.start = bstack1lll11l11l_opy_
            Service.stop = bstack1l111l1ll_opy_
            webdriver.Remote.__init__ = bstack1l1l1l1111_opy_
            webdriver.Remote.get = bstack11111ll11_opy_
            if not isinstance(os.getenv(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕ࡟ࡔࡆࡕࡗࡣࡕࡇࡒࡂࡎࡏࡉࡑ࠭ᚔ")), str):
                return
            WebDriver.close = bstack1l1lll111_opy_
            WebDriver.quit = bstack111ll11l_opy_
            WebDriver.getAccessibilityResults = getAccessibilityResults
            WebDriver.bstack1l1l1llll1_opy_ = getAccessibilityResults
            WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
            WebDriver.bstack1l111ll1l_opy_ = getAccessibilityResultsSummary
        if not bstack11l1l1111l_opy_() and bstack1ll1l1llll_opy_.on():
            webdriver.Remote.__init__ = bstack1ll1lll1_opy_
        bstack1111l1lll_opy_ = True
    except Exception as e:
        pass
    bstack1lll1lll1_opy_()
    if os.environ.get(bstack1l1l1_opy_ (u"࠭ࡓࡆࡎࡈࡒࡎ࡛ࡍࡠࡑࡕࡣࡕࡒࡁ࡚࡙ࡕࡍࡌࡎࡔࡠࡋࡑࡗ࡙ࡇࡌࡍࡇࡇࠫᚕ")):
        bstack1111l1lll_opy_ = eval(os.environ.get(bstack1l1l1_opy_ (u"ࠧࡔࡇࡏࡉࡓࡏࡕࡎࡡࡒࡖࡤࡖࡌࡂ࡛࡚ࡖࡎࡍࡈࡕࡡࡌࡒࡘ࡚ࡁࡍࡎࡈࡈࠬᚖ")))
    if not bstack1111l1lll_opy_:
        bstack1l11ll1l_opy_(bstack1l1l1_opy_ (u"ࠣࡒࡤࡧࡰࡧࡧࡦࡵࠣࡲࡴࡺࠠࡪࡰࡶࡸࡦࡲ࡬ࡦࡦࠥᚗ"), bstack1ll1ll11ll_opy_)
    if bstack1lll11l111_opy_():
        try:
            from selenium.webdriver.remote.remote_connection import RemoteConnection
            RemoteConnection._get_proxy_url = bstack1l1l1lll_opy_
        except Exception as e:
            logger.error(bstack1l111111l_opy_.format(str(e)))
    if bstack1l1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩᚘ") in str(framework_name).lower():
        if not bstack11l1l1111l_opy_():
            return
        try:
            from pytest_selenium import pytest_selenium
            from _pytest.config import Config
            pytest_selenium.pytest_report_header = bstack1lll1l1l_opy_
            from pytest_selenium.drivers import browserstack
            browserstack.pytest_selenium_runtest_makereport = bstack1ll1ll1ll1_opy_
            Config.getoption = bstack1111ll1ll_opy_
        except Exception as e:
            pass
        try:
            from pytest_bdd import reporting
            reporting.runtest_makereport = bstack1lll1lll11_opy_
        except Exception as e:
            pass
def bstack111ll11l_opy_(self):
    global bstack1lll111ll_opy_
    global bstack1ll1ll1111_opy_
    global bstack11l1l1l1_opy_
    try:
        if bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪᚙ") in bstack1lll111ll_opy_ and self.session_id != None and bstack1lllll11l_opy_(threading.current_thread(), bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡕࡷࡥࡹࡻࡳࠨᚚ"), bstack1l1l1_opy_ (u"ࠬ࠭᚛")) != bstack1l1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧ᚜"):
            bstack111l11l11_opy_ = bstack1l1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᚝") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1l1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨ᚞")
            bstack1llll1111_opy_(logger, True)
            if self != None:
                bstack11ll11ll_opy_(self, bstack111l11l11_opy_, bstack1l1l1_opy_ (u"ࠩ࠯ࠤࠬ᚟").join(threading.current_thread().bstackTestErrorMessages))
        threading.current_thread().testStatus = bstack1l1l1_opy_ (u"ࠪࠫᚠ")
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࠧᚡ") + str(e))
    bstack11l1l1l1_opy_(self)
    self.session_id = None
def bstack1l1l1l1111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
    global CONFIG
    global bstack1ll1ll1111_opy_
    global bstack1ll1lll111_opy_
    global bstack1l1111l1l_opy_
    global bstack1lll111ll_opy_
    global bstack111l1l1l_opy_
    global bstack1l1l11ll11_opy_
    global bstack11l1ll11_opy_
    global bstack1lll1111_opy_
    global bstack1lllll1llll_opy_
    global bstack1l1ll11lll_opy_
    CONFIG[bstack1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧᚢ")] = str(bstack1lll111ll_opy_) + str(__version__)
    command_executor = bstack1l111l111_opy_(bstack11l1ll11_opy_)
    logger.debug(bstack1ll11llll_opy_.format(command_executor))
    proxy = bstack1lll111l1l_opy_(CONFIG, proxy)
    bstack1l1lll111l_opy_ = 0
    try:
        if bstack1l1111l1l_opy_ is True:
            bstack1l1lll111l_opy_ = int(os.environ.get(bstack1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡖࡌࡂࡖࡉࡓࡗࡓ࡟ࡊࡐࡇࡉ࡝࠭ᚣ")))
    except:
        bstack1l1lll111l_opy_ = 0
    bstack111l11111_opy_ = bstack1lll1l1l1_opy_(CONFIG, bstack1l1lll111l_opy_)
    logger.debug(bstack1l1llll111_opy_.format(str(bstack111l11111_opy_)))
    bstack1l1ll11lll_opy_ = CONFIG.get(bstack1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᚤ"))[bstack1l1lll111l_opy_]
    if bstack1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬᚥ") in CONFIG and CONFIG[bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ᚦ")]:
        bstack1ll111l111_opy_(bstack111l11111_opy_, bstack1lll1111_opy_)
    if desired_capabilities:
        bstack1l1ll1ll11_opy_ = bstack1lllllll1l_opy_(desired_capabilities)
        bstack1l1ll1ll11_opy_[bstack1l1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪᚧ")] = bstack111llll1l_opy_(CONFIG)
        bstack11l1l1111_opy_ = bstack1lll1l1l1_opy_(bstack1l1ll1ll11_opy_)
        if bstack11l1l1111_opy_:
            bstack111l11111_opy_ = update(bstack11l1l1111_opy_, bstack111l11111_opy_)
        desired_capabilities = None
    if options:
        bstack1ll111l1ll_opy_(options, bstack111l11111_opy_)
    if not options:
        options = bstack1l1l1ll1l1_opy_(bstack111l11111_opy_)
    if bstack11llllll1_opy_.bstack11l1ll1ll_opy_(CONFIG, bstack1l1lll111l_opy_) and bstack11llllll1_opy_.bstack11l11l1l1_opy_(bstack111l11111_opy_, options):
        bstack1lllll1llll_opy_ = True
        bstack11llllll1_opy_.set_capabilities(bstack111l11111_opy_, CONFIG)
    if proxy and bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫᚨ")):
        options.proxy(proxy)
    if options and bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫᚩ")):
        desired_capabilities = None
    if (
            not options and not desired_capabilities
    ) or (
            bstack1ll111l11l_opy_() < version.parse(bstack1l1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬᚪ")) and not desired_capabilities
    ):
        desired_capabilities = {}
        desired_capabilities.update(bstack111l11111_opy_)
    logger.info(bstack111llllll_opy_)
    if bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧᚫ")):
        bstack111l1l1l_opy_(self, command_executor=command_executor,
                  options=options, keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧᚬ")):
        bstack111l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities, options=options,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    elif bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩᚭ")):
        bstack111l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive, file_detector=file_detector)
    else:
        bstack111l1l1l_opy_(self, command_executor=command_executor,
                  desired_capabilities=desired_capabilities,
                  browser_profile=browser_profile, proxy=proxy,
                  keep_alive=keep_alive)
    try:
        bstack1lllll1l1_opy_ = bstack1l1l1_opy_ (u"ࠪࠫᚮ")
        if bstack1ll111l11l_opy_() >= version.parse(bstack1l1l1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬᚯ")):
            bstack1lllll1l1_opy_ = self.caps.get(bstack1l1l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧᚰ"))
        else:
            bstack1lllll1l1_opy_ = self.capabilities.get(bstack1l1l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨᚱ"))
        if bstack1lllll1l1_opy_:
            bstack11lll11l1_opy_(bstack1lllll1l1_opy_)
            if bstack1ll111l11l_opy_() <= version.parse(bstack1l1l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧᚲ")):
                self.command_executor._url = bstack1l1l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤᚳ") + bstack11l1ll11_opy_ + bstack1l1l1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨᚴ")
            else:
                self.command_executor._url = bstack1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧᚵ") + bstack1lllll1l1_opy_ + bstack1l1l1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧᚶ")
            logger.debug(bstack111lll111_opy_.format(bstack1lllll1l1_opy_))
        else:
            logger.debug(bstack1l11ll1ll_opy_.format(bstack1l1l1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨᚷ")))
    except Exception as e:
        logger.debug(bstack1l11ll1ll_opy_.format(e))
    bstack1ll1ll1111_opy_ = self.session_id
    if bstack1l1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ᚸ") in bstack1lll111ll_opy_:
        threading.current_thread().bstackSessionId = self.session_id
        threading.current_thread().bstackSessionDriver = self
        threading.current_thread().bstackTestErrorMessages = []
        bstack1ll1l1llll_opy_.bstack111l111l_opy_(self)
    bstack1l1l11ll11_opy_.append(self)
    if bstack1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᚹ") in CONFIG and bstack1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ᚺ") in CONFIG[bstack1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚻ")][bstack1l1lll111l_opy_]:
        bstack1ll1lll111_opy_ = CONFIG[bstack1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᚼ")][bstack1l1lll111l_opy_][bstack1l1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᚽ")]
    logger.debug(bstack111l11ll1_opy_.format(bstack1ll1ll1111_opy_))
def bstack11111ll11_opy_(self, url):
    global bstack1llll111l_opy_
    global CONFIG
    try:
        bstack1lll1l1lll_opy_(url, CONFIG, logger)
    except Exception as err:
        logger.debug(bstack11l11llll_opy_.format(str(err)))
    try:
        bstack1llll111l_opy_(self, url)
    except Exception as e:
        try:
            bstack11111l11l_opy_ = str(e)
            if any(err_msg in bstack11111l11l_opy_ for err_msg in bstack1l1llllll_opy_):
                bstack1lll1l1lll_opy_(url, CONFIG, logger, True)
        except Exception as err:
            logger.debug(bstack11l11llll_opy_.format(str(err)))
        raise e
def bstack11111111l_opy_(item, when):
    global bstack1ll1lllll_opy_
    try:
        bstack1ll1lllll_opy_(item, when)
    except Exception as e:
        pass
def bstack1lll1lll11_opy_(item, call, rep):
    global bstack111ll11ll_opy_
    global bstack1l1l11ll11_opy_
    name = bstack1l1l1_opy_ (u"ࠬ࠭ᚾ")
    try:
        if rep.when == bstack1l1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࠫᚿ"):
            bstack1ll1ll1111_opy_ = threading.current_thread().bstackSessionId
            bstack1llll1l1111_opy_ = item.config.getoption(bstack1l1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩᛀ"))
            try:
                if (str(bstack1llll1l1111_opy_).lower() != bstack1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᛁ")):
                    name = str(rep.nodeid)
                    bstack1llll1l11_opy_ = bstack1lll1111ll_opy_(bstack1l1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᛂ"), name, bstack1l1l1_opy_ (u"ࠪࠫᛃ"), bstack1l1l1_opy_ (u"ࠫࠬᛄ"), bstack1l1l1_opy_ (u"ࠬ࠭ᛅ"), bstack1l1l1_opy_ (u"࠭ࠧᛆ"))
                    os.environ[bstack1l1l1_opy_ (u"ࠧࡑ࡛ࡗࡉࡘ࡚࡟ࡕࡇࡖࡘࡤࡔࡁࡎࡇࠪᛇ")] = name
                    for driver in bstack1l1l11ll11_opy_:
                        if bstack1ll1ll1111_opy_ == driver.session_id:
                            driver.execute_script(bstack1llll1l11_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡷࡪࡺࡴࡪࡰࡪࠤࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᛈ").format(str(e)))
            try:
                bstack1l1111ll1_opy_(rep.outcome.lower())
                if rep.outcome.lower() != bstack1l1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᛉ"):
                    status = bstack1l1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᛊ") if rep.outcome.lower() == bstack1l1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫᛋ") else bstack1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᛌ")
                    reason = bstack1l1l1_opy_ (u"࠭ࠧᛍ")
                    if status == bstack1l1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᛎ"):
                        reason = rep.longrepr.reprcrash.message
                        if (not threading.current_thread().bstackTestErrorMessages):
                            threading.current_thread().bstackTestErrorMessages = []
                        threading.current_thread().bstackTestErrorMessages.append(reason)
                    level = bstack1l1l1_opy_ (u"ࠨ࡫ࡱࡪࡴ࠭ᛏ") if status == bstack1l1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩᛐ") else bstack1l1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᛑ")
                    data = name + bstack1l1l1_opy_ (u"ࠫࠥࡶࡡࡴࡵࡨࡨࠦ࠭ᛒ") if status == bstack1l1l1_opy_ (u"ࠬࡶࡡࡴࡵࡨࡨࠬᛓ") else name + bstack1l1l1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠡࠡࠩᛔ") + reason
                    bstack1llllll111_opy_ = bstack1lll1111ll_opy_(bstack1l1l1_opy_ (u"ࠧࡢࡰࡱࡳࡹࡧࡴࡦࠩᛕ"), bstack1l1l1_opy_ (u"ࠨࠩᛖ"), bstack1l1l1_opy_ (u"ࠩࠪᛗ"), bstack1l1l1_opy_ (u"ࠪࠫᛘ"), level, data)
                    for driver in bstack1l1l11ll11_opy_:
                        if bstack1ll1ll1111_opy_ == driver.session_id:
                            driver.execute_script(bstack1llllll111_opy_)
            except Exception as e:
                logger.debug(bstack1l1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡥࡲࡲࡹ࡫ࡸࡵࠢࡩࡳࡷࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡷࡪࡹࡳࡪࡱࡱ࠾ࠥࢁࡽࠨᛙ").format(str(e)))
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡨࡧࡷࡸ࡮ࡴࡧࠡࡵࡷࡥࡹ࡫ࠠࡪࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࠥࡹࡴࡢࡶࡸࡷ࠿ࠦࡻࡾࠩᛚ").format(str(e)))
    bstack111ll11ll_opy_(item, call, rep)
notset = Notset()
def bstack1111ll1ll_opy_(self, name: str, default=notset, skip: bool = False):
    global bstack1l1l1llll_opy_
    if str(name).lower() == bstack1l1l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷ࠭ᛛ"):
        return bstack1l1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠨᛜ")
    else:
        return bstack1l1l1llll_opy_(self, name, default, skip)
def bstack1l1l1lll_opy_(self):
    global CONFIG
    global bstack1lllll1l11_opy_
    try:
        proxy = bstack1l111lll1_opy_(CONFIG)
        if proxy:
            if proxy.endswith(bstack1l1l1_opy_ (u"ࠨ࠰ࡳࡥࡨ࠭ᛝ")):
                proxies = bstack1111l11ll_opy_(proxy, bstack1l111l111_opy_())
                if len(proxies) > 0:
                    protocol, bstack1ll11ll1_opy_ = proxies.popitem()
                    if bstack1l1l1_opy_ (u"ࠤ࠽࠳࠴ࠨᛞ") in bstack1ll11ll1_opy_:
                        return bstack1ll11ll1_opy_
                    else:
                        return bstack1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰ࠻࠱࠲ࠦᛟ") + bstack1ll11ll1_opy_
            else:
                return proxy
    except Exception as e:
        logger.error(bstack1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡱࡴࡲࡼࡾࠦࡵࡳ࡮ࠣ࠾ࠥࢁࡽࠣᛠ").format(str(e)))
    return bstack1lllll1l11_opy_(self)
def bstack1lll11l111_opy_():
    return (bstack1l1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨᛡ") in CONFIG or bstack1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᛢ") in CONFIG) and bstack1lll111l_opy_() and bstack1ll111l11l_opy_() >= version.parse(
        bstack1llll1llll_opy_)
def bstack1ll1llll_opy_(self,
               executablePath=None,
               channel=None,
               args=None,
               ignoreDefaultArgs=None,
               handleSIGINT=None,
               handleSIGTERM=None,
               handleSIGHUP=None,
               timeout=None,
               env=None,
               headless=None,
               devtools=None,
               proxy=None,
               downloadsPath=None,
               slowMo=None,
               tracesDir=None,
               chromiumSandbox=None,
               firefoxUserPrefs=None
               ):
    global CONFIG
    global bstack1ll1lll111_opy_
    global bstack1l1111l1l_opy_
    global bstack1lll111ll_opy_
    CONFIG[bstack1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࡙ࡄࡌࠩᛣ")] = str(bstack1lll111ll_opy_) + str(__version__)
    bstack1l1lll111l_opy_ = 0
    try:
        if bstack1l1111l1l_opy_ is True:
            bstack1l1lll111l_opy_ = int(os.environ.get(bstack1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡌࡒࡉࡋࡘࠨᛤ")))
    except:
        bstack1l1lll111l_opy_ = 0
    CONFIG[bstack1l1l1_opy_ (u"ࠤ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠣᛥ")] = True
    bstack111l11111_opy_ = bstack1lll1l1l1_opy_(CONFIG, bstack1l1lll111l_opy_)
    logger.debug(bstack1l1llll111_opy_.format(str(bstack111l11111_opy_)))
    if CONFIG.get(bstack1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࠧᛦ")):
        bstack1ll111l111_opy_(bstack111l11111_opy_, bstack1lll1111_opy_)
    if bstack1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᛧ") in CONFIG and bstack1l1l1_opy_ (u"ࠬࡹࡥࡴࡵ࡬ࡳࡳࡔࡡ࡮ࡧࠪᛨ") in CONFIG[bstack1l1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᛩ")][bstack1l1lll111l_opy_]:
        bstack1ll1lll111_opy_ = CONFIG[bstack1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᛪ")][bstack1l1lll111l_opy_][bstack1l1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭᛫")]
    import urllib
    import json
    bstack1lll1lllll_opy_ = bstack1l1l1_opy_ (u"ࠩࡺࡷࡸࡀ࠯࠰ࡥࡧࡴ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࡄࡩࡡࡱࡵࡀࠫ᛬") + urllib.parse.quote(json.dumps(bstack111l11111_opy_))
    browser = self.connect(bstack1lll1lllll_opy_)
    return browser
def bstack1lll1lll1_opy_():
    global bstack1111l1lll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        BrowserType.launch = bstack1ll1llll_opy_
        bstack1111l1lll_opy_ = True
    except Exception as e:
        pass
def bstack1lllll1l11l_opy_():
    global CONFIG
    global bstack1111111ll_opy_
    global bstack11l1ll11_opy_
    global bstack1lll1111_opy_
    global bstack1l1111l1l_opy_
    CONFIG = json.loads(os.environ.get(bstack1l1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࠩ᛭")))
    bstack1111111ll_opy_ = eval(os.environ.get(bstack1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡍࡘࡥࡁࡑࡒࡢࡅ࡚࡚ࡏࡎࡃࡗࡉࠬᛮ")))
    bstack11l1ll11_opy_ = os.environ.get(bstack1l1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡍ࡛ࡂࡠࡗࡕࡐࠬᛯ"))
    bstack1lll1lll1l_opy_(CONFIG, bstack1111111ll_opy_)
    bstack1ll1lll1l_opy_()
    global bstack111l1l1l_opy_
    global bstack11l1l1l1_opy_
    global bstack1lll11ll11_opy_
    global bstack111l1ll1l_opy_
    global bstack1ll11lll11_opy_
    global bstack1ll1llllll_opy_
    global bstack1lllll111l_opy_
    global bstack1llll111l_opy_
    global bstack1lllll1l11_opy_
    global bstack1l1l1llll_opy_
    global bstack1ll1lllll_opy_
    global bstack111ll11ll_opy_
    try:
        from selenium import webdriver
        from selenium.webdriver.remote.webdriver import WebDriver
        bstack111l1l1l_opy_ = webdriver.Remote.__init__
        bstack11l1l1l1_opy_ = WebDriver.quit
        bstack1lllll111l_opy_ = WebDriver.close
        bstack1llll111l_opy_ = WebDriver.get
    except Exception as e:
        pass
    if (bstack1l1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩᛰ") in CONFIG or bstack1l1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫᛱ") in CONFIG) and bstack1lll111l_opy_():
        if bstack1ll111l11l_opy_() < version.parse(bstack1llll1llll_opy_):
            logger.error(bstack1l1llll1ll_opy_.format(bstack1ll111l11l_opy_()))
        else:
            try:
                from selenium.webdriver.remote.remote_connection import RemoteConnection
                bstack1lllll1l11_opy_ = RemoteConnection._get_proxy_url
            except Exception as e:
                logger.error(bstack1l111111l_opy_.format(str(e)))
    try:
        from _pytest.config import Config
        bstack1l1l1llll_opy_ = Config.getoption
        from _pytest import runner
        bstack1ll1lllll_opy_ = runner._update_current_test_var
    except Exception as e:
        logger.warn(e, bstack1ll11l1l11_opy_)
    try:
        from pytest_bdd import reporting
        bstack111ll11ll_opy_ = reporting.runtest_makereport
    except Exception as e:
        logger.debug(bstack1l1l1_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡰࠢࡵࡹࡳࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡪࡹࡴࡴࠩᛲ"))
    bstack1lll1111_opy_ = CONFIG.get(bstack1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛳ"), {}).get(bstack1l1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬᛴ"))
    bstack1l1111l1l_opy_ = True
    bstack11111ll1_opy_(bstack111lllll1_opy_)
if (bstack11ll1111ll_opy_()):
    bstack1lllll1l11l_opy_()
@bstack1l111llll1_opy_(class_method=False)
def bstack1lllll1l1l1_opy_(hook_name, event, bstack1llllll1111_opy_=None):
    if hook_name not in [bstack1l1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲࡢࡪࡺࡴࡣࡵ࡫ࡲࡲࠬᛵ"), bstack1l1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᛶ"), bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬᛷ"), bstack1l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᛸ"), bstack1l1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟ࡤ࡮ࡤࡷࡸ࠭᛹"), bstack1l1l1_opy_ (u"ࠩࡷࡩࡦࡸࡤࡰࡹࡱࡣࡨࡲࡡࡴࡵࠪ᛺"), bstack1l1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࡡࡰࡩࡹ࡮࡯ࡥࠩ᛻"), bstack1l1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥ࡭ࡦࡶ࡫ࡳࡩ࠭᛼")]:
        return
    node = store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡴࡦࡵࡷࡣ࡮ࡺࡥ࡮ࠩ᛽")]
    if hook_name in [bstack1l1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳ࡯ࡥࡷ࡯ࡩࠬ᛾"), bstack1l1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩ᛿")]:
        node = store[bstack1l1l1_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡰࡳࡩࡻ࡬ࡦࡡ࡬ࡸࡪࡳࠧᜀ")]
    elif hook_name in [bstack1l1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᜁ"), bstack1l1l1_opy_ (u"ࠪࡸࡪࡧࡲࡥࡱࡺࡲࡤࡩ࡬ࡢࡵࡶࠫᜂ")]:
        node = store[bstack1l1l1_opy_ (u"ࠫࡨࡻࡲࡳࡧࡱࡸࡤࡩ࡬ࡢࡵࡶࡣ࡮ࡺࡥ࡮ࠩᜃ")]
    if event == bstack1l1l1_opy_ (u"ࠬࡨࡥࡧࡱࡵࡩࠬᜄ"):
        hook_type = bstack1111ll111l_opy_(hook_name)
        uuid = uuid4().__str__()
        bstack1l11ll1111_opy_ = {
            bstack1l1l1_opy_ (u"࠭ࡵࡶ࡫ࡧࠫᜅ"): uuid,
            bstack1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᜆ"): bstack1l11lllll_opy_(),
            bstack1l1l1_opy_ (u"ࠨࡶࡼࡴࡪ࠭ᜇ"): bstack1l1l1_opy_ (u"ࠩ࡫ࡳࡴࡱࠧᜈ"),
            bstack1l1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡶࡼࡴࡪ࠭ᜉ"): hook_type,
            bstack1l1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡱࡥࡲ࡫ࠧᜊ"): hook_name
        }
        store[bstack1l1l1_opy_ (u"ࠬࡩࡵࡳࡴࡨࡲࡹࡥࡨࡰࡱ࡮ࡣࡺࡻࡩࡥࠩᜋ")].append(uuid)
        bstack1llll1l11ll_opy_ = node.nodeid
        if hook_type == bstack1l1l1_opy_ (u"࠭ࡂࡆࡈࡒࡖࡊࡥࡅࡂࡅࡋࠫᜌ"):
            if not _1l111l111l_opy_.get(bstack1llll1l11ll_opy_, None):
                _1l111l111l_opy_[bstack1llll1l11ll_opy_] = {bstack1l1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡸ࠭ᜍ"): []}
            _1l111l111l_opy_[bstack1llll1l11ll_opy_][bstack1l1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᜎ")].append(bstack1l11ll1111_opy_[bstack1l1l1_opy_ (u"ࠩࡸࡹ࡮ࡪࠧᜏ")])
        _1l111l111l_opy_[bstack1llll1l11ll_opy_ + bstack1l1l1_opy_ (u"ࠪ࠱ࠬᜐ") + hook_name] = bstack1l11ll1111_opy_
        bstack1lllll1l1ll_opy_(node, bstack1l11ll1111_opy_, bstack1l1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᜑ"))
    elif event == bstack1l1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࠫᜒ"):
        bstack1l11ll1l1l_opy_ = node.nodeid + bstack1l1l1_opy_ (u"࠭࠭ࠨᜓ") + hook_name
        _1l111l111l_opy_[bstack1l11ll1l1l_opy_][bstack1l1l1_opy_ (u"ࠧࡧ࡫ࡱ࡭ࡸ࡮ࡥࡥࡡࡤࡸ᜔ࠬ")] = bstack1l11lllll_opy_()
        bstack1llll1l11l1_opy_(_1l111l111l_opy_[bstack1l11ll1l1l_opy_][bstack1l1l1_opy_ (u"ࠨࡷࡸ࡭ࡩ᜕࠭")])
        bstack1lllll1l1ll_opy_(node, _1l111l111l_opy_[bstack1l11ll1l1l_opy_], bstack1l1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ᜖"), bstack1llll1ll1ll_opy_=bstack1llllll1111_opy_)
def bstack1llll1l1lll_opy_():
    global bstack1lllll1ll1l_opy_
    if bstack1l1l1ll1ll_opy_():
        bstack1lllll1ll1l_opy_ = bstack1l1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠧ᜗")
    else:
        bstack1lllll1ll1l_opy_ = bstack1l1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ᜘")
@bstack1ll1l1llll_opy_.bstack1111111l11_opy_
def bstack1lllll11ll1_opy_():
    bstack1llll1l1lll_opy_()
    if bstack1lll111l_opy_():
        bstack11ll11111_opy_(bstack111l111ll_opy_)
    bstack11l111llll_opy_ = bstack11l11ll111_opy_(bstack1lllll1l1l1_opy_)
bstack1lllll11ll1_opy_()