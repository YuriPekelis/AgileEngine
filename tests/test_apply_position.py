import pytest

from pages.home_page import HomePage
from tests.testrunner import TestRunner


class TestApplyPositions(TestRunner):

    def test_apply_position_field_check(self, browser):
        filters = {
            'Specialization': 'AQA',
            'Location': 'Ukraine',
        }
        speciality = 'Automation QA'
        open_position_page = HomePage(browser). \
            open_page(). \
            go_to_career(). \
            search_career(speciality). \
            filter_found_positions(filters)
        positions_title = open_position_page. \
            get_all_positions_title()
        assert len(positions_title) > 0, f"No found positions with {speciality} seed"
        assert all([speciality in position_title for position_title in positions_title]), \
            f"Some positions title after searching {speciality} does not content {speciality}. List of found titles: " \
            f"{positions_title}"
        position_page = open_position_page. \
            choose_random_position()
        apply_position_visibility = position_page. \
            open_apply_sidebar(). \
            get_apply_position_flds_visibility()
        assert all(apply_position_visibility.values()), \
            f"Some fields are not shown on the position page, fields visibility state: {apply_position_visibility}"


if __name__ == "__main__":
    pytest.main(["-q", "test_apply_position.py"])
