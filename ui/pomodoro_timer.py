"""
Pomodoro Timer Integration for Time Tracker
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time

class PomodoroTimer:
    """Pomodoro technique timer"""

    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.config_file = "pomodoro_config.json"
        self.config = self.load_config()

        self.is_running = False
        self.is_break = False
        self.remaining_seconds = 0
        self.timer_thread = None
        self.session_count = 0

    def load_config(self):
        """Load Pomodoro configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_config()
        return self.get_default_config()

    def get_default_config(self):
        """Get default Pomodoro config"""
        return {
            "work_duration": 25,  # minutes
            "short_break": 5,
            "long_break": 15,
            "sessions_until_long_break": 4,
            "auto_start_breaks": True,
            "auto_start_work": False,
            "sound_enabled": True,
            "daily_goal_sessions": 8
        }

    def save_config(self):
        """Save configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def create_pomodoro_ui(self, frame):
        """Create Pomodoro timer UI"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Main container
        main_frame = ctk.CTkFrame(frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True)

        # Timer section (top)
        timer_frame = ctk.CTkFrame(main_frame)
        timer_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header = ctk.CTkLabel(
            timer_frame,
            text="🍅 Pomodoro Timer",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=(20, 10))

        # Session counter
        self.session_label = ctk.CTkLabel(
            timer_frame,
            text=f"Session {self.session_count % self.config['sessions_until_long_break'] + 1}/{self.config['sessions_until_long_break']}",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.session_label.pack(pady=5)

        # Timer display
        self.timer_display = ctk.CTkLabel(
            timer_frame,
            text="25:00",
            font=ctk.CTkFont(size=96, weight="bold")
        )
        self.timer_display.pack(pady=30)

        # Status label
        self.status_label = ctk.CTkLabel(
            timer_frame,
            text="Ready to start",
            font=ctk.CTkFont(size=20),
            text_color="gray"
        )
        self.status_label.pack(pady=10)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            timer_frame,
            width=400,
            height=20,
            mode="determinate"
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)

        # Control buttons
        button_frame = ctk.CTkFrame(timer_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶️ Start",
            command=self.start_timer,
            height=50,
            width=150,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.start_btn.pack(side="left", padx=10)

        self.pause_btn = ctk.CTkButton(
            button_frame,
            text="⏸️ Pause",
            command=self.pause_timer,
            height=50,
            width=150,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00",
            state="disabled"
        )
        self.pause_btn.pack(side="left", padx=10)

        self.reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Reset",
            command=self.reset_timer,
            height=50,
            width=150,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        self.reset_btn.pack(side="left", padx=10)

        # Stats section (bottom)
        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            stats_frame,
            text="Today's Progress",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 5))

        # Daily stats
        daily_frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
        daily_frame.pack(fill="x", padx=20, pady=10)

        # Completed sessions
        completed_today = self.get_completed_today()
        goal = self.config["daily_goal_sessions"]

        session_card = ctk.CTkFrame(daily_frame)
        session_card.pack(side="left", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            session_card,
            text="🍅 Sessions",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            session_card,
            text=f"{completed_today}/{goal}",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4CAF50" if completed_today >= goal else "#2196F3"
        ).pack(pady=5)

        # Total time
        total_minutes = completed_today * self.config["work_duration"]
        time_card = ctk.CTkFrame(daily_frame)
        time_card.pack(side="left", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            time_card,
            text="⏱️ Focus Time",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))

        hours = total_minutes // 60
        minutes = total_minutes % 60
        time_text = f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"

        ctk.CTkLabel(
            time_card,
            text=time_text,
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#FF9800"
        ).pack(pady=5)

        # Settings section
        settings_frame = ctk.CTkFrame(frame)
        settings_frame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkButton(
            settings_frame,
            text="⚙️ Pomodoro Settings",
            command=self.show_settings,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=15)

        # Initialize timer display
        self.remaining_seconds = self.config["work_duration"] * 60
        self.update_display()

    def start_timer(self):
        """Start the Pomodoro timer"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.configure(state="disabled")
            self.pause_btn.configure(state="normal")

            if self.is_break:
                self.status_label.configure(text="Break Time - Relax!")
            else:
                self.status_label.configure(text="Work Session - Stay Focused!")

            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()

    def pause_timer(self):
        """Pause the timer"""
        self.is_running = False
        self.start_btn.configure(state="normal", text="▶️ Resume")
        self.pause_btn.configure(state="disabled")
        self.status_label.configure(text="Paused")

    def reset_timer(self):
        """Reset the timer"""
        self.is_running = False
        self.is_break = False
        self.remaining_seconds = self.config["work_duration"] * 60
        self.start_btn.configure(state="normal", text="▶️ Start")
        self.pause_btn.configure(state="disabled")
        self.status_label.configure(text="Ready to start")
        self.progress_bar.set(0)
        self.update_display()

    def run_timer(self):
        """Timer countdown loop"""
        total_seconds = self.remaining_seconds

        while self.is_running and self.remaining_seconds > 0:
            time.sleep(1)
            if self.is_running:
                self.remaining_seconds -= 1
                self.update_display()

                # Update progress bar
                progress = 1 - (self.remaining_seconds / total_seconds)
                self.progress_bar.set(progress)

        if self.remaining_seconds == 0 and self.is_running:
            self.timer_complete()

    def update_display(self):
        """Update timer display"""
        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60
        self.timer_display.configure(text=f"{minutes:02d}:{seconds:02d}")

    def timer_complete(self):
        """Handle timer completion"""
        self.is_running = False

        if not self.is_break:
            # Work session completed
            self.session_count += 1
            self.save_session()

            # Send notification
            self.tracker.send_notification(
                "🍅 Pomodoro Complete!",
                "Great work! Time for a break."
            )

            # Determine break type
            if self.session_count % self.config["sessions_until_long_break"] == 0:
                break_duration = self.config["long_break"]
                break_type = "Long"
            else:
                break_duration = self.config["short_break"]
                break_type = "Short"

            # Start break
            self.is_break = True
            self.remaining_seconds = break_duration * 60

            if self.config["auto_start_breaks"]:
                self.start_timer()
            else:
                self.status_label.configure(text=f"{break_type} Break Ready")
                self.start_btn.configure(state="normal", text=f"▶️ Start {break_type} Break")
                self.pause_btn.configure(state="disabled")
        else:
            # Break completed
            self.tracker.send_notification(
                "⏰ Break Over",
                "Ready to start another session?"
            )

            self.is_break = False
            self.remaining_seconds = self.config["work_duration"] * 60

            if self.config["auto_start_work"]:
                self.start_timer()
            else:
                self.status_label.configure(text="Ready to work")
                self.start_btn.configure(state="normal", text="▶️ Start Work")
                self.pause_btn.configure(state="disabled")

        # Update session counter
        self.session_label.configure(
            text=f"Session {self.session_count % self.config['sessions_until_long_break'] + 1}/{self.config['sessions_until_long_break']}"
        )
        self.update_display()
        self.progress_bar.set(0)

    def save_session(self):
        """Save completed Pomodoro session"""
        today = datetime.now().strftime("%Y-%m-%d")
        sessions_file = "pomodoro_sessions.json"

        sessions = {}
        if os.path.exists(sessions_file):
            try:
                with open(sessions_file, 'r') as f:
                    sessions = json.load(f)
            except:
                pass

        if today not in sessions:
            sessions[today] = []

        sessions[today].append({
            "timestamp": datetime.now().isoformat(),
            "duration": self.config["work_duration"]
        })

        with open(sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)

    def get_completed_today(self):
        """Get number of completed sessions today"""
        today = datetime.now().strftime("%Y-%m-%d")
        sessions_file = "pomodoro_sessions.json"

        if os.path.exists(sessions_file):
            try:
                with open(sessions_file, 'r') as f:
                    sessions = json.load(f)
                    return len(sessions.get(today, []))
            except:
                pass
        return 0

    def show_settings(self):
        """Show Pomodoro settings dialog"""
        settings_window = ctk.CTkToplevel(self.parent)
        settings_window.title("Pomodoro Settings")
        settings_window.geometry("500x700")

        # Header
        ctk.CTkLabel(
            settings_window,
            text="⚙️ Pomodoro Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(settings_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Work duration
        self.create_setting_field(
            scroll_frame, "Work Duration (minutes):", "work_duration", 1, 60
        )

        # Short break
        self.create_setting_field(
            scroll_frame, "Short Break (minutes):", "short_break", 1, 30
        )

        # Long break
        self.create_setting_field(
            scroll_frame, "Long Break (minutes):", "long_break", 1, 60
        )

        # Sessions until long break
        self.create_setting_field(
            scroll_frame, "Sessions Until Long Break:", "sessions_until_long_break", 2, 10
        )

        # Daily goal
        self.create_setting_field(
            scroll_frame, "Daily Goal (sessions):", "daily_goal_sessions", 1, 20
        )

        # Checkboxes
        self.auto_start_breaks_var = ctk.BooleanVar(value=self.config["auto_start_breaks"])
        ctk.CTkCheckBox(
            scroll_frame,
            text="Auto-start breaks",
            variable=self.auto_start_breaks_var
        ).pack(anchor="w", pady=10, padx=20)

        self.auto_start_work_var = ctk.BooleanVar(value=self.config["auto_start_work"])
        ctk.CTkCheckBox(
            scroll_frame,
            text="Auto-start work sessions",
            variable=self.auto_start_work_var
        ).pack(anchor="w", pady=10, padx=20)

        # Save button
        ctk.CTkButton(
            settings_window,
            text="💾 Save Settings",
            command=lambda: self.save_pomodoro_settings(settings_window),
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(pady=20)

    def create_setting_field(self, parent, label, config_key, min_val, max_val):
        """Create a setting input field"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", pady=10, padx=20)

        ctk.CTkLabel(frame, text=label, width=250, anchor="w").pack(side="left", padx=5)

        entry = ctk.CTkEntry(frame, width=100)
        entry.pack(side="left", padx=5)
        entry.insert(0, str(self.config[config_key]))

        # Store reference
        if not hasattr(self, 'setting_entries'):
            self.setting_entries = {}
        self.setting_entries[config_key] = entry

    def save_pomodoro_settings(self, window):
        """Save Pomodoro settings"""
        try:
            for key, entry in self.setting_entries.items():
                self.config[key] = int(entry.get())

            self.config["auto_start_breaks"] = self.auto_start_breaks_var.get()
            self.config["auto_start_work"] = self.auto_start_work_var.get()

            self.save_config()
            window.destroy()
            messagebox.showinfo("Success", "Pomodoro settings saved!")

            # Reset timer with new duration
            if not self.is_running and not self.is_break:
                self.remaining_seconds = self.config["work_duration"] * 60
                self.update_display()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers")
