#!/usr/bin/env python
import uuid
import json
from event_service_utils.streams.redis import RedisStreamFactory

from worker_profile_rating.conf import (
    REDIS_ADDRESS,
    REDIS_PORT,
    SERVICE_STREAM_KEY,
    LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED
)


def make_dict_key_bites(d):
    return {k.encode('utf-8'): v for k, v in d.items()}


def new_msg(event_data):
    event_data.update({'id': str(uuid.uuid4())})
    return {'event': json.dumps(event_data)}



def main():
    stream_factory = RedisStreamFactory(host=REDIS_ADDRESS, port=REDIS_PORT)
    # for checking published events output
    # new_event_type_cmd = stream_factory.create(PUB_EVENT_TYPE_NEW_EVENT_TYPE, stype='streamOnly')

    # for testing sending msgs that the service listens to:
    import ipdb; ipdb.set_trace()
    worker_announce_cmd = stream_factory.create(LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED, stype='streamOnly')
    worker_announce_cmd.write_events(
        new_msg(
            {
                'worker': {
                    'service_type': 'SomeService',
                    'stream_key': 'SomeServiceA',
                    'queue_limit': 100,
                    'throughput': 20,
                    'accuracy': 0.7,
                    'energy_consumption': 100,
                }
            }
        )
    )
    worker_announce_cmd.write_events(
        new_msg(
            {
                'worker': {
                    'service_type': 'SomeService',
                    'stream_key': 'SomeServiceB',
                    'queue_limit': 100,
                    'throughput': 10,
                    'accuracy': 0.9,
                    'energy_consumption': 60,
                }
            }
        )
    )
    worker_announce_cmd.write_events(
        new_msg(
            {
                'worker': {
                    'service_type': 'AnotherService',
                    'stream_key': 'AnotherServiceC',
                    'queue_limit': 100,
                    'throughput': 15,
                    'accuracy': 0.6,
                    'energy_consumption': 120,
                }
            }
        )
    )
    import ipdb; ipdb.set_trace()

    # read published events output
    # events = new_event_type_cmd.read_events()
    # print(list(events))
    # import ipdb; ipdb.set_trace()


if __name__ == '__main__':
    main()
