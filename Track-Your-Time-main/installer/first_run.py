"""
First-run setup wizard for Time Tracker Pro
Helps users configure the app on first launch
"""

import customtkinter as ctk
import json
import os
from pathlib import Path
import sys

class FirstRunWizard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Time Tracker Pro - Welcome")
        self.geometry("700x600")
        self.resizable(False, False)

        # Center window
        self.center_window()

        # Configuration to save
        self.config = {
            "idle_threshold_seconds": 300,
            "goals": {},
            "notifications_enabled": True,
            "break_reminder_interval": 3600,
            "focus_mode_blocked": ["facebook", "twitter", "instagram", "tiktok", "youtube", "netflix"],
            "auto_start": False,
            "first_run_completed": True
        }

        # Current page
        self.current_page = 0
        self.pages = [
            self.create_welcome_page,
            self.create_goals_page,
            self.create_settings_page,
            self.create_autostart_page,
            self.create_finish_page
        ]

        # Container for pages
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Navigation buttons
        self.nav_frame = ctk.CTkFrame(self)
        self.nav_frame.pack(fill="x", padx=20, pady=(0, 20))

        self.back_button = ctk.CTkButton(
            self.nav_frame,
            text="← Back",
            command=self.previous_page,
            width=100
        )
        self.back_button.pack(side="left", padx=5)
        self.back_button.configure(state="disabled")

        self.next_button = ctk.CTkButton(
            self.nav_frame,
            text="Next →",
            command=self.next_page,
            width=100
        )
        self.next_button.pack(side="right", padx=5)

        # Show first page
        self.show_page()

    def center_window(self):
        """Center the window on screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def clear_container(self):
        """Clear the container"""
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_page(self):
        """Show current page"""
        self.clear_container()
        self.pages[self.current_page]()

        # Update navigation buttons
        if self.current_page == 0:
            self.back_button.configure(state="disabled")
        else:
            self.back_button.configure(state="normal")

        if self.current_page == len(self.pages) - 1:
            self.next_button.configure(text="Finish ✓")
        else:
            self.next_button.configure(text="Next →")

    def next_page(self):
        """Go to next page"""
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page()
        else:
            # Finish setup
            self.save_config()
            self.destroy()

    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def create_welcome_page(self):
        """Create welcome page"""
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="Welcome to Time Tracker Pro! ⏱️",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=(50, 20))

        # Subtitle
        subtitle = ctk.CTkLabel(
            frame,
            text="Let's set up your time tracking in just a few steps",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))

        # Features
        features_frame = ctk.CTkFrame(frame, corner_radius=10)
        features_frame.pack(fill="both", expand=True, padx=40, pady=20)

        features = [
            ("📊", "Real-time Dashboard", "See what you're working on right now"),
            ("🎯", "Goal Tracking", "Set and achieve your productivity goals"),
            ("🔥", "Streak System", "Build consistent habits"),
            ("🎯", "Focus Mode", "Block distractions when you need to concentrate"),
            ("📁", "Project Tracking", "Organize your time by projects"),
        ]

        for icon, title, desc in features:
            item_frame = ctk.CTkFrame(features_frame, fg_color="transparent")
            item_frame.pack(fill="x", padx=20, pady=10)

            ctk.CTkLabel(
                item_frame,
                text=f"{icon} {title}",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(fill="x")

            ctk.CTkLabel(
                item_frame,
                text=desc,
                font=ctk.CTkFont(size=12),
                text_color="gray",
                anchor="w"
            ).pack(fill="x")

    def create_goals_page(self):
        """Create goals setup page"""
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="Set Your Daily Goals 🎯",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            frame,
            text="How many hours per day do you want to spend on each category?",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))

        # Goals input
        goals_frame = ctk.CTkFrame(frame, corner_radius=10)
        goals_frame.pack(fill="both", expand=True, padx=40, pady=20)

        self.goal_entries = {}
        categories = [
            ("Coding", "💻", 4),
            ("Productivity", "📝", 3),
            ("Education", "📚", 2),
            ("Entertainment", "🎮", 2),
        ]

        for category, icon, default in categories:
            cat_frame = ctk.CTkFrame(goals_frame, fg_color="transparent")
            cat_frame.pack(fill="x", padx=20, pady=10)

            ctk.CTkLabel(
                cat_frame,
                text=f"{icon} {category}",
                font=ctk.CTkFont(size=14, weight="bold"),
                width=150
            ).pack(side="left", padx=(0, 20))

            entry = ctk.CTkEntry(cat_frame, width=80, placeholder_text=str(default))
            entry.insert(0, str(default))
            entry.pack(side="left")

            ctk.CTkLabel(
                cat_frame,
                text="hours/day",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(side="left", padx=(10, 0))

            self.goal_entries[category] = entry

        # Note
        note = ctk.CTkLabel(
            frame,
            text="Don't worry, you can change these anytime in Settings",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        note.pack(pady=10)

    def create_settings_page(self):
        """Create settings page"""
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="Configure Settings ⚙️",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            frame,
            text="Customize how Time Tracker works for you",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))

        # Settings
        settings_frame = ctk.CTkFrame(frame, corner_radius=10)
        settings_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Notifications
        self.notifications_var = ctk.BooleanVar(value=True)
        notif_switch = ctk.CTkSwitch(
            settings_frame,
            text="Enable notifications for goals and reminders",
            variable=self.notifications_var,
            font=ctk.CTkFont(size=14)
        )
        notif_switch.pack(anchor="w", padx=20, pady=15)

        # Idle threshold
        idle_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        idle_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            idle_frame,
            text="Idle threshold (minutes):",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        self.idle_entry = ctk.CTkEntry(idle_frame, width=80)
        self.idle_entry.insert(0, "5")
        self.idle_entry.pack(side="left", padx=10)

        ctk.CTkLabel(
            idle_frame,
            text="(pause tracking after this time)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="left")

        # Break reminder
        break_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        break_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            break_frame,
            text="Break reminder (minutes):",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        self.break_entry = ctk.CTkEntry(break_frame, width=80)
        self.break_entry.insert(0, "60")
        self.break_entry.pack(side="left", padx=10)

        ctk.CTkLabel(
            break_frame,
            text="(remind to take breaks)",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(side="left")

    def create_autostart_page(self):
        """Create auto-start page"""
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="Start Automatically? 🚀",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(30, 10))

        subtitle = ctk.CTkLabel(
            frame,
            text="Would you like Time Tracker to start automatically when Windows starts?",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 30))

        # Info
        info_frame = ctk.CTkFrame(frame, corner_radius=10)
        info_frame.pack(fill="both", expand=True, padx=40, pady=20)

        benefits = [
            "✅ Never forget to start tracking",
            "✅ Get complete daily statistics",
            "✅ Runs silently in the background",
            "✅ Can be paused anytime from system tray",
        ]

        for benefit in benefits:
            ctk.CTkLabel(
                info_frame,
                text=benefit,
                font=ctk.CTkFont(size=14),
                anchor="w"
            ).pack(fill="x", padx=20, pady=10)

        # Toggle
        self.autostart_var = ctk.BooleanVar(value=True)
        autostart_switch = ctk.CTkSwitch(
            frame,
            text="Start Time Tracker when Windows starts",
            variable=self.autostart_var,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        autostart_switch.pack(pady=30)

    def create_finish_page(self):
        """Create finish page"""
        frame = ctk.CTkFrame(self.container, fg_color="transparent")
        frame.pack(fill="both", expand=True)

        # Title
        title = ctk.CTkLabel(
            frame,
            text="All Set! 🎉",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.pack(pady=(50, 20))

        subtitle = ctk.CTkLabel(
            frame,
            text="Time Tracker Pro is ready to help you understand your time",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))

        # Summary
        summary_frame = ctk.CTkFrame(frame, corner_radius=10)
        summary_frame.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(
            summary_frame,
            text="Your Configuration:",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(20, 10), anchor="w", padx=20)

        # Build summary text
        summary_items = []

        # Goals
        if hasattr(self, 'goal_entries'):
            goals_set = sum(1 for e in self.goal_entries.values() if e.get().strip())
            summary_items.append(f"📊 {goals_set} goals configured")

        # Settings
        summary_items.append(f"⚙️ Idle threshold: {self.idle_entry.get()} minutes")
        summary_items.append(f"⏰ Break reminder: {self.break_entry.get()} minutes")
        summary_items.append(f"🔔 Notifications: {'Enabled' if self.notifications_var.get() else 'Disabled'}")
        summary_items.append(f"🚀 Auto-start: {'Enabled' if self.autostart_var.get() else 'Disabled'}")

        for item in summary_items:
            ctk.CTkLabel(
                summary_frame,
                text=item,
                font=ctk.CTkFont(size=13),
                anchor="w"
            ).pack(fill="x", padx=20, pady=5)

        # Final message
        message = ctk.CTkLabel(
            frame,
            text="Click 'Finish' to start tracking your time!",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        message.pack(pady=20)

    def save_config(self):
        """Save configuration"""
        # Save goals
        if hasattr(self, 'goal_entries'):
            for category, entry in self.goal_entries.items():
                try:
                    hours = float(entry.get() or 0)
                    if hours > 0:
                        self.config["goals"][category] = hours
                except:
                    pass

        # Save settings
        try:
            self.config["idle_threshold_seconds"] = int(float(self.idle_entry.get()) * 60)
        except:
            pass

        try:
            self.config["break_reminder_interval"] = int(float(self.break_entry.get()) * 60)
        except:
            pass

        self.config["notifications_enabled"] = self.notifications_var.get()
        self.config["auto_start"] = self.autostart_var.get()

        # Save to file
        config_path = Path.home() / "tracker_config.json"
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

        print(f"✅ Configuration saved to {config_path}")


def main():
    """Main entry point"""
    # Check if first run is needed
    config_path = Path.home() / "tracker_config.json"

    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if config.get("first_run_completed"):
                    print("First run already completed")
                    return
        except:
            pass

    # Run wizard
    app = FirstRunWizard()
    app.mainloop()


if __name__ == "__main__":
    main()
