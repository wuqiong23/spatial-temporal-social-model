import datetimeimport numpy as npimport unittestfrom mocker import Mockerfrom Models import Model, StanfordModelfrom Utils import Utilsclass TestModel(unittest.TestCase):    def setUp(self):        self.model = Model()    def test_produce_initial_check_in_assignment_correct_clustering(self):        check_ins = [                {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 37.6164, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': -122.386, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},                {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 50.6164, 'check_in_message': 'empty_message', 'check_in_id': '14', 'longitude': 122.386, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},                {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 51, 'check_in_message': 'empty_message', 'check_in_id': '15', 'longitude': 120.386, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},                {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 35, 'check_in_message': 'empty_message', 'check_in_id': '13', 'longitude': -120.386, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)}        ]        cluster1, cluster2 = self.model.produce_initial_check_in_assignment(check_ins)        expected_cluster1 = [{'venue_id': '41059b00f964a520850b1fe3', 'date': datetime.datetime(2012, 7, 18, 14, 43, 38), 'longitude': 122.386, 'check_in_id': '14', 'check_in_message': 'empty_message', 'latitude': 50.6164}, {'venue_id': '41059b00f964a520850b1fe3', 'date': datetime.datetime(2012, 7, 18, 14, 43, 38), 'longitude': 120.386, 'check_in_id': '15', 'check_in_message': 'empty_message', 'latitude': 51}]        expected_cluster2 = [{'venue_id': '41059b00f964a520850b1fe3', 'date': datetime.datetime(2012, 7, 18, 14, 43, 38), 'longitude': -122.386, 'check_in_id': '12', 'check_in_message': 'empty_message', 'latitude': 37.6164}, {'venue_id': '41059b00f964a520850b1fe3', 'date': datetime.datetime(2012, 7, 18, 14, 43, 38), 'longitude': -120.386, 'check_in_id': '13', 'check_in_message': 'empty_message', 'latitude': 35}]        self.assertTrue((cluster1 == expected_cluster1 and cluster2 == expected_cluster2) or (cluster1 == expected_cluster2 and cluster2 == expected_cluster1))            def test_produce_max_likelihood_estimates_lists_invalid(self):        with self.assertRaises(ValueError) as cm:            self.model.produce_max_likelihood_estimates(None, [1, 2])        self.assertEqual(cm.exception.message, "First argument has to be a list!")        with self.assertRaises(ValueError) as cm:            self.model.produce_max_likelihood_estimates([1, 2], None)        self.assertEqual(cm.exception.message, "Second argument has to be a list!")    def test_produce_max_likelihood_estimates_lists_empty(self):        with self.assertRaises(ValueError) as cm:            self.model.produce_max_likelihood_estimates([], [1, 2])        self.assertEqual(cm.exception.message, "First list has to contain at least one check-in!")        with self.assertRaises(ValueError) as cm:            self.model.produce_max_likelihood_estimates([1, 2], [])        self.assertEqual(cm.exception.message, "Second list has to contain at least one check-in!")    def test_hours_from_midnight_happy_path(self):        self.assertAlmostEqual(14.717, self.model.hours_from_midnight(datetime.datetime(2012, 7, 18, 14, 43, 38)), 3)    def test_hours_from_midnight_invalid_timestamp(self):        with self.assertRaises(ValueError) as cm:            self.model.hours_from_midnight(1.2)        self.assertEqual(cm.exception.message, "Timestamp should be an instance of datetime.datetime!")    def test_calculate_circular_mean_happy_path(self):        self.assertAlmostEqual(0.5, self.model.calculate_circular_mean([22, 3]), 2)    def test_calculate_circular_mean_invalid_numbers(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_circular_mean([22, "3a"])        self.assertEqual(cm.exception.message, "3a is not a number!")    def test_calculate_circular_SD_happy_path(self):        self.assertAlmostEqual(1.74, self.model.calculate_circular_SD([22, 3]), 2)    def test_calculate_circular_SD_invalid_numbers(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_circular_SD([22, "3a"])        self.assertEqual(cm.exception.message, "3a is not a number!")    def test_calculate_covariation_matrix_happy_path(self):        H = [            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 56, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': 120, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 52, 'check_in_message': 'empty_message', 'check_in_id': '14', 'longitude': 122, 'date': datetime.datetime(2012, 7, 18, 16, 43, 38)},        ]        self.assertEqual(self.model.calculate_covariation_matrix(H)[0][0], 8)        self.assertEqual(self.model.calculate_covariation_matrix(H)[0][1], -4)        self.assertEqual(self.model.calculate_covariation_matrix(H)[1][0], -4)        self.assertEqual(self.model.calculate_covariation_matrix(H)[1][1], 2)    def test_calculate_covariation_matrix_duplicate_ids(self):        H = [            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 56, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': 120, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 52, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': 122, 'date': datetime.datetime(2012, 7, 18, 16, 43, 38)},        ]        with self.assertRaises(ValueError) as cm:            self.model.calculate_covariation_matrix(H)        self.assertEqual(cm.exception.message, "Error: some check-ins have same IDs!")    def test_calculate_N_happy_path(self):        self.assertAlmostEqual(0.042, self.model.calculate_N(12, 0.45, 3, 2), 3)    def test_calculate_N_invalid_time(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_N(25, 0.45, 3, 2)        self.assertEqual(cm.exception.message, "Error: t_hours should be in the [0, 24] interval!")    def test_calculate_N_invalid_proportion(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_N(17, 1.23, 3, 2)        self.assertEqual(cm.exception.message, "Error: Pc should be in the [0, 1] interval!")    def test_calculate_N_invalid_sigma(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_N(17, 0.7, 25, 2)        self.assertEqual(cm.exception.message, "Error: sigma should be in the [0, 24] interval!")    def test_calculate_N_invalid_tau(self):        with self.assertRaises(ValueError) as cm:            self.model.calculate_N(17, 0.7, 2, 25)        self.assertEqual(cm.exception.message, "Error: tau should be in the [0, 24] interval!")    def test_calculate_temporal_probabilities_happy_path(self):        t = 15        self.model.parameters = {"tau_h": 22, "tau_w": 14, "sigma_h": 1, "sigma_w": 1, "Pc_h": 0.5, "Pc_w": 0.5}        home_p, work_p = self.model.calculate_temporal_probabilities(t)        self.assertAlmostEqual(home_p + work_p, 1, 1)        self.assertTrue(home_p < work_p)   class TestStanfordModel(unittest.TestCase):    def setUp(self):        self.model = StanfordModel()    def test_produce_max_likelihood_estimates_happy_path(self):        H = [            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 60, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': 220, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)},            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 42, 'check_in_message': 'empty_message', 'check_in_id': '14', 'longitude': 22, 'date': datetime.datetime(2012, 7, 18, 16, 43, 38)},        ]        W = [            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 40, 'check_in_message': 'empty_message', 'check_in_id': '15', 'longitude': 160, 'date': datetime.datetime(2012, 7, 18, 02, 43, 38)},            {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 42, 'check_in_message': 'empty_message', 'check_in_id': '13', 'longitude': 142, 'date': datetime.datetime(2012, 7, 18, 22, 43, 38)}        ]        results = self.model.produce_max_likelihood_estimates(H, W)        self.assertAlmostEqual(results["tau_h"], 15.717, 2)        self.assertAlmostEqual(results["tau_w"], 0.717, 2)        self.assertAlmostEqual(results["sigma_h"], 0.71, 2)        self.assertAlmostEqual(results["sigma_w"], 1.4, 2)        self.assertEqual(results["mju_w"], [41.0, 151.0])        self.assertEqual(results["mju_h"], [51.0, 121.0])        self.assertTrue((results["Sigma_h"] == np.array([[162., 1782.], [1782., 19602.]])).all())        self.assertTrue((results["Sigma_w"] == np.array([[2., -18.], [-18., 162.]])).all())    def test_probability_multivariate_normal_happy_path(self):        latitude = 12        longitude = 13        mju = [10, 11]        Sigma = np.array([[1, 0.5], [0.5, 1]])        result = self.model.probability_multivariate_normal([latitude, longitude], mju, Sigma)        self.assertAlmostEqual(result, 0.002, 3)    def test_calculate_spatial_probabilities_happy_path(self):        latitude = 12        longitude = 13        self.model.parameters = {"mju_h": [12, 13], "mju_w": [100, 101], "Sigma_h": np.array([[1, 0.5], [0.5, 1]]), "Sigma_w": np.array([[1, 0.5], [0.5, 1]])}        home, work = self.model.calculate_spatial_probabilities(latitude, longitude)        self.assertTrue(home > work)    def test_aggregated_probability_happy_path(self):        check_in = {'venue_id': '41059b00f964a520850b1fe3', 'latitude': 10, 'check_in_message': 'empty_message', 'check_in_id': '12', 'longitude': 11, 'date': datetime.datetime(2012, 7, 18, 14, 43, 38)}        self.model.P_temporal_H = {}        self.model.P_temporal_W = {}        self.model.P_spatial_H = {}        self.model.P_spatial_W = {}        id = check_in["check_in_id"]        self.model.P_temporal_H[id] = 0.1        self.model.P_temporal_W[id] = 0.2        self.model.P_spatial_H[id] = 0.5        self.model.P_spatial_W[id] = 0.6        home, work = self.model.aggregated_probability(check_in)        self.assertAlmostEqual(home, 0.05, 2)        self.assertAlmostEqual(work, 0.12, 2)    def test_get_average_venue_coordinates_happy_path(self):        check_ins = [            {"venue_id": "A", "latitude": 20, "longitude": 130},            {"venue_id": "A", "latitude": 22, "longitude": 32},            {"venue_id": "A", "latitude": 120, "longitude": 30},            {"venue_id": "B", "latitude": 20, "longitude": 130},            {"venue_id": "B", "latitude": 120, "longitude": 1130},            {"venue_id": "B", "latitude": 222, "longitude": 32}        ]        expected = {'A': {'latitude': 22.0, 'longitude': 32.0}, 'B': {'latitude': 120.0, 'longitude': 130.0}}        self.assertDictEqual(self.model._get_average_venue_coordinates(check_ins), expected)if __name__ == '__main__':    unittest.main()