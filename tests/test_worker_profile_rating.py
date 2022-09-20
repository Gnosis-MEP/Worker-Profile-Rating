from unittest.mock import patch

from event_service_utils.tests.base_test_case import MockedEventDrivenServiceStreamTestCase
from event_service_utils.tests.json_msg_helper import prepare_event_msg_tuple

from worker_profile_rating.service import WorkerProfileRating

from worker_profile_rating.conf import (
    SERVICE_STREAM_KEY,
    SERVICE_CMD_KEY_LIST,
    SERVICE_DETAILS,
    PUB_EVENT_LIST,
)


class TestWorkerProfileRating(MockedEventDrivenServiceStreamTestCase):
    GLOBAL_SERVICE_CONFIG = {
        'service_stream_key': SERVICE_STREAM_KEY,
        'service_cmd_key_list': SERVICE_CMD_KEY_LIST,
        'pub_event_list': PUB_EVENT_LIST,
        'service_details': SERVICE_DETAILS,
        'logging_level': 'ERROR',
        'tracer_configs': {'reporting_host': None, 'reporting_port': None},
    }
    SERVICE_CLS = WorkerProfileRating

    MOCKED_CG_STREAM_DICT = {

    }

    MOCKED_STREAMS_DICT = {
        SERVICE_STREAM_KEY: [],
        'cg-WorkerProfileRating': MOCKED_CG_STREAM_DICT,
    }

    @patch('worker_profile_rating.service.WorkerProfileRating.process_event_type')
    def test_process_cmd_should_call_process_event_type(self, mocked_process_event_type):
        event_type = 'SomeEventType'
        unicode_event_type = event_type.encode('utf-8')
        event_data = {
            'id': 1,
            'action': event_type,
            'some': 'stuff'
        }
        msg_tuple = prepare_event_msg_tuple(event_data)
        mocked_process_event_type.__name__ = 'process_event_type'

        self.service.service_cmd.mocked_values_dict = {
            unicode_event_type: [msg_tuple]
        }
        self.service.process_cmd()
        self.assertTrue(mocked_process_event_type.called)
        self.service.process_event_type.assert_called_once_with(event_type=event_type, event_data=event_data, json_msg=msg_tuple[1])

