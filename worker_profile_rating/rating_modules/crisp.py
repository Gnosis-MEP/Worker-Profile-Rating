from worker_profile_rating.rating_modules.base import RatingModuleBase

class RatingModuleCrisp(RatingModuleBase):
    def calculate_worker_criterion_rating_from_crisp_rating(self, crisp_rating):
        return crisp_rating