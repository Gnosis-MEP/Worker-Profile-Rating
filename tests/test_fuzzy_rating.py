from unittest.mock import patch
from unittest import TestCase


from worker_profile_rating.rating_modules.fuzzy import RatingModuleFuzzy


class TestRatingModuleFuzzy(TestCase):

    def setUp(self):
        self.qos_criteria = ['energy_consumption', 'throughput', 'accuracy']
        self.default_criteria_ranges = {
            'service_type': {
                'accuracy': [0.1, 1]
            }
        }
        self.rating = RatingModuleFuzzy(qos_criteria=self.qos_criteria, default_criteria_ranges=self.default_criteria_ranges)


    def test_get_criterion_crisp_rating_for_service_type(self):
        self.rating.rating_range = (1, 10)
        service_type = 'service_type'
        criterion = 'accuracy'
        ret1 = self.rating.get_criterion_crisp_rating_for_service_type(service_type, criterion, 0.1)
        ret2 = self.rating.get_criterion_crisp_rating_for_service_type(service_type, criterion, 0.5)
        ret3 = self.rating.get_criterion_crisp_rating_for_service_type(service_type, criterion, 1)
        self.assertEqual(ret1, 1)
        self.assertEqual(ret2, 5)
        self.assertEqual(ret3, 10)

    def test_calculate_worker_criterion_rating_for_service_type(self):

        self.rating.rating_range = (1, 10)
        service_type = 'service_type'
        criterion = 'accuracy'
        ret1 = self.rating.calculate_worker_criterion_rating_for_service_type(service_type, criterion, 0.5)
        self.assertListEqual(list(ret1), list(self.rating.criteria_rating_mfs['medium']))


    def test_get_closest_mf_to_rating_by_modal(self):
        ret1 = self.rating.get_closest_mf_to_rating_by_modal(1)
        self.assertEqual(ret1, self.rating.criteria_rating_mfs['low'])
        ret2 = self.rating.get_closest_mf_to_rating_by_modal(2)
        self.assertEqual(ret2, self.rating.criteria_rating_mfs['low'])
        ret3 = self.rating.get_closest_mf_to_rating_by_modal(3)
        self.assertEqual(ret3, self.rating.criteria_rating_mfs['medium_low'])
        ret4 = self.rating.get_closest_mf_to_rating_by_modal(4)
        self.assertEqual(ret4, self.rating.criteria_rating_mfs['medium_low'])
        ret5 = self.rating.get_closest_mf_to_rating_by_modal(5)
        self.assertEqual(ret5, self.rating.criteria_rating_mfs['medium'])
        ret6 = self.rating.get_closest_mf_to_rating_by_modal(6)
        self.assertEqual(ret6, self.rating.criteria_rating_mfs['medium'])
        ret7 = self.rating.get_closest_mf_to_rating_by_modal(7)
        self.assertEqual(ret7, self.rating.criteria_rating_mfs['medium_high'])
        ret8 = self.rating.get_closest_mf_to_rating_by_modal(8)
        self.assertEqual(ret8, self.rating.criteria_rating_mfs['medium_high'])
        ret9 = self.rating.get_closest_mf_to_rating_by_modal(9)
        self.assertEqual(ret9, self.rating.criteria_rating_mfs['high'])
        ret10 = self.rating.get_closest_mf_to_rating_by_modal(10)
        self.assertEqual(ret10, self.rating.criteria_rating_mfs['high'])