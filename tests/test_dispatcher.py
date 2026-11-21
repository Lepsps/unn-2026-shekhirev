import unittest
from unittest.mock import Mock, call, create_autospec

from bot.dispatcher import Dispatcher
from bot.handlers.handler import Handler, HandlerStatus
from bot.messenger import Messenger


class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.messenger = create_autospec(Messenger, instance=True, spec_set=True)
        self.dispatcher = Dispatcher(self.messenger)

    def test_skips_mismatches_continues_on_continue_and_stops_on_stop(self):
        update = {"update_id": 1}
        skipped = create_autospec(Handler, instance=True, spec_set=True)
        continuing = create_autospec(Handler, instance=True, spec_set=True)
        stopping = create_autospec(Handler, instance=True, spec_set=True)
        unreachable = create_autospec(Handler, instance=True, spec_set=True)
        skipped.can_handle.return_value = False
        continuing.can_handle.return_value = stopping.can_handle.return_value = True
        continuing.handle.return_value = HandlerStatus.CONTINUE
        stopping.handle.return_value = HandlerStatus.STOP
        trace = Mock()
        trace.attach_mock(skipped, "skipped")
        trace.attach_mock(continuing, "continuing")
        trace.attach_mock(stopping, "stopping")
        trace.attach_mock(unreachable, "unreachable")
        self.dispatcher.add_handlers(skipped, continuing, stopping, unreachable)

        self.dispatcher.dispatch(update)

        self.assertEqual(
            trace.mock_calls,
            [
                call.skipped.can_handle(update),
                call.continuing.can_handle(update),
                call.continuing.handle(update, self.messenger),
                call.stopping.can_handle(update),
                call.stopping.handle(update, self.messenger),
            ],
        )

    def test_propagates_send_failure_to_polling(self):
        handler = create_autospec(Handler, instance=True, spec_set=True)
        handler.can_handle.return_value = True
        handler.handle.side_effect = RuntimeError("send failed")
        self.dispatcher.add_handlers(handler)

        with self.assertRaisesRegex(RuntimeError, "send failed"):
            self.dispatcher.dispatch({"update_id": 1})
