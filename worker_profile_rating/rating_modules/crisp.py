from worker_profile_rating.rating_modules.base import RatingModuleBase

class RatingModuleCrisp(RatingModuleBase):
    def calculate_worker_criterion_rating_for_service_type(self, service_type, criterion, worker_value):
        return worker_value