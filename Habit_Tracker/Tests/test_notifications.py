import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the parent directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from notifications import HabitNotifications

class TestHabitNotifications(unittest.TestCase):
    @patch('notifications.HabitTracker')
    def setUp(self, MockHabitTracker):
        """Set up a mock HabitTracker instance."""
        self.mock_tracker = MockHabitTracker.return_value
        self.mock_tracker.data = {
            "Exercise": ["2023-10-01"],
            "Read": ["2023-10-01"]
        }
        self.notifier = HabitNotifications()
        self.notifier.tracker = self.mock_tracker

    @patch('notifications.notification.notify')
    def test_send_notification(self, mock_notify):
        """Test send_notification method."""
        habit_name = "Exercise"
        self.notifier.send_notification(habit_name)
        mock_notify.assert_called_once_with(
            title="🔔 Habit Reminder",
            message=f"Time to {habit_name}! Keep your streak going!",
            app_name="Habit Tracker",
            timeout=10
        )

    @patch('notifications.HabitNotifications.send_notification')
    def test_check_habit_status_not_completed(self, mock_send_notification):
        """Test check_habit_status when habit is not completed today."""
        habit_name = "Read"
        today = datetime.now().strftime('%Y-%m-%d')
        self.mock_tracker.data[habit_name] = []  # Simulate no completion today
        self.notifier.check_habit_status(habit_name)
        mock_send_notification.assert_called_once_with(habit_name)

    def test_check_habit_status_completed(self):
        """Test check_habit_status when habit is completed today."""
        habit_name = "Exercise"
        today = datetime.now().strftime('%Y-%m-%d')
        self.mock_tracker.data[habit_name] = [today]  # Simulate completion today
        with patch('builtins.print') as mock_print:
            self.notifier.check_habit_status(habit_name)
            mock_print.assert_called_with(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {habit_name} already completed")

    def test_check_habit_status_habit_not_found(self):
        """Test check_habit_status when habit is not found."""
        habit_name = "Meditate"
        with patch('builtins.print') as mock_print:
            self.notifier.check_habit_status(habit_name)
            mock_print.assert_called_with(f"[{datetime.now().strftime('%H:%M:%S')}] Habit '{habit_name}' not found")

    @patch('notifications.schedule.every')
    def test_schedule_habit_reminders(self, mock_schedule_every):
        """Test schedule_habit_reminders method."""
        mock_job = MagicMock()
        mock_schedule_every.return_value.hours.do.return_value = mock_job
        
        result = self.notifier.schedule_habit_reminders()
        self.assertTrue(result)

    @patch('builtins.print')
    def test_schedule_habit_reminders_no_habits(self, mock_print):
        """Test schedule_habit_reminders when no habits exist."""
        self.mock_tracker.data = {}  # Simulate no habits
        result = self.notifier.schedule_habit_reminders()
        self.assertFalse(result)
        # Updated to match the actual message in your code
        mock_print.assert_called_with("❌ No habits found to schedule reminders")

    @patch('notifications.schedule.run_pending')
    @patch('notifications.time.sleep', side_effect=KeyboardInterrupt)
    def test_run_scheduler(self, mock_sleep, mock_run_pending):
        """Test run_scheduler method."""
        with patch('builtins.print') as mock_print:
            self.notifier.run_scheduler()
            mock_print.assert_any_call("\n👋 Stopping Habit Tracker Notifications")

if __name__ == '__main__':
    unittest.main()