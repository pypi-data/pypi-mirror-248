import unittest

import sketching.bezier_util


class BezierUtil(unittest.TestCase):

    def test_make_bezier(self):
        input_points = [
            [10, 20],
            [30, 20],
            [80, 70],
            [100, 70]
        ]

        output_points_gen = sketching.bezier_util.make_bezier(input_points)
        output_points = output_points_gen([0, 1])
        
        self.assertEqual(output_points[0][0], 10)
        self.assertEqual(output_points[0][1], 20)
        self.assertEqual(output_points[1][0], 100)
        self.assertEqual(output_points[1][1], 70)
