import pytest
import json
import os
import sys
from datetime import datetime
from unittest.mock import patch, mock_open
# Add the parent directory to the Python path
# Add the parent directory to the Python path (go up one level to find tracker.py)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tracker import HabitTracker

@pytest.fixture
def temp_tracker():
    """Create a temporary tracker instance for testing"""
    test_file = 'test_habits.json'
    tracker = HabitTracker(test_file)
    yield tracker
    # Cleanup after test
    if os.path.exists(test_file):
        os.remove(test_file)

@pytest.fixture
def tracker_with_data():
    """Create a tracker with some test data"""
    test_file = 'test_habits_with_data.json'
    tracker = HabitTracker(test_file)
    tracker.add_habit('exercise')
    tracker.add_habit('reading')
    yield tracker
    # Cleanup after test
    if os.path.exists(test_file):
        os.remove(test_file)

class TestHabitTracker:
    def test_init_with_new_file(self, temp_tracker):
        """Test initialization with a new file"""
        assert temp_tracker.file == 'test_habits.json'
        assert temp_tracker.data == {}
    
    def test_init_with_existing_file(self):
        """Test initialization with existing file"""
        test_file = 'test_existing.json'
        test_data = {'exercise': ['2025-07-10'], 'reading': []}
        
        # Create test file
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        tracker = HabitTracker(test_file)
        assert tracker.data == test_data
        os.remove(test_file)
    
    def test_load_data_file_not_found(self, temp_tracker):
        """Test load_data when file doesn't exist"""
        assert temp_tracker.data == {}
    
    def test_save_data(self, temp_tracker):
        """Test save_data functionality"""
        temp_tracker.data = {'test_habit': ['2025-07-10']}
        temp_tracker.save_data()
        
        # Verify file was created and contains correct data
        with open(temp_tracker.file, 'r') as f:
            saved_data = json.load(f)
        assert saved_data == {'test_habit': ['2025-07-10']}
    
    def test_add_habit_new(self, temp_tracker):
        """Test adding a new habit"""
        result = temp_tracker.add_habit('exercise')
        assert result == 'Habit "exercise" added.'
        assert 'exercise' in temp_tracker.data
        assert temp_tracker.data['exercise'] == []
    
    def test_add_habit_existing(self, tracker_with_data):
        """Test adding an existing habit"""
        result = tracker_with_data.add_habit('exercise')
        assert result == 'Habit "exercise" already exists.'
    
    @patch('tracker.datetime')
    def test_mark_as_done_new_date(self, mock_datetime, tracker_with_data):
        """Test marking a habit as done for a new date"""
        mock_datetime.now.return_value.strftime.return_value = '2025-07-10'
        result = tracker_with_data.mark_as_done('exercise')
        assert result == 'Habit "exercise" marked as done for today.'
        assert '2025-07-10' in tracker_with_data.data['exercise']
    
    @patch('tracker.datetime')
    def test_mark_as_done_existing_date(self, mock_datetime, tracker_with_data):
        """Test marking a habit as done when already marked for today"""
        mock_datetime.now.return_value.strftime.return_value = '2025-07-10'
        
        # Mark it first time
        tracker_with_data.mark_as_done('exercise')
        
        # Try to mark again
        result = tracker_with_data.mark_as_done('exercise')
        
        assert result == 'Habit "exercise" already marked as done for today.'
        assert tracker_with_data.data['exercise'].count('2025-07-10') == 1
    
    def test_mark_as_done_nonexistent_habit(self, tracker_with_data):
        """Test marking a non-existent habit as done"""
        result = tracker_with_data.mark_as_done('nonexistent')
        
        assert result == 'Habit "nonexistent" does not exist.'
    
    def test_remove_habit_existing(self, tracker_with_data):
        """Test removing an existing habit"""
        result = tracker_with_data.remove_habit('exercise')
        
        assert result == 'Habit "exercise" removed.'
        assert 'exercise' not in tracker_with_data.data
    
    def test_remove_habit_nonexistent(self, tracker_with_data):
        """Test removing a non-existent habit"""
        result = tracker_with_data.remove_habit('nonexistent')
        
        assert result == 'Habit "nonexistent" does not exist.'
    
    def test_list_habits_empty(self, temp_tracker, capsys):
        """Test listing habits when no habits exist"""
        temp_tracker.list_habits()
        captured = capsys.readouterr()
        assert captured.out.strip() == 'No habits found.'
    
    def test_list_habits_with_data(self, tracker_with_data, capsys):
        """Test listing habits when habits exist"""
        tracker_with_data.list_habits()
        captured = capsys.readouterr()
        output_lines = captured.out.strip().split('\n')
        assert '- exercise' in output_lines
        assert '- reading' in output_lines
    
    def test_data_persistence(self, temp_tracker):
        """Test that data persists between instances"""
        # Add habit and mark as done
        temp_tracker.add_habit('test_habit')
        with patch('tracker.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2025-07-10'
            temp_tracker.mark_as_done('test_habit')
        # Create new instance with same file
        new_tracker = HabitTracker(temp_tracker.file)
        assert 'test_habit' in new_tracker.data
        assert '2025-07-10' in new_tracker.data['test_habit']
    
    def test_file_operations_error_handling(self):
        """Test error handling for file operations"""
        # Test with invalid file path (read-only directory on Windows)
        with pytest.raises(PermissionError):
            invalid_tracker = HabitTracker('C:\\Windows\\test.json')
            invalid_tracker.data = {'test': []}
            invalid_tracker.save_data()


class TestEdgeCases:
    def test_empty_habit_name(self, temp_tracker):
        """Test adding empty habit name"""
        result = temp_tracker.add_habit('')
        assert result == 'Habit "" added.'
        assert '' in temp_tracker.data
    
    def test_special_characters_in_habit_name(self, temp_tracker):
        """Test habit names with special characters"""
        special_habit = 'drink 💧 water!'
        result = temp_tracker.add_habit(special_habit)
        assert result == f'Habit "{special_habit}" added.'
        assert special_habit in temp_tracker.data
    
    def test_very_long_habit_name(self, temp_tracker):
        """Test very long habit names"""
        long_habit = 'a' * 1000
        result = temp_tracker.add_habit(long_habit)
        assert result == f'Habit "{long_habit}" added.'
        assert long_habit in temp_tracker.data
    
    @patch('tracker.datetime')
    def test_multiple_dates_same_habit(self, mock_datetime, temp_tracker):
        """Test marking same habit on multiple dates"""
        temp_tracker.add_habit('daily_habit')
        dates = ['2025-07-08', '2025-07-09', '2025-07-10']
        for date in dates:
            mock_datetime.now.return_value.strftime.return_value = date
            temp_tracker.mark_as_done('daily_habit')
        assert temp_tracker.data['daily_habit'] == dates


# Integration tests
class TestIntegration:
    def test_complete_habit_lifecycle(self, temp_tracker):
        """Test complete lifecycle of a habit"""
        # Add habit
        add_result = temp_tracker.add_habit('morning_run')
        assert add_result == 'Habit "morning_run" added.'
        
        # Mark as done
        with patch('tracker.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = '2025-07-10'
            mark_result = temp_tracker.mark_as_done('morning_run')
            assert mark_result == 'Habit "morning_run" marked as done for today.'
        # Verify data
        assert '2025-07-10' in temp_tracker.data['morning_run']
        # Remove habit
        remove_result = temp_tracker.remove_habit('morning_run')
        assert remove_result == 'Habit "morning_run" removed.'
        assert 'morning_run' not in temp_tracker.data

if __name__ == '__main__':
    pytest.main([__file__])