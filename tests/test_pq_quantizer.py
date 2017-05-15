import unittest

import numpy as np

from quantization.pq_quantizer import PQQuantizer


class PQQuantizerTest(unittest.TestCase):
    X = None
    quantizer = None

    @classmethod
    def setUpClass(cls):
        cls.X = np.array([
            [0, 2, 4, 2],
            [0, 3, 4, 2],
            [1, 3, 5, 1],
            [1, 3, 6, 0]
        ])
        cls.quantizer = PQQuantizer(2, 2)
        cls.quantizer.fit(cls.X)

    def test_predict_shape(self):
        predicted_base_vectors = PQQuantizerTest.quantizer.predict(PQQuantizerTest.X)
        predicted_base_vectors_shape = predicted_base_vectors.shape
        truth_shape = (4, 2)
        self.assertEquals(predicted_base_vectors_shape, truth_shape)

    def test_clusters_shape(self):
        cluster_centers = PQQuantizerTest.quantizer.get_cluster_centers()
        cluster_centers_shape = cluster_centers.shape
        truth_shape = (2, 2, 2)
        self.assertEquals(cluster_centers_shape, truth_shape)


if __name__ == '__main__':
    unittest.main()