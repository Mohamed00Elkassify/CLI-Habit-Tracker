# Calendar and Streak 
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from tracker import HabitTracker

console = Console()

def show_calendar(habit):
    tracker = HabitTracker('habits.json')  # Add the same file path used in CLI
    data = tracker.data
    
    if habit not in data:
        console.print(f"[red]Habit '{habit}' not found![/red]")
        return

    dates = [datetime.strptime(d, "%Y-%m-%d").date() for d in data[habit]]
    today = datetime.today().date()
    start_day = today.replace(day=1)
    table = Table(title=f"{habit} - {today.strftime('%B %Y')}", show_lines=True)
    table.add_column("Mon")
    table.add_column("Tue")
    table.add_column("Wed")
    table.add_column("Thu")
    table.add_column("Fri")
    table.add_column("Sat")
    table.add_column("Sun")

    week = []
    for i in range(start_day.weekday()):
        week.append("")

    for i in range(31):
        try:
            day = start_day + timedelta(days=i)
            if day.month != today.month:
                break
            symbol = "✅" if day in dates else str(day.day)
            week.append(symbol)
            if len(week) == 7:
                table.add_row(*week)
                week = []
        except:
            break
    if week:
        while len(week) < 7:
            week.append("")
        table.add_row(*week)

    console.print(table)

def show_streak(habit):
    tracker = HabitTracker('habits.json')  # Add the same file path used in CLI
    data = tracker.data
    
    if habit not in data:
        console.print(f"[red]Habit '{habit}' not found![/red]")
        return
    
    dates = sorted([datetime.strptime(date, "%Y-%m-%d").date() for date in data[habit]])
    if not dates:
        console.print(f"[yellow]No streaks found for habit '{habit}'.[/yellow]")
        return

    longest_streak = 0
    current_streak = 1
    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current_streak += 1
            longest_streak = max(longest_streak, current_streak)
        else:
            current_streak = 1

    # Check if the streak is ongoing
    today = datetime.now().date()
    ongoing_streak = current_streak if dates[-1] == today - timedelta(days=1) or dates[-1] == today else 0

    console.print(f"[green]Longest streak:[/green] {longest_streak} 🔥")
    if ongoing_streak:
        console.print(f"[blue]Ongoing streak:[/blue] {ongoing_streak} 🌟")
    else:
        console.print(f"[yellow]No ongoing streak.[/yellow]")

