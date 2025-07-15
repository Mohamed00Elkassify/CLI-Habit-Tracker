import time
import schedule
import threading
from plyer import notification
from datetime import datetime
from tracker import HabitTracker

class HabitNotifications:
    def __init__(self, data_file='habits.json'):
        self.tracker = HabitTracker(data_file)
        self.running = False
    
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
        # Reload data to get latest updates
        self.tracker.load_data()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if habit_name in self.tracker.data:
            if today not in self.tracker.data[habit_name]:
                # Not done today - send notification
                self.send_notification(habit_name)
                print(f"[{datetime.now().strftime('%H:%M:%S')}] {habit_name} not completed today")
            else:
                # Already done today - skip notification
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ {habit_name} already completed - skipping notification")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Habit '{habit_name}' not found")
    
    def schedule_habit_reminders(self):
        """Schedule reminders for all habits every 2 hours."""
        scheduled_count = 0
        
        for habit_name in self.tracker.data.keys():
            schedule.every(2).hours.do(self.check_habit_status, habit_name)
            print(f"📅 Scheduled '{habit_name}' reminder every 2 hours")
            scheduled_count += 1
        
        if scheduled_count == 0:
            print("❌ No habits found to schedule reminders")
            return False
        return True
    
    def run_scheduler(self):
        """Run scheduler in background - user can close terminal."""
        print("\n✅ Starting background notifications...")
        print("🔔 You will get desktop notifications every 2 hours")
        print("🛑 Only incomplete habits will send notifications")
        
        self.running = True
        
        # Background worker function
        def background_worker():
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        
        # Start background thread
        thread = threading.Thread(target=background_worker)
        thread.daemon = True  # Dies when main program dies
        thread.start()
        
        try:
            # Keep main program alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Stopping notifications...")
            self.running = False

def main():
    """Simple entry point - always runs in background."""
    print("🚀 Habit Tracker Notifications")
    
    notifier = HabitNotifications('habits.json')
    
    if not notifier.tracker.data:
        print("❌ No habits found. Add some habits first!")
        return
    
    print(f"📊 Found {len(notifier.tracker.data)} habits")
    
    # Show what will be scheduled
    print("\n📋 Will send notifications for:")
    for habit in notifier.tracker.data.keys():
        print(f"   - {habit}")
    
    # Schedule and run in background
    if notifier.schedule_habit_reminders():
        notifier.run_scheduler()

if __name__ == "__main__":
    main()
