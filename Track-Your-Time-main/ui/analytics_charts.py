"""
Interactive Analytics Charts for Time Tracker
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk
from datetime import datetime, timedelta
from collections import defaultdict
import json

class AnalyticsCharts:
    """Creates interactive charts for time tracking analytics"""

    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker

    def create_weekly_chart(self, frame):
        """Create weekly time distribution chart"""
        # Get last 7 days of data
        data_by_day = defaultdict(lambda: defaultdict(float))

        for date_str, day_data in self.tracker.data.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if (datetime.now() - date).days <= 7:
                    for category, hours in day_data.items():
                        if category not in ['date', 'session_duration', 'idle_time', 'projects']:
                            data_by_day[date_str][category] = hours
            except:
                continue

        # Create figure
        fig = Figure(figsize=(10, 6), facecolor='#1e1e1e')
        ax = fig.add_subplot(111)

        # Prepare data
        dates = sorted(data_by_day.keys())[-7:]
        categories = set()
        for day in dates:
            categories.update(data_by_day[day].keys())

        # Plot stacked bar chart
        bottom = [0] * len(dates)
        colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0', '#00BCD4', '#FFEB3B']

        for i, category in enumerate(sorted(categories)):
            values = [data_by_day[date].get(category, 0) for date in dates]
            ax.bar(dates, values, bottom=bottom, label=category, color=colors[i % len(colors)])
            bottom = [b + v for b, v in zip(bottom, values)]

        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Hours', color='white')
        ax.set_title('Weekly Time Distribution', color='white', fontsize=16, pad=20)
        ax.legend(loc='upper left', framealpha=0.9)
        ax.tick_params(colors='white')
        ax.set_facecolor('#2b2b2b')
        fig.patch.set_facecolor('#1e1e1e')
        plt.xticks(rotation=45)

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        return canvas

    def create_category_pie_chart(self, frame):
        """Create pie chart for category distribution"""
        # Get today's data
        today = datetime.now().strftime("%Y-%m-%d")
        today_data = self.tracker.data.get(today, {})

        categories = {}
        for key, value in today_data.items():
            if key not in ['date', 'session_duration', 'idle_time', 'projects'] and value > 0:
                categories[key] = value

        if not categories:
            # Show message
            label = ctk.CTkLabel(frame, text="No data for today yet. Start tracking!",
                               font=ctk.CTkFont(size=16))
            label.pack(pady=50)
            return None

        # Create figure
        fig = Figure(figsize=(8, 8), facecolor='#1e1e1e')
        ax = fig.add_subplot(111)

        colors = ['#2196F3', '#4CAF50', '#FF9800', '#F44336', '#9C27B0', '#00BCD4', '#FFEB3B']

        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
               colors=colors[:len(categories)], textprops={'color': 'white'})
        ax.set_title("Today's Category Distribution", color='white', fontsize=16, pad=20)
        fig.patch.set_facecolor('#1e1e1e')

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        return canvas

    def create_productivity_heatmap(self, frame):
        """Create heatmap showing productivity by hour of day"""
        # Aggregate data by hour
        hourly_data = defaultdict(lambda: defaultdict(float))

        # This would require tracking hourly data - placeholder for now
        label = ctk.CTkLabel(frame, text="Hourly heatmap coming soon!\n(Requires hourly tracking data)",
                           font=ctk.CTkFont(size=16), text_color="gray")
        label.pack(pady=50)

        return None

    def create_trend_line_chart(self, frame):
        """Create line chart showing productivity trends"""
        # Get last 30 days
        data_by_day = {}

        for date_str, day_data in self.tracker.data.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if (datetime.now() - date).days <= 30:
                    total_hours = sum(v for k, v in day_data.items()
                                    if k not in ['date', 'session_duration', 'idle_time', 'projects'])
                    data_by_day[date_str] = total_hours
            except:
                continue

        if len(data_by_day) < 2:
            label = ctk.CTkLabel(frame, text="Not enough data yet. Keep tracking!",
                               font=ctk.CTkFont(size=16), text_color="gray")
            label.pack(pady=50)
            return None

        # Create figure
        fig = Figure(figsize=(10, 6), facecolor='#1e1e1e')
        ax = fig.add_subplot(111)

        dates = sorted(data_by_day.keys())
        hours = [data_by_day[d] for d in dates]

        ax.plot(dates, hours, marker='o', color='#2196F3', linewidth=2, markersize=6)
        ax.fill_between(range(len(dates)), hours, alpha=0.3, color='#2196F3')

        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Total Hours', color='white')
        ax.set_title('30-Day Productivity Trend', color='white', fontsize=16, pad=20)
        ax.tick_params(colors='white')
        ax.set_facecolor('#2b2b2b')
        ax.grid(True, alpha=0.2, color='white')
        fig.patch.set_facecolor('#1e1e1e')
        plt.xticks(rotation=45)

        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        return canvas
