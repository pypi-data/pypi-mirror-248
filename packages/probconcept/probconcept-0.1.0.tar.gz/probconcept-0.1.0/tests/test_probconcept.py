import unittest

import numpy as np
import pandas as pd

from probconcept.probconcept import ProbConceptFit, insert_row_in_dataframe


class TestProbConceptFit(unittest.TestCase):
    def setUp(self):
        # Set up any common data or configurations for your tests
        self.depths = np.array(
            [2.21, 1.91, 1.61, 1.31, 1.01, 0.81, 0.61, 0.41, 0.31, 0.21, 0.11, 0.06]
        )
        self.velocities = np.array(
            [37.51, 37.55, 37.64, 37.51, 36.76, 35.9, 35.02, 32.43, 29.94, 26.6, 22.33, 14.45]
        )
        self.uncertainties = np.ones(12) * 0.01
        self.max_depth = 2.31
        self.h = 0.58
        self.max_velocity = 37.64

    def tearDown(self):
        # Clean up after each test
        pass

    def test_insert_row_in_dataframe(self):
        # Test the insert_row_in_dataframe function

        # Create a sample dataframe
        original_df = pd.DataFrame(
            {"name": ["A", "B", "C"], "value": [1, 2, 3], "vary": [True, False, True]}
        )

        # Insert a new row at index 1
        new_row = ["D", 4, False]
        new_df = insert_row_in_dataframe(1, original_df, new_row)

        # Check if the row is inserted correctly
        self.assertEqual(new_df.loc[1, "name"], "D")
        self.assertEqual(new_df.loc[1, "value"], 4)
        self.assertEqual(new_df.loc[1, "vary"], False)

    def test_populate_velocity_profile_data(self):
        # Test the populate_velocity_profile_data method

        # Create an instance of ProbConceptFit
        prob_fit = ProbConceptFit()

        # Call the method
        prob_fit.populate_velocity_profile_data(
            depths=self.depths,
            velocities=self.velocities,
            uncertainties=self.uncertainties,
            max_depth=self.max_depth,
            h=self.h,
            max_velocity=self.max_velocity,
            use_uncertainty=True,
        )

        # Add assertions based on expected behavior

    def test_compute_fit(self):
        # Test the compute_fit method

        # Create an instance of ProbConceptFit
        prob_fit = ProbConceptFit()

        # Call the method
        prob_fit.populate_velocity_profile_data(
            depths=self.depths,
            velocities=self.velocities,
            uncertainties=self.uncertainties,
            max_depth=self.max_depth,
            h=self.h,
            max_velocity=self.max_velocity,
            use_uncertainty=True,
        )

        # Call the method
        prob_fit.compute_fit()

        # Add assertions based on expected behavior
        known_phi = 0.764
        self.assertAlmostEqual(prob_fit.phi, known_phi, 2)

    # Add more test methods for other functionalities of your class


if __name__ == "__main__":
    unittest.main()
