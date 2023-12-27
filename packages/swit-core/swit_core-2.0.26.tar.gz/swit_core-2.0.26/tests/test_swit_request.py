import json  # noqa: F401
import unittest

from switcore.action.schemas import SwitResponse, ViewCallbackType, View, Body, AttachmentCallbackTypes, AttachmentView, \
    AttachmentBody, SuggestionsCallbackTypes, SuggestionsResult, NoOptionsReason, SwitRequest, UserActionType
from switcore.ui.divider import Divider
from switcore.ui.element_components import Tag, TagStyle, TagColorTypes, TagShapeTypes
from switcore.ui.header import Header, AttachmentHeader
from switcore.ui.image import Image
from switcore.ui.select import Option, OptionGroup
from switcore.ui.text_paragraph import TextParagraph
from tests.utils import create_submit_swit_request, create_query_swit_request


class SwitViewResponseTest(unittest.TestCase):

    def test_swit_response_view(self):
        swit_request: SwitRequest = create_query_swit_request("right_panel", "test_action_id01")
        self.assertEqual(swit_request.user_action.type, UserActionType.view_actions_submit)