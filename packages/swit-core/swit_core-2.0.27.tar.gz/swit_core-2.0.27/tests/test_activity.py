# import datetime
# import unittest
#
# from switcore.action.activity_router import ActivityRouter, PathResolver
# from switcore.action.async_activity_handler_abc import AsyncActivityHandlerABC
# from switcore.action.exceptions import UndefinedSubmitAction
# from switcore.action.schemas import SwitRequest, PlatformTypes, UserInfo, UserPreferences, Context, UserAction, \
#     UserActionType, View, Body, BaseState, SwitResponse, ViewCallbackType
# from switcore.ui.header import Header
# from tests.utils import ActivityHandler, create_submit_swit_request
#
#
# class RouterTest(unittest.IsolatedAsyncioTestCase):
#
#     async def asyncSetUp(self) -> None:
#         self.activity_handler = ActivityHandler()
#         return await super().asyncSetUp()
#
#     async def test_(self):
#         activity_router = ActivityRouter()
#         action_id: str = str(PathResolver("test_action_id01"))
#         swit_request: SwitRequest = create_submit_swit_request("right_panel", action_id)
#
#         @activity_router.register("test_action_id01")
#         async def draw_webhook_create(request: SwitRequest, state: BaseState):  # noqa F811
#             return SwitResponse(callback_type=ViewCallbackType.update)
#
#         self.activity_handler.include_activity_router(activity_router)
#
#         swit_response = await self.activity_handler.on_turn(swit_request, BaseState())
#         self.assertTrue(isinstance(swit_response, SwitResponse))
