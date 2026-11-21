import unittest
from unittest.mock import call, create_autospec, patch

from bot.dispatcher import Dispatcher
from bot.long_polling import poll_once, start_long_polling
from bot.messenger import Messenger


class LongPollingTest(unittest.TestCase):
    def setUp(self):
        self.dispatcher = create_autospec(Dispatcher, instance=True, spec_set=True)
        self.messenger = create_autospec(Messenger, instance=True, spec_set=True)

    def test_requests_updates_and_never_moves_offset_backwards(self):
        first, second = {"update_id": 42}, {"update_id": 40}
        self.messenger.get_updates.return_value = [first, second]

        self.assertEqual(list(poll_once(self.dispatcher, self.messenger, 40)), [43, 43])

        self.messenger.get_updates.assert_called_once_with(
            offset=40, limit=10, timeout=30, allowed_updates=["message"]
        )
        self.assertEqual(self.dispatcher.dispatch.call_args_list, [call(first), call(second)])

    def test_empty_batch_dispatches_nothing(self):
        self.messenger.get_updates.return_value = []

        self.assertEqual(list(poll_once(self.dispatcher, self.messenger, 40)), [])

        self.dispatcher.dispatch.assert_not_called()

    def test_a_failed_update_yields_no_offset_and_stops_the_batch(self):
        first, failed, pending = ({"update_id": number} for number in (40, 41, 42))
        self.messenger.get_updates.return_value = [first, failed, pending]
        self.dispatcher.dispatch.side_effect = [None, RuntimeError("send failed")]
        offsets = poll_once(self.dispatcher, self.messenger, 40)

        self.assertEqual(next(offsets), 41)
        with self.assertRaisesRegex(RuntimeError, "send failed"):
            next(offsets)

        self.assertEqual(self.dispatcher.dispatch.call_args_list, [call(first), call(failed)])

    def test_retries_after_network_error_with_last_saved_offset(self):
        update = {"update_id": 40}
        self.messenger.get_updates.side_effect = [[update], OSError("offline"), KeyboardInterrupt]

        with (
            patch("bot.long_polling.time.sleep") as sleep,
            self.assertLogs("bot.long_polling"),
            self.assertRaises(KeyboardInterrupt),
        ):
            start_long_polling(self.dispatcher, self.messenger)

        offsets = [
            request.kwargs["offset"] for request in self.messenger.get_updates.call_args_list
        ]
        self.assertEqual(offsets, [0, 41, 41])
        self.dispatcher.dispatch.assert_called_once_with(update)
        sleep.assert_called_once_with(5)
