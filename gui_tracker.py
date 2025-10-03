"""
Modern GUI Time Tracker
A beautiful, feature-rich time tracking application
"""

import customtkinter as ctk
import threading
import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import logging
import traceback

# Import the core tracker
from tracker import TimeTracker
from ui.themes import get_theme, DARK_THEME, LIGHT_THEME, get_category_color

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('time_tracker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TimeTrackerGUI')

class TimeTrackerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        try:
            # Window configuration
            self.title("⏱️ Time Tracker Pro")
            self.geometry("1200x800")
            self.minsize(1000, 700)

            logger.info("Initializing Time Tracker Pro")

            # Initialize tracker backend
            self.tracker = TimeTracker()
            self.tracking_thread = None
            self.is_tracking = False
            self.is_dark_mode = True
            self.last_error = None

            # Restore focus mode state from config
            self.tracker.focus_mode = self.tracker.config.get("focus_mode_active", False)

            # Set icon (if available)
            try:
                icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
                if os.path.exists(icon_path):
                    self.iconbitmap(icon_path)
            except Exception as e:
                logger.warning(f"Could not load icon: {e}")

            # Setup UI
            self.setup_ui()

            # Start update loop
            self.update_dashboard()

            # Handle window close
            self.protocol("WM_DELETE_WINDOW", self.on_closing)

            logger.info("Time Tracker Pro initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize Time Tracker: {e}", exc_info=True)
            messagebox.showerror("Initialization Error", f"Failed to start Time Tracker:\n{str(e)}\n\nCheck time_tracker.log for details")
            sys.exit(1)

    def setup_ui(self):
        """Setup the main user interface"""
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top bar
        self.create_top_bar()

        # Main content area with tabs
        self.create_tabview()

    def create_top_bar(self):
        """Create the top navigation bar"""
        self.top_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        self.top_frame.grid_columnconfigure(1, weight=1)

        # Logo and title
        title_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        title_label = ctk.CTkLabel(
            title_frame,
            text="⏱️ Time Tracker Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")

        # Status indicator
        self.status_frame = ctk.CTkFrame(self.top_frame, fg_color="transparent")
        self.status_frame.grid(row=0, column=1, sticky="e", padx=20, pady=20)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="⏸️ Not Tracking",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(side="left", padx=10)

        # Track/Pause button
        self.track_button = ctk.CTkButton(
            self.status_frame,
            text="▶️ Start Tracking",
            command=self.toggle_tracking,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4caf50",
            hover_color="#45a049"
        )
        self.track_button.pack(side="left", padx=5)

        # Theme toggle
        self.theme_button = ctk.CTkButton(
            self.status_frame,
            text="🌙",
            command=self.toggle_theme,
            width=50,
            height=40,
            font=ctk.CTkFont(size=20)
        )
        self.theme_button.pack(side="left", padx=5)

        # Health status indicator
        self.health_indicator = ctk.CTkLabel(
            self.status_frame,
            text="✓",
            font=ctk.CTkFont(size=20),
            text_color="#4caf50"
        )
        self.health_indicator.pack(side="left", padx=5)

    def create_tabview(self):
        """Create the main tab view"""
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        # Add tabs
        self.tab_dashboard = self.tabview.add("📊 Dashboard")
        self.tab_analytics = self.tabview.add("📈 Analytics")
        self.tab_goals = self.tabview.add("🎯 Goals")
        self.tab_focus = self.tabview.add("🎯 Focus Mode")
        self.tab_projects = self.tabview.add("📁 Projects")
        self.tab_settings = self.tabview.add("⚙️ Settings")

        # Configure tab grid
        for tab in [self.tab_dashboard, self.tab_analytics, self.tab_goals,
                    self.tab_focus, self.tab_projects, self.tab_settings]:
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)

        # Initialize tabs
        self.init_dashboard_tab()
        self.init_analytics_tab()
        self.init_goals_tab()
        self.init_focus_tab()
        self.init_projects_tab()
        self.init_settings_tab()

    def init_dashboard_tab(self):
        """Initialize dashboard tab"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_dashboard, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Current activity section
        activity_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        activity_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        activity_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            activity_frame,
            text="📍 Current Activity",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20,10))

        self.current_app_label = ctk.CTkLabel(
            activity_frame,
            text="Idle",
            font=ctk.CTkFont(size=16)
        )
        self.current_app_label.grid(row=1, column=0, sticky="w", padx=20, pady=5)

        self.current_duration_label = ctk.CTkLabel(
            activity_frame,
            text="0m 0s",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.current_duration_label.grid(row=1, column=1, sticky="e", padx=20, pady=5)

        self.current_category_label = ctk.CTkLabel(
            activity_frame,
            text="Category: None",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.current_category_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=20, pady=(0,20))

        # Today's stats
        stats_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        stats_container.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        stats_container.grid_columnconfigure((0,1), weight=1)

        # Total time card
        total_frame = ctk.CTkFrame(stats_container, corner_radius=10)
        total_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(
            total_frame,
            text="⏱️ Total Today",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(20,10))

        self.total_time_label = ctk.CTkLabel(
            total_frame,
            text="0.0h",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.total_time_label.pack(padx=20, pady=(0,20))

        # Streak card
        streak_frame = ctk.CTkFrame(stats_container, corner_radius=10)
        streak_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        ctk.CTkLabel(
            streak_frame,
            text="🔥 Current Streak",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(padx=20, pady=(20,10))

        self.streak_label = ctk.CTkLabel(
            streak_frame,
            text="0 days",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.streak_label.pack(padx=20, pady=(0,20))

        # Category breakdown
        category_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        category_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(
            category_frame,
            text="📊 Category Breakdown",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20,10), anchor="w")

        self.category_container = ctk.CTkFrame(category_frame, fg_color="transparent")
        self.category_container.pack(fill="both", expand=True, padx=20, pady=(0,20))

    def init_analytics_tab(self):
        """Initialize analytics tab"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_analytics, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll_frame.grid_columnconfigure((0,1), weight=1)

        # Title and time range selector
        header_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            header_frame,
            text="📈 Analytics & Insights",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Time range selector
        self.analytics_range_var = ctk.StringVar(value="Week")
        range_menu = ctk.CTkSegmentedButton(
            header_frame,
            values=["Today", "Week", "Month", "All Time"],
            variable=self.analytics_range_var,
            command=self.update_analytics
        )
        range_menu.grid(row=0, column=1, sticky="e", padx=20, pady=20)

        # Summary cards
        cards_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        cards_container.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        cards_container.grid_columnconfigure((0,1,2), weight=1)

        # Total time card
        self.analytics_total_card = ctk.CTkFrame(cards_container, corner_radius=10)
        self.analytics_total_card.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(
            self.analytics_total_card,
            text="⏱️ Total Time",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=20, pady=(20,5))
        self.analytics_total_label = ctk.CTkLabel(
            self.analytics_total_card,
            text="0.0h",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.analytics_total_label.pack(padx=20, pady=(5,20))

        # Productivity score card
        self.analytics_prod_card = ctk.CTkFrame(cards_container, corner_radius=10)
        self.analytics_prod_card.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(
            self.analytics_prod_card,
            text="📊 Productivity Score",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=20, pady=(20,5))
        self.analytics_prod_label = ctk.CTkLabel(
            self.analytics_prod_card,
            text="0%",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.analytics_prod_label.pack(padx=20, pady=(5,20))

        # Most used app card
        self.analytics_top_card = ctk.CTkFrame(cards_container, corner_radius=10)
        self.analytics_top_card.grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ctk.CTkLabel(
            self.analytics_top_card,
            text="⭐ Most Used App",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(padx=20, pady=(20,5))
        self.analytics_top_label = ctk.CTkLabel(
            self.analytics_top_card,
            text="None",
            font=ctk.CTkFont(size=16)
        )
        self.analytics_top_label.pack(padx=20, pady=(5,5))
        self.analytics_top_hours = ctk.CTkLabel(
            self.analytics_top_card,
            text="0.0h",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.analytics_top_hours.pack(padx=20, pady=(0,20))

        # Category breakdown
        category_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        category_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        category_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            category_frame,
            text="📊 Category Breakdown",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20,10))

        self.analytics_categories = ctk.CTkFrame(category_frame, fg_color="transparent")
        self.analytics_categories.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))

        # Top apps table
        apps_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        apps_frame.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        apps_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            apps_frame,
            text="⭐ Top Applications",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20,10))

        self.analytics_apps = ctk.CTkFrame(apps_frame, fg_color="transparent")
        self.analytics_apps.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0,20))

        # Daily trend chart (text-based)
        trend_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        trend_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(
            trend_frame,
            text="📈 Time Trend",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20,10), anchor="w")

        self.analytics_trend = ctk.CTkFrame(trend_frame, fg_color="transparent")
        self.analytics_trend.pack(fill="both", expand=True, padx=20, pady=(0,20))

        # Initial update
        self.update_analytics(None)

    def init_goals_tab(self):
        """Initialize goals tab"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_goals, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            scroll_frame,
            text="🎯 Daily Goals",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Goals container
        self.goals_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        self.goals_container.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.goals_container.grid_columnconfigure((0,1), weight=1)

        # Add goal button
        add_button = ctk.CTkButton(
            scroll_frame,
            text="➕ Add New Goal",
            command=self.add_goal_dialog,
            height=40
        )
        add_button.grid(row=2, column=0, sticky="ew", padx=20, pady=20)

        # Load existing goals
        self.refresh_goals()

    def init_focus_tab(self):
        """Initialize focus mode tab"""
        container = ctk.CTkFrame(self.tab_focus, fg_color="transparent")
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ctk.CTkLabel(
            container,
            text="🎯 Focus Mode",
            font=ctk.CTkFont(size=32, weight="bold")
        ).pack(pady=20)

        # Status
        self.focus_status_label = ctk.CTkLabel(
            container,
            text="Inactive",
            font=ctk.CTkFont(size=18),
            text_color="gray"
        )
        self.focus_status_label.pack(pady=10)

        # Toggle button
        self.focus_button = ctk.CTkButton(
            container,
            text="🎯 Activate Focus Mode",
            command=self.toggle_focus_mode,
            width=250,
            height=60,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.focus_button.pack(pady=20)

        # Blocked apps info
        info_label = ctk.CTkLabel(
            container,
            text="Blocked apps will be minimized automatically",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info_label.pack(pady=10)

    def init_projects_tab(self):
        """Initialize projects tab"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_projects, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            scroll_frame,
            text="📁 Projects",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # Current project selector
        project_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        project_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

        ctk.CTkLabel(
            project_frame,
            text="Current Project:",
            font=ctk.CTkFont(size=16)
        ).pack(side="left", padx=20, pady=20)

        self.project_var = ctk.StringVar(value="None")
        self.project_dropdown = ctk.CTkComboBox(
            project_frame,
            variable=self.project_var,
            values=["None"] + list(self.tracker.config.get("projects", {}).keys()),
            command=self.change_project,
            width=200
        )
        self.project_dropdown.pack(side="left", padx=10, pady=20)

        # Add project button
        add_project_button = ctk.CTkButton(
            project_frame,
            text="➕ New Project",
            command=self.add_project_dialog,
            width=120
        )
        add_project_button.pack(side="left", padx=10, pady=20)

    def init_settings_tab(self):
        """Initialize settings tab"""
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(self.tab_settings, fg_color="transparent")
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            scroll_frame,
            text="⚙️ Settings",
            font=ctk.CTkFont(size=24, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=20)

        # === TRACKING SETTINGS ===
        tracking_header = ctk.CTkLabel(
            scroll_frame,
            text="📊 Tracking Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        tracking_header.grid(row=1, column=0, sticky="w", padx=20, pady=(10,5))

        # Idle threshold
        idle_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        idle_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        idle_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            idle_frame,
            text="Idle Threshold (seconds):",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        self.idle_entry = ctk.CTkEntry(idle_frame, width=100)
        self.idle_entry.insert(0, str(self.tracker.config.get("idle_threshold_seconds", 300)))
        self.idle_entry.grid(row=0, column=1, sticky="e", padx=20, pady=15)

        # Break reminder
        break_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        break_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        break_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            break_frame,
            text="Break Reminder (seconds):",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=0, sticky="w", padx=20, pady=15)

        self.break_entry = ctk.CTkEntry(break_frame, width=100)
        self.break_entry.insert(0, str(self.tracker.config.get("break_reminder_interval", 3600)))
        self.break_entry.grid(row=0, column=1, sticky="e", padx=20, pady=15)

        # === NOTIFICATIONS ===
        notif_header = ctk.CTkLabel(
            scroll_frame,
            text="🔔 Notifications",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        notif_header.grid(row=4, column=0, sticky="w", padx=20, pady=(20,5))

        notif_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        notif_frame.grid(row=5, column=0, sticky="ew", padx=10, pady=5)

        self.notif_var = ctk.BooleanVar(value=self.tracker.config.get("notifications_enabled", True))
        notif_switch = ctk.CTkSwitch(
            notif_frame,
            text="Enable Notifications",
            variable=self.notif_var,
            font=ctk.CTkFont(size=14)
        )
        notif_switch.pack(padx=20, pady=15, anchor="w")

        # === APPEARANCE ===
        appearance_header = ctk.CTkLabel(
            scroll_frame,
            text="🎨 Appearance",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        appearance_header.grid(row=6, column=0, sticky="w", padx=20, pady=(20,5))

        appearance_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        appearance_frame.grid(row=7, column=0, sticky="ew", padx=10, pady=5)

        # Theme preference (default)
        theme_inner = ctk.CTkFrame(appearance_frame, fg_color="transparent")
        theme_inner.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            theme_inner,
            text="Default Theme:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        self.default_theme_var = ctk.StringVar(value=self.tracker.config.get("default_theme", "dark"))
        theme_selector = ctk.CTkSegmentedButton(
            theme_inner,
            values=["dark", "light"],
            variable=self.default_theme_var
        )
        theme_selector.pack(side="right", padx=10)

        # === APP MANAGEMENT ===
        apps_header = ctk.CTkLabel(
            scroll_frame,
            text="📱 App Management",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        apps_header.grid(row=8, column=0, sticky="w", padx=20, pady=(20,5))

        # Excluded apps
        excluded_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        excluded_frame.grid(row=9, column=0, sticky="ew", padx=10, pady=5)

        ctk.CTkLabel(
            excluded_frame,
            text="Excluded Apps (comma-separated patterns):",
            font=ctk.CTkFont(size=14)
        ).pack(padx=20, pady=(15,5), anchor="w")

        self.excluded_entry = ctk.CTkEntry(excluded_frame, width=400)
        current_excluded = ", ".join(self.tracker.config.get("excluded_apps", []))
        self.excluded_entry.insert(0, current_excluded)
        self.excluded_entry.pack(padx=20, pady=(0,15), fill="x")

        # Custom categories
        custom_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        custom_frame.grid(row=10, column=0, sticky="ew", padx=10, pady=5)

        custom_header_frame = ctk.CTkFrame(custom_frame, fg_color="transparent")
        custom_header_frame.pack(fill="x", padx=20, pady=(15,10))

        ctk.CTkLabel(
            custom_header_frame,
            text="Custom Category Rules:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left")

        add_rule_btn = ctk.CTkButton(
            custom_header_frame,
            text="➕ Add Rule",
            command=self.add_custom_category_rule,
            width=100,
            height=28
        )
        add_rule_btn.pack(side="right")

        self.custom_rules_container = ctk.CTkFrame(custom_frame, fg_color="transparent")
        self.custom_rules_container.pack(fill="x", padx=20, pady=(0,15))

        self.refresh_custom_rules()

        # === DATA MANAGEMENT ===
        data_header = ctk.CTkLabel(
            scroll_frame,
            text="💾 Data Management",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        data_header.grid(row=11, column=0, sticky="w", padx=20, pady=(20,5))

        data_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        data_frame.grid(row=12, column=0, sticky="ew", padx=10, pady=5)

        buttons_frame = ctk.CTkFrame(data_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=15)

        export_btn = ctk.CTkButton(
            buttons_frame,
            text="📤 Export to CSV",
            command=self.export_data_dialog,
            width=150
        )
        export_btn.pack(side="left", padx=5)

        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Clear All Data",
            command=self.clear_data_dialog,
            width=150,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        clear_btn.pack(side="left", padx=5)

        # Save button
        save_button = ctk.CTkButton(
            scroll_frame,
            text="💾 Save All Settings",
            command=self.save_settings,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#4caf50",
            hover_color="#45a049"
        )
        save_button.grid(row=13, column=0, sticky="ew", padx=20, pady=30)

    def toggle_tracking(self):
        """Toggle tracking on/off"""
        if self.is_tracking:
            self.stop_tracking()
        else:
            self.start_tracking()

    def start_tracking(self):
        """Start tracking"""
        self.is_tracking = True
        self.track_button.configure(text="⏸️ Pause", fg_color="#ff5722", hover_color="#e64a19")
        self.status_label.configure(text="▶️ Tracking Active")

        # Start tracking in background thread
        self.tracking_thread = threading.Thread(target=self.run_tracker, daemon=True)
        self.tracking_thread.start()

    def stop_tracking(self):
        """Stop tracking"""
        self.is_tracking = False
        self.tracker.is_paused = True
        self.track_button.configure(text="▶️ Start Tracking", fg_color="#4caf50", hover_color="#45a049")
        self.status_label.configure(text="⏸️ Not Tracking")

        # Save data
        self.tracker.stop_tracking()

    def run_tracker(self):
        """Background tracking loop"""
        try:
            logger.info("Starting tracking loop")
            self.tracker.is_paused = False
            self.tracker.session_start = datetime.now()

            while self.is_tracking:
                try:
                    # Check idle
                    idle_time = self.tracker.get_idle_time()

                    if idle_time < self.tracker.idle_threshold:
                        app = self.tracker.get_active_window()

                        if app and app != "Unknown":
                            # Check focus mode
                            if self.tracker.is_app_blocked(app):
                                self.tracker.send_notification(
                                    "🚫 Blocked App",
                                    f"{app[:30]} is blocked in focus mode"
                                )
                                import time
                                time.sleep(5)
                                continue

                            if self.tracker.current_app == app:
                                elapsed = self.tracker.get_current_elapsed_time()
                                if elapsed >= 5:
                                    self.tracker.record_time(app, elapsed, self.tracker.current_project)
                                    self.tracker.start_time = self.tracker.get_time()
                                    self.tracker.save_data()
                            else:
                                if self.tracker.current_app:
                                    elapsed = self.tracker.get_current_elapsed_time()
                                    self.tracker.record_time(self.tracker.current_app, elapsed, self.tracker.current_project)

                                self.tracker.current_app = app
                                self.tracker.start_time = self.tracker.get_time()
                                logger.debug(f"Now tracking: {app[:60]}")
                    else:
                        if self.tracker.current_app:
                            logger.debug("User idle, pausing tracking")
                            self.tracker.current_app = None
                            self.tracker.start_time = None

                except Exception as e:
                    logger.error(f"Error in tracking loop iteration: {e}", exc_info=True)
                    self.last_error = str(e)

                import time
                time.sleep(5)

        except Exception as e:
            logger.error(f"Critical tracking error: {e}", exc_info=True)
            self.last_error = str(e)
            self.tracker.send_notification("⚠️ Tracking Error", "Tracking stopped due to error. Check logs.")

    def update_analytics(self, _):
        """Update analytics tab with data"""
        try:
            range_val = self.analytics_range_var.get()

            # Determine date range
            from datetime import datetime, timedelta
            today = datetime.now()

            if range_val == "Today":
                dates = [today.strftime("%Y-%m-%d")]
            elif range_val == "Week":
                dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
            elif range_val == "Month":
                dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
            else:  # All Time
                dates = list(self.tracker.data.keys())

            # Aggregate data
            total_seconds = 0
            category_totals = {}
            app_totals = {}
            productive_seconds = 0

            for date in dates:
                if date not in self.tracker.data:
                    continue
                for category, cat_data in self.tracker.data[date].items():
                    if category == "streaks":
                        continue
                    seconds = cat_data.get("total_seconds", 0)
                    total_seconds += seconds
                    category_totals[category] = category_totals.get(category, 0) + seconds

                    # Track productive time
                    if category in self.tracker.config.get("productive_categories", []):
                        productive_seconds += seconds

                    # Track apps
                    for app, app_secs in cat_data.get("apps", {}).items():
                        app_totals[app] = app_totals.get(app, 0) + app_secs

            # Update total time
            total_hours = total_seconds / 3600
            self.analytics_total_label.configure(text=f"{total_hours:.1f}h")

            # Update productivity score
            prod_score = (productive_seconds / total_seconds * 100) if total_seconds > 0 else 0
            self.analytics_prod_label.configure(text=f"{prod_score:.0f}%")
            if prod_score >= 70:
                self.analytics_prod_label.configure(text_color="#4caf50")
            elif prod_score >= 40:
                self.analytics_prod_label.configure(text_color="#ff9800")
            else:
                self.analytics_prod_label.configure(text_color="#f44336")

            # Update top app
            if app_totals:
                top_app = max(app_totals.items(), key=lambda x: x[1])
                self.analytics_top_label.configure(text=top_app[0][:30])
                self.analytics_top_hours.configure(text=f"{top_app[1]/3600:.1f}h")
            else:
                self.analytics_top_label.configure(text="None")
                self.analytics_top_hours.configure(text="0.0h")

            # Update category breakdown
            for widget in self.analytics_categories.winfo_children():
                widget.destroy()

            if category_totals:
                for category, seconds in sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:8]:
                    frame = ctk.CTkFrame(self.analytics_categories, fg_color="transparent")
                    frame.pack(fill="x", pady=3)

                    ctk.CTkLabel(
                        frame,
                        text=category,
                        font=ctk.CTkFont(size=13),
                        width=120,
                        anchor="w"
                    ).pack(side="left")

                    hours = seconds / 3600
                    percentage = (seconds / total_seconds * 100) if total_seconds > 0 else 0

                    progress = ctk.CTkProgressBar(frame, width=150)
                    progress.pack(side="left", padx=10)
                    progress.set(min(percentage / 100, 1.0))

                    ctk.CTkLabel(
                        frame,
                        text=f"{hours:.1f}h ({percentage:.0f}%)",
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    ).pack(side="left")
            else:
                ctk.CTkLabel(
                    self.analytics_categories,
                    text="No data for selected range",
                    text_color="gray"
                ).pack(pady=20)

            # Update top apps
            for widget in self.analytics_apps.winfo_children():
                widget.destroy()

            if app_totals:
                for i, (app, seconds) in enumerate(sorted(app_totals.items(), key=lambda x: x[1], reverse=True)[:10], 1):
                    frame = ctk.CTkFrame(self.analytics_apps, fg_color="transparent")
                    frame.pack(fill="x", pady=2)

                    ctk.CTkLabel(
                        frame,
                        text=f"{i}.",
                        font=ctk.CTkFont(size=12),
                        width=20
                    ).pack(side="left")

                    ctk.CTkLabel(
                        frame,
                        text=app[:25],
                        font=ctk.CTkFont(size=12),
                        anchor="w"
                    ).pack(side="left", fill="x", expand=True)

                    ctk.CTkLabel(
                        frame,
                        text=f"{seconds/3600:.1f}h",
                        font=ctk.CTkFont(size=12),
                        text_color="gray"
                    ).pack(side="right")
            else:
                ctk.CTkLabel(
                    self.analytics_apps,
                    text="No data",
                    text_color="gray"
                ).pack(pady=20)

            # Update trend (text-based bar chart)
            for widget in self.analytics_trend.winfo_children():
                widget.destroy()

            if range_val in ["Week", "Month"]:
                display_dates = dates[:14] if range_val == "Month" else dates
                daily_totals = []
                for date in reversed(display_dates):
                    if date in self.tracker.data:
                        day_total = sum(cat.get("total_seconds", 0) for cat in self.tracker.data[date].values() if isinstance(cat, dict))
                        daily_totals.append((date, day_total))
                    else:
                        daily_totals.append((date, 0))

                max_seconds = max([s for _, s in daily_totals], default=1)

                for date, seconds in daily_totals:
                    frame = ctk.CTkFrame(self.analytics_trend, fg_color="transparent")
                    frame.pack(fill="x", pady=2)

                    # Date label
                    date_obj = datetime.strptime(date, "%Y-%m-%d")
                    date_label = date_obj.strftime("%m/%d") if range_val == "Month" else date_obj.strftime("%a")

                    ctk.CTkLabel(
                        frame,
                        text=date_label,
                        font=ctk.CTkFont(size=11),
                        width=40
                    ).pack(side="left")

                    # Bar
                    progress = ctk.CTkProgressBar(frame, width=300)
                    progress.pack(side="left", padx=10)
                    progress.set(seconds / max_seconds if max_seconds > 0 else 0)

                    # Hours
                    ctk.CTkLabel(
                        frame,
                        text=f"{seconds/3600:.1f}h",
                        font=ctk.CTkFont(size=11),
                        text_color="gray",
                        width=50
                    ).pack(side="left")
            else:
                ctk.CTkLabel(
                    self.analytics_trend,
                    text="Select Week or Month to view trend",
                    text_color="gray"
                ).pack(pady=20)

        except Exception as e:
            print(f"Analytics update error: {e}")
            import traceback
            traceback.print_exc()

    def update_dashboard(self):
        """Update dashboard with current stats"""
        if not hasattr(self, 'current_app_label'):
            self.after(1000, self.update_dashboard)
            return

        try:
            # Update health indicator
            if self.last_error:
                self.health_indicator.configure(text="⚠", text_color="#ff9800")
            else:
                self.health_indicator.configure(text="✓", text_color="#4caf50")

            stats = self.tracker.get_session_stats()

            # Update current activity
            if self.tracker.current_app:
                self.current_app_label.configure(text=self.tracker.current_app[:50])
                duration = stats.get("current_app_time", 0)
                mins = int(duration // 60)
                secs = int(duration % 60)
                self.current_duration_label.configure(text=f"{mins}m {secs}s")

                category = self.tracker.categorize_app(self.tracker.current_app)
                self.current_category_label.configure(text=f"Category: {category}")
            else:
                self.current_app_label.configure(text="Idle")
                self.current_duration_label.configure(text="0m 0s")
                self.current_category_label.configure(text="Category: None")

            # Update total time
            total_hours = stats.get("today_total", 0) / 3600
            self.total_time_label.configure(text=f"{total_hours:.1f}h")

            # Update streak
            streak = self.tracker.data.get("streaks", {}).get("current", 0)
            self.streak_label.configure(text=f"{streak} days")

            # Update categories
            self.update_category_bars(stats.get("today_by_category", {}))

            # Update focus mode status
            if hasattr(self, 'focus_status_label'):
                if self.tracker.focus_mode:
                    self.focus_status_label.configure(text="🎯 Active", text_color="#4caf50")
                    self.focus_button.configure(text="⏸️ Deactivate Focus Mode")
                else:
                    self.focus_status_label.configure(text="Inactive", text_color="gray")
                    self.focus_button.configure(text="🎯 Activate Focus Mode")

        except Exception as e:
            logger.error(f"Dashboard update error: {e}", exc_info=True)
            self.last_error = str(e)

        # Schedule next update
        self.after(2000, self.update_dashboard)

    def update_category_bars(self, categories):
        """Update category progress bars"""
        # Clear existing
        for widget in self.category_container.winfo_children():
            widget.destroy()

        if not categories:
            ctk.CTkLabel(
                self.category_container,
                text="No data yet today",
                text_color="gray"
            ).pack(pady=20)
            return

        # Sort by time
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)

        for category, hours in sorted_categories[:5]:  # Top 5
            frame = ctk.CTkFrame(self.category_container, fg_color="transparent")
            frame.pack(fill="x", pady=5)

            # Category name and time
            header = ctk.CTkFrame(frame, fg_color="transparent")
            header.pack(fill="x")

            ctk.CTkLabel(
                header,
                text=category,
                font=ctk.CTkFont(size=13, weight="bold")
            ).pack(side="left")

            ctk.CTkLabel(
                header,
                text=f"{hours:.1f}h",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            ).pack(side="right")

            # Progress bar
            progress = ctk.CTkProgressBar(frame, height=8)
            progress.pack(fill="x", pady=(2,0))

            # Calculate progress (max 8 hours)
            progress_value = min(hours / 8.0, 1.0)
            progress.set(progress_value)

    def toggle_theme(self):
        """Toggle between dark and light theme"""
        self.is_dark_mode = not self.is_dark_mode
        mode = "dark" if self.is_dark_mode else "light"
        ctk.set_appearance_mode(mode)
        self.theme_button.configure(text="🌙" if self.is_dark_mode else "☀️")

    def toggle_focus_mode(self):
        """Toggle focus mode"""
        self.tracker.focus_mode = not self.tracker.focus_mode

        # Save focus mode state to config for persistence
        self.tracker.config["focus_mode_active"] = self.tracker.focus_mode
        self.tracker.save_config()

        status = "activated" if self.tracker.focus_mode else "deactivated"
        self.tracker.send_notification("🎯 Focus Mode", f"Focus mode {status}")

        # Update UI immediately
        if hasattr(self, 'focus_status_label'):
            if self.tracker.focus_mode:
                self.focus_status_label.configure(text="🎯 Active", text_color="#4caf50")
                self.focus_button.configure(text="⏸️ Deactivate Focus Mode", fg_color="#ff5722", hover_color="#e64a19")
            else:
                self.focus_status_label.configure(text="Inactive", text_color="gray")
                self.focus_button.configure(text="🎯 Activate Focus Mode", fg_color=("#3B8ED0", "#1F6AA5"), hover_color=("#36719F", "#144870"))

    def add_goal_dialog(self):
        """Show dialog to add new goal"""
        dialog = ctk.CTkInputDialog(
            text="Enter category name:",
            title="Add New Goal"
        )
        category = dialog.get_input()

        if category:
            dialog2 = ctk.CTkInputDialog(
                text=f"Enter daily goal (hours) for {category}:",
                title="Set Goal"
            )
            hours = dialog2.get_input()

            if hours:
                try:
                    hours_float = float(hours)
                    if "goals" not in self.tracker.config:
                        self.tracker.config["goals"] = {}
                    self.tracker.config["goals"][category] = hours_float
                    self.tracker.save_config()
                    self.refresh_goals()
                    messagebox.showinfo("Success", f"Goal set: {category} = {hours_float}h/day")
                except ValueError:
                    messagebox.showerror("Error", "Invalid number")

    def refresh_goals(self):
        """Refresh goals display with categories and delete buttons"""
        # Clear existing
        for widget in self.goals_container.winfo_children():
            widget.destroy()

        goals = self.tracker.config.get("goals", {})
        if not goals:
            ctk.CTkLabel(
                self.goals_container,
                text="No goals set yet",
                text_color="gray",
                font=ctk.CTkFont(size=14)
            ).grid(row=0, column=0, columnspan=2, pady=40)
            return

        # Categorize goals
        productive_categories = self.tracker.config.get("productive_categories", ["Coding", "Productivity", "Education"])
        productive_goals = {}
        entertainment_goals = {}
        other_goals = {}

        for category, hours in goals.items():
            if category in productive_categories:
                productive_goals[category] = hours
            elif category in ["Entertainment", "Social Media", "Browsing"]:
                entertainment_goals[category] = hours
            else:
                other_goals[category] = hours

        # Get today's stats for progress
        today = datetime.now().strftime("%Y-%m-%d")
        today_stats = {}
        if today in self.tracker.data:
            for category, data in self.tracker.data[today].items():
                if category != "streaks":
                    today_stats[category] = data.get("total_seconds", 0) / 3600

        # Display by category groups
        row = 0

        # Productive goals
        if productive_goals:
            header = ctk.CTkLabel(
                self.goals_container,
                text="💼 Productive Goals",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            header.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(10,5))
            row += 1

            for i, (category, goal_hours) in enumerate(sorted(productive_goals.items())):
                col = i % 2
                if i > 0 and col == 0:
                    row += 1

                self._create_goal_card(category, goal_hours, today_stats.get(category, 0), row, col)

            row += 1

        # Entertainment goals
        if entertainment_goals:
            header = ctk.CTkLabel(
                self.goals_container,
                text="🎮 Entertainment Goals",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            header.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(10,5))
            row += 1

            for i, (category, goal_hours) in enumerate(sorted(entertainment_goals.items())):
                col = i % 2
                if i > 0 and col == 0:
                    row += 1

                self._create_goal_card(category, goal_hours, today_stats.get(category, 0), row, col)

            row += 1

        # Other goals
        if other_goals:
            header = ctk.CTkLabel(
                self.goals_container,
                text="📂 Other Goals",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            header.grid(row=row, column=0, columnspan=2, sticky="w", padx=10, pady=(10,5))
            row += 1

            for i, (category, goal_hours) in enumerate(sorted(other_goals.items())):
                col = i % 2
                if i > 0 and col == 0:
                    row += 1

                self._create_goal_card(category, goal_hours, today_stats.get(category, 0), row, col)

    def _create_goal_card(self, category, goal_hours, current_hours, row, col):
        """Create a goal card with progress and delete button"""
        goal_frame = ctk.CTkFrame(self.goals_container, corner_radius=10)
        goal_frame.grid(row=row, column=col, sticky="nsew", padx=10, pady=10)

        # Header with category and delete button
        header_frame = ctk.CTkFrame(goal_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15,5))

        ctk.CTkLabel(
            header_frame,
            text=category,
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        delete_btn = ctk.CTkButton(
            header_frame,
            text="🗑️",
            command=lambda c=category: self.delete_goal(c),
            width=30,
            height=30,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        delete_btn.pack(side="right")

        # Goal info
        ctk.CTkLabel(
            goal_frame,
            text=f"Goal: {goal_hours}h/day",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        ).pack(padx=20, pady=5)

        # Progress
        progress_pct = (current_hours / goal_hours * 100) if goal_hours > 0 else 0
        progress_bar = ctk.CTkProgressBar(goal_frame, width=200)
        progress_bar.pack(padx=20, pady=5)
        progress_bar.set(min(progress_pct / 100, 1.0))

        # Current progress text
        status_text = f"{current_hours:.1f}h / {goal_hours}h today"
        if progress_pct >= 100:
            status_color = "#4caf50"
            status_text += " ✓"
        elif progress_pct >= 75:
            status_color = "#ff9800"
        else:
            status_color = "gray"

        ctk.CTkLabel(
            goal_frame,
            text=status_text,
            font=ctk.CTkFont(size=12),
            text_color=status_color
        ).pack(padx=20, pady=(0,15))

    def delete_goal(self, category):
        """Delete a goal"""
        if messagebox.askyesno("Delete Goal", f"Are you sure you want to delete the goal for '{category}'?"):
            if "goals" in self.tracker.config and category in self.tracker.config["goals"]:
                del self.tracker.config["goals"][category]
                self.tracker.save_config()
                self.refresh_goals()
                messagebox.showinfo("Success", f"Goal for '{category}' deleted")

    def add_project_dialog(self):
        """Show dialog to add new project"""
        dialog = ctk.CTkInputDialog(
            text="Enter project name:",
            title="Add New Project"
        )
        project = dialog.get_input()

        if project:
            if "projects" not in self.tracker.config:
                self.tracker.config["projects"] = {}
            self.tracker.config["projects"][project] = {"created": datetime.now().strftime("%Y-%m-%d")}
            self.tracker.save_config()

            # Update dropdown
            projects = list(self.tracker.config.get("projects", {}).keys())
            self.project_dropdown.configure(values=["None"] + projects)
            self.project_var.set(project)
            self.tracker.current_project = project

            messagebox.showinfo("Success", f"Project '{project}' created")

    def change_project(self, choice):
        """Change current project"""
        if choice == "None":
            self.tracker.current_project = None
        else:
            self.tracker.current_project = choice

    def refresh_custom_rules(self):
        """Refresh custom category rules display"""
        for widget in self.custom_rules_container.winfo_children():
            widget.destroy()

        custom_categories = self.tracker.config.get("custom_categories", {})
        if not custom_categories:
            ctk.CTkLabel(
                self.custom_rules_container,
                text="No custom rules. Click 'Add Rule' to create one.",
                text_color="gray",
                font=ctk.CTkFont(size=12)
            ).pack(pady=10)
            return

        for pattern, category in custom_categories.items():
            rule_frame = ctk.CTkFrame(self.custom_rules_container, fg_color="transparent")
            rule_frame.pack(fill="x", pady=2)

            ctk.CTkLabel(
                rule_frame,
                text=f"'{pattern}' → {category}",
                font=ctk.CTkFont(size=12)
            ).pack(side="left")

            delete_btn = ctk.CTkButton(
                rule_frame,
                text="✖",
                command=lambda p=pattern: self.delete_custom_rule(p),
                width=25,
                height=25,
                fg_color="#f44336",
                hover_color="#d32f2f"
            )
            delete_btn.pack(side="right")

    def add_custom_category_rule(self):
        """Add a custom category rule"""
        dialog = ctk.CTkInputDialog(
            text="Enter app name pattern (e.g., 'figma', 'notion'):",
            title="Add Custom Rule"
        )
        pattern = dialog.get_input()

        if pattern:
            dialog2 = ctk.CTkInputDialog(
                text=f"Enter category for '{pattern}':",
                title="Set Category"
            )
            category = dialog2.get_input()

            if category:
                if "custom_categories" not in self.tracker.config:
                    self.tracker.config["custom_categories"] = {}
                self.tracker.config["custom_categories"][pattern] = category
                self.tracker.save_config()
                self.refresh_custom_rules()
                messagebox.showinfo("Success", f"Rule added: '{pattern}' → {category}")

    def delete_custom_rule(self, pattern):
        """Delete a custom category rule"""
        if "custom_categories" in self.tracker.config:
            del self.tracker.config["custom_categories"][pattern]
            self.tracker.save_config()
            self.refresh_custom_rules()

    def export_data_dialog(self):
        """Export data to CSV"""
        try:
            from tkinter import filedialog
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile="time_tracking_export.csv"
            )
            if filename:
                self.tracker.export_csv(filename)
                messagebox.showinfo("Success", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

    def clear_data_dialog(self):
        """Clear all tracking data"""
        if messagebox.askyesno(
            "Clear All Data",
            "Are you sure you want to delete ALL tracking data? This cannot be undone!",
            icon="warning"
        ):
            confirm = messagebox.askyesno(
                "Final Confirmation",
                "This will permanently delete all your time tracking history. Continue?",
                icon="warning"
            )
            if confirm:
                self.tracker.data = {"streaks": {"current": 0, "longest": 0, "last_date": None}}
                self.tracker.save_data()
                messagebox.showinfo("Success", "All data has been cleared")
                self.update_dashboard()

    def save_settings(self):
        """Save all settings"""
        try:
            # Update config
            self.tracker.config["idle_threshold_seconds"] = int(self.idle_entry.get())
            self.tracker.idle_threshold = int(self.idle_entry.get())

            self.tracker.config["break_reminder_interval"] = int(self.break_entry.get())
            self.tracker.config["notifications_enabled"] = self.notif_var.get()

            # Save default theme
            self.tracker.config["default_theme"] = self.default_theme_var.get()

            # Save excluded apps
            excluded_text = self.excluded_entry.get().strip()
            if excluded_text:
                self.tracker.config["excluded_apps"] = [app.strip() for app in excluded_text.split(",")]
            else:
                self.tracker.config["excluded_apps"] = []

            self.tracker.save_config()
            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid number format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {str(e)}")

    def on_closing(self):
        """Handle window closing"""
        if self.is_tracking:
            if messagebox.askokcancel("Quit", "Tracking is active. Stop tracking and quit?"):
                self.stop_tracking()
                self.destroy()
        else:
            self.destroy()


# Helper method additions for tracker
def get_current_elapsed_time(tracker_self):
    """Get elapsed time for current app"""
    if tracker_self.start_time:
        import time
        return time.time() - tracker_self.start_time
    return 0

def get_time(tracker_self):
    """Get current time"""
    import time
    return time.time()

# Monkey patch the methods
TimeTracker.get_current_elapsed_time = get_current_elapsed_time
TimeTracker.get_time = get_time


def main():
    """Main entry point"""
    app = TimeTrackerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
