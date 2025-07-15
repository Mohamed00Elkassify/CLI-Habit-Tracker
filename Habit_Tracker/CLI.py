# Main CLI entry 
import argparse
from tracker import HabitTracker
from visualization import show_calendar, show_streak
from notifications import HabitNotifications
from rich.console import Console

console = Console()

print("""
===============================
🌟 Welcome to the CLI Habit Tracker! 🌟
Track your habits and stay motivated!
===============================
""")

def main():
    parser = argparse.ArgumentParser(description="CLI Habit Tracker")
    parser.add_argument("command", choices=["add", "done", "remove", "list", "calendar", "streak", "notify", "stats"])
    parser.add_argument("--name", help="Habit name")

    args = parser.parse_args()

    # Initialize tracker and notifier
    tracker = HabitTracker('habits.json')
    notifier = HabitNotifications('habits.json')

    if args.command == "add" and args.name:
        result = tracker.add_habit(args.name)
        console.print(f"[green]{result}[/green]")
    
    elif args.command == "done" and args.name:
        result = tracker.mark_as_done(args.name)
        if "marked as done" in result:
            console.print(f"[green]✅ {result}[/green]")
        else:
            console.print(f"[yellow]{result}[/yellow]")
    
    elif args.command == "remove" and args.name:
        result = tracker.remove_habit(args.name)
        console.print(f"[red]{result}[/red]")
    
    elif args.command == "list":
        tracker.list_habits()
    
    elif args.command == "calendar" and args.name:
        show_calendar(args.name)
    
    elif args.command == "streak" and args.name:
        show_streak(args.name)
    
    elif args.command == "notify":
        console.print("[bold green]🚀 Starting Habit Notifications...[/bold green]")
        if notifier.schedule_habit_reminders():
            notifier.run_scheduler()
        else:
            console.print("[red]❌ No notifications to schedule[/red]")
    
    elif args.command == "stats":
        # Show basic stats
        if not tracker.data:
            console.print("[yellow]No habits found.[/yellow]")
        else:
            console.print(f"\n[bold blue]📊 You have {len(tracker.data)} habits:[/bold blue]")
            for habit in tracker.data:
                total = len(tracker.data[habit])
                console.print(f"  • {habit}: {total} completions")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()