"""
Calendar View for Time Tracker
"""

import customtkinter as ctk
from datetime import datetime, timedelta
import calendar
from tkinter import messagebox

class CalendarView:
    """Interactive calendar view for tracking history"""

    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.current_date = datetime.now()

    def create_calendar(self, frame):
        """Create interactive calendar"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header with navigation
        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)

        prev_btn = ctk.CTkButton(
            header_frame,
            text="◀",
            width=50,
            command=self.previous_month,
            font=ctk.CTkFont(size=16)
        )
        prev_btn.pack(side="left", padx=5)

        month_label = ctk.CTkLabel(
            header_frame,
            text=self.current_date.strftime("%B %Y"),
            font=ctk.CTkFont(size=24, weight="bold")
        )
        month_label.pack(side="left", expand=True)

        next_btn = ctk.CTkButton(
            header_frame,
            text="▶",
            width=50,
            command=self.next_month,
            font=ctk.CTkFont(size=16)
        )
        next_btn.pack(side="left", padx=5)

        today_btn = ctk.CTkButton(
            header_frame,
            text="Today",
            width=80,
            command=self.go_to_today,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        today_btn.pack(side="left", padx=5)

        # Days of week header
        days_frame = ctk.CTkFrame(frame)
        days_frame.pack(fill="x", padx=20, pady=(10, 0))

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for day in days:
            day_label = ctk.CTkLabel(
                days_frame,
                text=day,
                font=ctk.CTkFont(size=14, weight="bold"),
                width=100
            )
            day_label.pack(side="left", expand=True, padx=2)

        # Calendar grid
        cal_frame = ctk.CTkFrame(frame)
        cal_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Get calendar data
        year = self.current_date.year
        month = self.current_date.month
        cal = calendar.monthcalendar(year, month)

        for week_num, week in enumerate(cal):
            week_frame = ctk.CTkFrame(cal_frame, fg_color="transparent")
            week_frame.pack(fill="both", expand=True, pady=2)

            for day_num in week:
                if day_num == 0:
                    # Empty cell
                    empty = ctk.CTkFrame(week_frame, fg_color="transparent")
                    empty.pack(side="left", expand=True, padx=2)
                else:
                    # Create day cell
                    self.create_day_cell(week_frame, day_num, year, month)

    def create_day_cell(self, parent, day, year, month):
        """Create a single day cell"""
        date_str = f"{year}-{month:02d}-{day:02d}"
        day_data = self.tracker.data.get(date_str, {})

        # Calculate total hours for the day
        total_hours = sum(v for k, v in day_data.items()
                         if k not in ['date', 'session_duration', 'idle_time', 'projects'])

        # Determine color based on productivity
        if total_hours == 0:
            bg_color = "#2b2b2b"
        elif total_hours < 2:
            bg_color = "#37474F"
        elif total_hours < 4:
            bg_color = "#455A64"
        elif total_hours < 6:
            bg_color = "#546E7A"
        elif total_hours < 8:
            bg_color = "#607D8B"
        else:
            bg_color = "#78909C"

        # Check if it's today
        today = datetime.now()
        is_today = (day == today.day and month == today.month and year == today.year)

        if is_today:
            border_color = "#2196F3"
        else:
            border_color = "transparent"

        cell_frame = ctk.CTkFrame(
            parent,
            fg_color=bg_color,
            border_width=2,
            border_color=border_color
        )
        cell_frame.pack(side="left", expand=True, fill="both", padx=2)

        # Day number
        day_label = ctk.CTkLabel(
            cell_frame,
            text=str(day),
            font=ctk.CTkFont(size=16, weight="bold" if is_today else "normal")
        )
        day_label.pack(pady=(5, 0))

        # Hours
        if total_hours > 0:
            hours_label = ctk.CTkLabel(
                cell_frame,
                text=f"{total_hours:.1f}h",
                font=ctk.CTkFont(size=11),
                text_color="#B0BEC5"
            )
            hours_label.pack()

        # Click to view details
        cell_frame.bind("<Button-1>", lambda e: self.show_day_details(date_str))
        day_label.bind("<Button-1>", lambda e: self.show_day_details(date_str))

    def show_day_details(self, date_str):
        """Show detailed view for a specific day"""
        day_data = self.tracker.data.get(date_str, {})

        if not day_data or all(v == 0 for k, v in day_data.items()
                               if k not in ['date', 'session_duration', 'idle_time', 'projects']):
            messagebox.showinfo("No Data", f"No tracking data for {date_str}")
            return

        # Create detail window
        detail_window = ctk.CTkToplevel(self.parent)
        detail_window.title(f"Details for {date_str}")
        detail_window.geometry("500x600")

        # Header
        header = ctk.CTkLabel(
            detail_window,
            text=f"📅 {date_str}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        header.pack(pady=20)

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(detail_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Show each category
        for category, hours in sorted(day_data.items(), key=lambda x: x[1], reverse=True):
            if category not in ['date', 'session_duration', 'idle_time', 'projects'] and hours > 0:
                cat_frame = ctk.CTkFrame(scroll_frame)
                cat_frame.pack(fill="x", pady=5)

                cat_label = ctk.CTkLabel(
                    cat_frame,
                    text=category,
                    font=ctk.CTkFont(size=16, weight="bold")
                )
                cat_label.pack(side="left", padx=10, pady=10)

                hours_label = ctk.CTkLabel(
                    cat_frame,
                    text=f"{hours:.2f}h",
                    font=ctk.CTkFont(size=16),
                    text_color="#4CAF50"
                )
                hours_label.pack(side="right", padx=10, pady=10)

        # Show projects if any
        if 'projects' in day_data and day_data['projects']:
            proj_header = ctk.CTkLabel(
                scroll_frame,
                text="Projects:",
                font=ctk.CTkFont(size=18, weight="bold")
            )
            proj_header.pack(pady=(20, 10))

            for proj, hours in day_data['projects'].items():
                proj_frame = ctk.CTkFrame(scroll_frame)
                proj_frame.pack(fill="x", pady=5)

                proj_label = ctk.CTkLabel(
                    proj_frame,
                    text=f"📁 {proj}",
                    font=ctk.CTkFont(size=14)
                )
                proj_label.pack(side="left", padx=10, pady=5)

                proj_hours = ctk.CTkLabel(
                    proj_frame,
                    text=f"{hours:.2f}h",
                    font=ctk.CTkFont(size=14),
                    text_color="#2196F3"
                )
                proj_hours.pack(side="right", padx=10, pady=5)

        # Close button
        close_btn = ctk.CTkButton(
            detail_window,
            text="Close",
            command=detail_window.destroy,
            height=40
        )
        close_btn.pack(pady=20)

    def previous_month(self):
        """Go to previous month"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.create_calendar(self.parent)

    def next_month(self):
        """Go to next month"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.create_calendar(self.parent)

    def go_to_today(self):
        """Return to current month"""
        self.current_date = datetime.now()
        self.create_calendar(self.parent)
