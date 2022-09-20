class RatingModuleBase(object):
    def __init__(self, qos_criteria, default_criteria_ranges):
        self.qos_criteria = qos_criteria
        self.criteria_range_by_service_type = {}
        self.rating_range = (0, 10)

    def update_criteria_range_from_worker(self, worker_data):
        service_type = worker_data['service_type']
        service_type_crit_range = self.criteria_range_by_service_type.setdefault(
            service_type,
            {
                k: None for k in self.qos_criteria
            }
        )

        changed_criterion = []
        # 'worker': {
        #     'service_type': 'ColorDetection',
        #     'stream_key': 'clrworker-key',
        #     'queue_limit': 100,
        #     'throughput': 1,
        #     'accuracy': 0.9,
        #     'energy_consumption': 10,
        # }
        for criterion in self.qos_criteria:
            value = worker_data.get(criterion, None)
            if value is not None:
                criterion_range = service_type_crit_range[criterion]
                if criterion_range is None:
                    service_type_crit_range[criterion] = [value, value]

                else:
                    if value < criterion_range[0]:
                        criterion_range[0] = value
                        changed_criterion.append(criterion)
                    if value > criterion_range[1]:
                        criterion_range[1] = value
                        changed_criterion.append(criterion)
        return changed_criterion

    def get_criterion_crisp_rating_for_service_type(self, service_type, criterion, value):
        criterion_range = self.criteria_range_by_service_type.get(service_type, {}).get(criterion)
        lower, upper = criterion_range
        norm_upper_lower = (upper - lower)
        norm = (value - lower) / (upper - lower)
        crisp_rating = norm * 10
        return crisp_rating

    def calculate_worker_criterion_rating_from_crisp_rating(self, crisp_rating):
        raise NotImplemented()

    def get_worker_qos_criteria_ratings(self, worker_data):
        service_type = worker_data['service_type']
        ratings = {}
        for criterion in self.qos_criteria:
            worker_value = worker_data.get(criterion, None)
            if worker_value is None:
                continue

            crisp_rating = self.get_criterion_crisp_rating_for_service_type(service_type, criterion, worker_value)
            ratings[criterion] = self.calculate_worker_criterion_rating_from_crisp_rating(crisp_rating)
        return ratings

    def get_worker_profile_rating(self, worker_data):
        self.update_criteria_range_from_worker(worker_data)
        base_profile_rating = {
            'worker':{
                'service_type': worker_data['service_type'],
                'stream_key': worker_data['stream_key'],
            }
        }
        base_profile_rating.update(self.get_worker_qos_criteria_ratings(worker_data))
        return base_profile_rating

