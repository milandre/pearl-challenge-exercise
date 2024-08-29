import pytest

from app.main import home_buyers_to_neighborhoods


class TestHomeBuyersToNeighborhoods:

    # Assign home buyers to neighborhoods based on fit scores and priorities
    def test_assign_home_buyers_based_on_fit_scores_and_priorities(self) -> None:
        home_buyers = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        neighborhoods = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        priorities = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        expected_assignments = {0: [(1, 0)], 1: [(5, 1)], 2: [(9, 2)]}
        assignments = home_buyers_to_neighborhoods(
            home_buyers, neighborhoods, priorities
        )
        assert assignments == expected_assignments
