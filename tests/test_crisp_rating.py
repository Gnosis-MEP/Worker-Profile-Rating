from unittest.mock import patch
from unittest import TestCase


from worker_profile_rating.rating_modules.crisp import RatingModuleCrisp


class TestRatingModuleCrisp(TestCase):

    def setUp(self):
        self.qos_criteria = ['energy_consumption', 'throughput', 'accuracy']
        self.default_criteria_ranges = {
            'service_type': {
                'accuracy': [0.1, 1]
            }
        }
        self.rating = RatingModuleCrisp(qos_criteria=self.qos_criteria, default_criteria_ranges=self.default_criteria_ranges)


    def test_get_criterion_crisp_rating_for_service_type(self):
        self.rating.rating_range = (1, 10)
        service_type = 'service_type'
        criterion = 'accuracy'
        ret1 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 0.1)
        ret2 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 0.5)
        ret3 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 1)
        self.assertEqual(ret1, 1)
        self.assertEqual(ret2, 5)
        self.assertEqual(ret3, 10)

    def test_get_criterion_crisp_rating_for_service_type_if_not_using_scaled_rating(self):
        self.rating.rating_range = (1, 10)
        self.rating.scale_ratings = False
        service_type = 'service_type'
        criterion = 'accuracy'
        ret1 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 0.1)
        ret2 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 0.5)
        ret3 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 1)
        self.assertEqual(ret1, 0.1)
        self.assertEqual(ret2, 0.5)
        self.assertEqual(ret3, 1)