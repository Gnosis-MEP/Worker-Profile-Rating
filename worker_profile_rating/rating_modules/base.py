class RatingModuleBase(object):
    def __init__(self, qos_criteria, scale_ratings=True, default_criteria_ranges=None):
        self.qos_criteria = qos_criteria
        if default_criteria_ranges is None:
            default_criteria_ranges = {}
        self.criteria_range_by_service_type = default_criteria_ranges
        self.rating_range = (1, 10)
        self.scale_ratings = scale_ratings

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
        target_lower, target_upper = self.rating_range
        criterion_range = self.criteria_range_by_service_type.get(service_type, {}).get(criterion)
        origin_lower, origin_upper = criterion_range
        if origin_lower == origin_upper and origin_lower == value:
            return target_upper

        diff_to_origin_lower = (value - origin_lower)
        target_difference = (target_upper - target_lower)
        origin_difference = (origin_upper - origin_lower)

        norm_incomplete = diff_to_origin_lower * target_difference / origin_difference

        norm = target_lower + norm_incomplete
        crisp_rating = round(norm)
        return crisp_rating

    def calculate_worker_criterion_rating_for_service_type(self, service_type, criterion, worker_value):
        raise NotImplemented()

    def get_worker_qos_criteria_ratings(self, worker_data):
        service_type = worker_data['service_type']
        ratings = {}
        for criterion in self.qos_criteria:
            worker_value = worker_data.get(criterion, None)
            if worker_value is None:
                continue

            ratings[criterion] = self.calculate_worker_criterion_rating_for_service_type(service_type, criterion, worker_value)
        return ratings

    def get_worker_profile_rating(self, worker_data):
        self.update_criteria_range_from_worker(worker_data)
        base_profile_rating = {
            'worker':{
                'service_type': worker_data['service_type'],
                'stream_key': worker_data['stream_key'],
            }
        }
        base_profile_rating['worker'].update(self.get_worker_qos_criteria_ratings(worker_data))
        return base_profile_rating

