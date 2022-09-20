from asyncio import new_event_loop
import threading

from event_service_utils.logging.decorators import timer_logger
from event_service_utils.services.event_driven import BaseEventDrivenCMDService
from event_service_utils.tracing.jaeger import init_tracer

from worker_profile_rating.conf import (
    LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED,
    PUB_EVENT_TYPE_WORKER_PROFILE_RATED,
    RATING_CLASS,
    QOS_CRITERIA,
)
from worker_profile_rating.rating_modules.crisp import RatingModuleCrisp
from worker_profile_rating.rating_modules.fuzzy import RatingModuleFuzzy


class WorkerProfileRating(BaseEventDrivenCMDService):
    def __init__(self,
                 service_stream_key, service_cmd_key_list,
                 pub_event_list, service_details,
                 stream_factory,
                 logging_level,
                 tracer_configs):
        tracer = init_tracer(self.__class__.__name__, **tracer_configs)
        super(WorkerProfileRating, self).__init__(
            name=self.__class__.__name__,
            service_stream_key=service_stream_key,
            service_cmd_key_list=service_cmd_key_list,
            pub_event_list=pub_event_list,
            service_details=service_details,
            stream_factory=stream_factory,
            logging_level=logging_level,
            tracer=tracer,
        )
        self.cmd_validation_fields = ['id']
        self.data_validation_fields = ['id']
        self.rating_class = RATING_CLASS
        self.rating_module = None
        self.setup_rating_module()


    def setup_rating_module(self):
        self.available_rating_modules = {
            'Crisp': RatingModuleCrisp,
            'Fuzzy': RatingModuleFuzzy,
        }

        self.rating_module = self.available_rating_modules[self.rating_class](QOS_CRITERIA)

    def publish_worker_profile_rated(self, worker_rating):
        worker_rating['id'] = self.service_based_random_event_id()
        self.publish_event_type_to_stream(event_type=PUB_EVENT_TYPE_WORKER_PROFILE_RATED, new_event_data=worker_rating)

    def process_service_worker_announced(self, worker_data):
        # 'worker': {
        #     'service_type': 'ColorDetection',
        #     'stream_key': 'clrworker-key',
        #     'queue_limit': 100,
        #     'throughput': 1,
        #     'accuracy': 0.9,
        #     'energy_consumption': 10,
        # }
        service_type = worker_data['service_type']
        stream_key = worker_data['stream_key']
        worker_rating = self.rating_module.get_worker_profile_rating(worker_data)
        self.publish_worker_profile_rated(worker_rating)

    def process_event_type(self, event_type, event_data, json_msg):
        if not super(WorkerProfileRating, self).process_event_type(event_type, event_data, json_msg):
            return False
        if event_type == LISTEN_EVENT_TYPE_SERVICE_WORKER_ANNOUNCED:
            self.process_service_worker_announced(event_data['worker'])

    def log_state(self):
        super(WorkerProfileRating, self).log_state()
        self.logger.info(f'Service name: {self.name}')
        self.logger.info(f'Rating class: {self.rating_class}')
        self.logger.info(f'Rating range (by Service Type): {self.rating_module.criteria_range_by_service_type}')

        # function for simple logging of python dictionary
        # self._log_dict('Some Dictionary', self.some_dict)

    def run(self):
        super(WorkerProfileRating, self).run()
        self.log_state()
        self.cmd_thread = threading.Thread(target=self.run_forever, args=(self.process_cmd,))
        self.cmd_thread.start()
        self.cmd_thread.join()
