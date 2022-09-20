from worker_profile_rating.rating_modules.base import RatingModuleBase

class RatingModuleFuzzy(RatingModuleBase):
    def __init__(self, qos_criteria):
        super().__init__(qos_criteria)
        self.criteria_rating_mfs = {
            'high': (7, 9, 10), # 9, 10
            'medium_high': (5, 7, 9), # 7, 8
            'medium': (3, 5, 7), # 5, 6
            'medium_low': (1, 3, 5), # 3, 4
            'low': (0, 1, 3), # 0, 1, 2
        }
        self.sorted_mfs_modals = {
            v[1]: k for k, v in
            sorted(self.criteria_rating_mfs.items(), key=lambda dt: dt[1][1])
        }

    def calculate_worker_criterion_rating_from_crisp_rating(self, crisp_rating):
        # use highest activation / lowervalue in case of ties
        # closest_mf = self.criteria_rating_mfs['low']
        closest_mf = None
        for modal, mf_l in self.sorted_mfs_modals.items():
            if modal < crisp_rating:
                dist = crisp_rating - modal
            else:
                dist = modal - crisp_rating

            if dist <= 1:
                closest_mf = mf_l
                break

        return self.criteria_rating_mfs[closest_mf]

