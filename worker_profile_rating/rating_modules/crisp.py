from worker_profile_rating.rating_modules.base import RatingModuleBase

class RatingModuleCrisp(RatingModuleBase):
    def calculate_worker_criterion_rating_for_service_type(self, service_type, criterion, worker_value):
        rating = worker_value
        if self.scale_ratings:
            crisp_rating = self.get_criterion_crisp_rating_for_service_type(service_type, criterion, worker_value)
            rating = crisp_rating
        return rating