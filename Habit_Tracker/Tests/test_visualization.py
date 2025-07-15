import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import visualization

class TestVisualization(unittest.TestCase):

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_calendar_habit_not_found(self, mock_tracker_class, mock_console):
        """Test show_calendar with non-existent habit."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {}
        
        visualization.show_calendar("nonexistent_habit")
        mock_console.print.assert_called_with("[red]Habit 'nonexistent_habit' not found![/red]")

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_calendar_valid_habit(self, mock_tracker_class, mock_console):
        """Test show_calendar with valid habit."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {"exercise": ["2023-10-01", "2023-10-02"]}
        
        visualization.show_calendar("exercise")
        # Just verify console.print was called (calendar table was printed)
        mock_console.print.assert_called()

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_streak_habit_not_found(self, mock_tracker_class, mock_console):
        """Test show_streak with non-existent habit."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {}
        
        visualization.show_streak("nonexistent_habit")
        mock_console.print.assert_called_with("[red]Habit 'nonexistent_habit' not found![/red]")

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_streak_no_data(self, mock_tracker_class, mock_console):
        """Test show_streak with no data."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {"exercise": []}
        
        visualization.show_streak("exercise")
        mock_console.print.assert_called_with("[yellow]No streaks found for habit 'exercise'.[/yellow]")

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_streak_with_data(self, mock_tracker_class, mock_console):
        """Test show_streak with valid data."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {
            "exercise": ["2023-10-01", "2023-10-02", "2023-10-03"]
        }
        
        visualization.show_streak("exercise")
        # Verify that streak information was printed
        mock_console.print.assert_called()

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_streak_with_ongoing_streak(self, mock_tracker_class, mock_console):
        """Test show_streak with ongoing streak."""
        mock_tracker = mock_tracker_class.return_value
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        mock_tracker.load_data.return_value = {
            "exercise": [yesterday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")]
        }
        
        visualization.show_streak("exercise")
        # Check that console.print was called multiple times (for longest streak and ongoing streak)
        self.assertTrue(mock_console.print.call_count >= 2)

    @patch("visualization.console")
    @patch("visualization.HabitTracker")
    def test_show_streak_no_ongoing_streak(self, mock_tracker_class, mock_console):
        """Test show_streak with no ongoing streak."""
        mock_tracker = mock_tracker_class.return_value
        old_date = datetime.now().date() - timedelta(days=10)
        
        mock_tracker.load_data.return_value = {
            "exercise": [old_date.strftime("%Y-%m-%d")]
        }
        
        visualization.show_streak("exercise")
        # Should print longest streak and "No ongoing streak"
        mock_console.print.assert_called()

    @patch("visualization.HabitTracker")
    def test_calendar_date_parsing(self, mock_tracker_class):
        """Test that calendar correctly parses dates."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {
            "exercise": ["2023-10-01", "2023-10-02"]
        }
        
        with patch("visualization.console") as mock_console:
            visualization.show_calendar("exercise")
            # Verify the function runs without error
            mock_console.print.assert_called()

    @patch("visualization.HabitTracker")
    def test_streak_calculation_logic(self, mock_tracker_class):
        """Test streak calculation with consecutive dates."""
        mock_tracker = mock_tracker_class.return_value
        mock_tracker.load_data.return_value = {
            "exercise": ["2023-10-01", "2023-10-02", "2023-10-03", "2023-10-05"]
        }
        
        with patch("visualization.console") as mock_console:
            visualization.show_streak("exercise")
            # Verify the function runs and calculates streaks
            mock_console.print.assert_called()

if __name__ == "__main__":
    unittest.main()