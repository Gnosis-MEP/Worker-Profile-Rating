from worker_profile_rating.rating_modules.base import RatingModuleBase

class RatingModuleFuzzy(RatingModuleBase):
    def __init__(self, qos_criteria, default_criteria_ranges=None):
        super().__init__(qos_criteria, default_criteria_ranges)
        self.criteria_rating_mfs = {
            'high': (7, 9, 10), # 9, 10
            'medium_high': (5, 7, 9), # 7, 8
            'medium': (3, 5, 7), # 5, 6
            'medium_low': (1, 3, 5), # 3, 4
            'low': (1, 1, 3), # 1, 1, 2 (no 0 to avoid division-by-zero issues)
        }
        self.sorted_mfs_modals = {
            v[1]: k for k, v in
            sorted(self.criteria_rating_mfs.items(), key=lambda dt: dt[1][1])
        }

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


    def get_closest_mf_to_rating_by_modal(self, crisp_rating):
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


    def calculate_worker_criterion_rating_for_service_type(self, service_type, criterion, worker_value):
        """
            closest to modal, similar to:
            Triantaphyllou, Evangelos, and Chi-Tun Lin.
                "Development and evaluation of five fuzzy multiattribute decision-making methods."
                international Journal of Approximate reasoning 14.4 (1996): 281-310.)
        """
        crisp_rating = self.get_criterion_crisp_rating_for_service_type(service_type, criterion, worker_value)
        return self.get_closest_mf_to_rating_by_modal(crisp_rating)
