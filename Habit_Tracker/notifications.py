import time
import schedule
from plyer import notification
from datetime import datetime
from tracker import HabitTracker

class HabitNotifications:
    def __init__(self, data_file='habits.json'):
        self.tracker = HabitTracker(data_file)
    
    def send_notification(self, habit_name):
        """Send a desktop notification for the given habit."""
        notification.notify(
            title=f"🔔 Habit Reminder",
            message=f"Time to {habit_name}! Keep your streak going!",
            app_name="Habit Tracker",
            timeout=10
        ) # type: ignore
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Notification sent for: {habit_name}")
    
    def check_habit_status(self, habit_name):
        """Check if habit is done today and send notification if not."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Get habit records from tracker
        if habit_name in self.tracker.data:
            if today not in self.tracker.data[habit_name]:
                self.send_notification(habit_name)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {habit_name} not completed today")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {habit_name} already completed")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Habit '{habit_name}' not found")
    
    def schedule_habit_reminders(self):
        """Schedule reminders for all habits every 2 hours."""
        scheduled_count = 0
        
        for habit_name in self.tracker.data.keys():
            # Schedule notifications every 2 hours for each habit
            schedule.every(2).hours.do(self.check_habit_status, habit_name)
            print(f"📅 Scheduled '{habit_name}' reminder every 2 hours")
            scheduled_count += 1
        
        if scheduled_count == 0:
            print("❌ No habits found to schedule reminders")
            return False
        return True
    
    def run_scheduler(self):
        """Run the scheduler in a loop."""
        print("\n🔄 Scheduler running... (Press Ctrl+C to stop)")
        print("Current scheduled jobs:")
        for job in schedule.jobs:
            print(f"   - {job}")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute instead of every second
        except KeyboardInterrupt:
            print("\n👋 Stopping Habit Tracker Notifications")
    
    def list_notifications(self):
        """List all scheduled notifications."""
        print("\n📋 Current Notification Schedule:")
        for habit in self.tracker.data.keys():
            print(f"   - {habit}: Every 2 hours")

def main():
    """Entry point for the Habit Tracker Notifications System."""
    print("🚀 Habit Tracker Notifications System")
    
    # Initialize with existing habits
    notifier = HabitNotifications('habits.json')
    
    # Check if there are any habits
    if not notifier.tracker.data:
        print("❌ No habits found. Please add habits using the Habit Tracker.")
        return
    
    print(f"📊 Loaded {len(notifier.tracker.data)} habits")
    notifier.list_notifications()
    
    # Schedule reminders
    if notifier.schedule_habit_reminders():
        notifier.run_scheduler()
    else:
        print("No notifications to schedule. Exiting.")

if __name__ == "__main__":
    main()
