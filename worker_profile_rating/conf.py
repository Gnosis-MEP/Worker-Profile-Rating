import json
import os

from decouple import config, Csv

SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SOURCE_DIR)

REDIS_ADDRESS = config('REDIS_ADDRESS', default='localhost')
REDIS_PORT = config('REDIS_PORT', default='6379')

TRACER_REPORTING_HOST = config('TRACER_REPORTING_HOST', default='localhost')
TRACER_REPORTING_PORT = config('TRACER_REPORTING_PORT', default='6831')

SERVICE_STREAM_KEY = config('SERVICE_STREAM_KEY')

RATING_CLASS = config('RATING_CLASS')

SCALE_RATINGS = config('SCALE_RATINGS', default=True)

DEFAULT_QOS_CRITERIA = 'energy_consumption,throughput,accuracy'

QOS_CRITERIA = config('QOS_CRITERIA', default=DEFAULT_QOS_CRITERIA, cast=Csv())


def cast_default_criteria_range_by_service_type(value):
    ret = {}

    if value != '':
        for service_type_and_criterias in value.split(';'):
            service_type_ranges = {}
            service_type, criteria_list = service_type_and_criterias.split('/')
            for criterion_and_val in criteria_list.split(','):
                criterion, val_list = criterion_and_val.split(':')
                lower, upper = [float(x) for x in val_list.split('_')]
                service_type_ranges[criterion] = [lower, upper]

            ret[service_type] = service_type_ranges
    return ret

DEFAULT_CRITERIA_RANGE_BY_SERVICE_TYPE = config('DEFAULT_CRITERIA_RANGE_BY_SERVICE_TYPE', cast=cast_default_criteria_range_by_service_type, default='')


LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED = config('LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED')

SERVICE_CMD_KEY_LIST = [
    LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED,
]

PUB_EVENT_TYPE_WORKER_PROFILE_RATED = config('PUB_EVENT_TYPE_WORKER_PROFILE_RATED')

PUB_EVENT_LIST = [
    PUB_EVENT_TYPE_WORKER_PROFILE_RATED,
]

# Only for Content Extraction services
SERVICE_DETAILS = None

# Example of how to define SERVICE_DETAILS from env vars:
# SERVICE_DETAILS_SERVICE_TYPE = config('SERVICE_DETAILS_SERVICE_TYPE')
# SERVICE_DETAILS_STREAM_KEY = config('SERVICE_DETAILS_STREAM_KEY')
# SERVICE_DETAILS_QUEUE_LIMIT = config('SERVICE_DETAILS_QUEUE_LIMIT', cast=int)
# SERVICE_DETAILS_THROUGHPUT = config('SERVICE_DETAILS_THROUGHPUT', cast=float)
# SERVICE_DETAILS_ACCURACY = config('SERVICE_DETAILS_ACCURACY', cast=float)
# SERVICE_DETAILS_ENERGY_CONSUMPTION = config('SERVICE_DETAILS_ENERGY_CONSUMPTION', cast=float)
# SERVICE_DETAILS_CONTENT_TYPES = config('SERVICE_DETAILS_CONTENT_TYPES', cast=Csv())
# SERVICE_DETAILS = {
#     'service_type': SERVICE_DETAILS_SERVICE_TYPE,
#     'stream_key': SERVICE_DETAILS_STREAM_KEY,
#     'queue_limit': SERVICE_DETAILS_QUEUE_LIMIT,
#     'throughput': SERVICE_DETAILS_THROUGHPUT,
#     'accuracy': SERVICE_DETAILS_ACCURACY,
#     'energy_consumption': SERVICE_DETAILS_ENERGY_CONSUMPTION,
#     'content_types': SERVICE_DETAILS_CONTENT_TYPES
# }

LOGGING_LEVEL = config('LOGGING_LEVEL', default='DEBUG')