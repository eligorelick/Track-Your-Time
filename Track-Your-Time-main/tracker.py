import time
import json
from datetime import datetime, timedelta
from collections import defaultdict
import os
import sys
import csv
import threading
import hashlib
import base64
from pathlib import Path
import re

# Platform-specific imports
import platform
system = platform.system()

if system == "Windows":
    import win32gui
    import win32process
    import psutil
    import ctypes
    try:
        from plyer import notification
        from pystray import Icon, Menu, MenuItem
        from PIL import Image, ImageDraw
        HAS_TRAY = True
    except ImportError:
        HAS_TRAY = False
elif system == "Darwin":  # macOS
    from AppKit import NSWorkspace
    import Quartz
    try:
        from plyer import notification
        from pystray import Icon, Menu, MenuItem
        from PIL import Image, ImageDraw
        HAS_TRAY = True
    except ImportError:
        HAS_TRAY = False
elif system == "Linux":
    import subprocess
    try:
        from plyer import notification
        from pystray import Icon, Menu, MenuItem
        from PIL import Image, ImageDraw
        HAS_TRAY = True
    except ImportError:
        HAS_TRAY = False

class TimeTracker:
    def __init__(self, data_file="time_tracking.json", config_file="tracker_config.json"):
        self.data_file = data_file
        self.config_file = config_file
        self.data = self.load_data()
        self.config = self.load_config()
        self.current_app = None
        self.start_time = None
        self.last_activity_time = time.time()
        self.idle_threshold = self.config.get("idle_threshold_seconds", 300)

        # New features
        self.is_paused = False
        self.current_project = None
        self.session_start = datetime.now()
        self.last_notification_time = {}
        self.pomodoro_state = {"active": False, "work_time": 25*60, "break_time": 5*60, "cycles": 0}
        self.focus_mode = False
        self.unknown_apps = set()
        self.tray_icon = None
        self.password_hash = self.config.get("password_hash", None)

        # Initialize streaks
        if "streaks" not in self.data:
            self.data["streaks"] = {"current": 0, "longest": 0, "last_date": None}
        
    def load_data(self):
        """Load existing tracking data"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                return json.load(f)
        return {}

    def save_data(self):
        """Save tracking data to file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def load_config(self):
        """Load configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        # Default config
        default_config = {
            "idle_threshold_seconds": 300,
            "goals": {
                "Coding": 4,
                "Entertainment": 2
            },
            "custom_categories": {},
            "excluded_apps": [],
            "focus_mode_blocked": ["facebook", "twitter", "instagram", "tiktok", "youtube", "netflix", "game"],
            "break_reminder_interval": 3600,  # 1 hour
            "pomodoro_enabled": False,
            "notifications_enabled": True,
            "auto_start": False,
            "email_reports": {"enabled": False, "email": "", "frequency": "weekly"},
            "password_hash": None,
            "encryption_enabled": False,
            "productive_categories": ["Coding", "Productivity", "Education"],
            "projects": {}
        }
        self.save_config(default_config)
        return default_config

    def save_config(self, config=None):
        """Save configuration"""
        if config is None:
            config = self.config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_active_window_windows(self):
        """Get active window name on Windows"""
        try:
            window = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(window)
            process = psutil.Process(pid)
            app_name = process.name()
            window_title = win32gui.GetWindowText(window)
            return f"{app_name} - {window_title}"
        except:
            return "Unknown"
    
    def get_active_window_mac(self):
        """Get active window name on macOS"""
        try:
            active_app = NSWorkspace.sharedWorkspace().activeApplication()
            app_name = active_app['NSApplicationName']
            return app_name
        except:
            return "Unknown"
    
    def get_active_window_linux(self):
        """Get active window name on Linux"""
        try:
            result = subprocess.run(
                ['xdotool', 'getactivewindow', 'getwindowname'],
                capture_output=True, text=True
            )
            return result.stdout.strip()
        except:
            return "Unknown"
    
    def get_active_window(self):
        """Get active window based on OS"""
        if system == "Windows":
            return self.get_active_window_windows()
        elif system == "Darwin":
            return self.get_active_window_mac()
        elif system == "Linux":
            return self.get_active_window_linux()
        return "Unknown"
    
    def get_idle_time(self):
        """Get system idle time in seconds"""
        if system == "Windows":
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_uint)]

            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
            millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return millis / 1000.0
        elif system == "Darwin":
            return Quartz.CGEventSourceSecondsSinceLastEventType(
                Quartz.kCGEventSourceStateCombinedSessionState,
                Quartz.kCGAnyInputEventType
            )
        else:
            # Linux - approximate using xprintidle if available
            try:
                result = subprocess.run(['xprintidle'], capture_output=True, text=True)
                return int(result.stdout.strip()) / 1000.0
            except:
                return 0

    def categorize_app(self, app_name):
        """Categorize apps into groups with extensive recognition"""
        app_lower = app_name.lower()

        # Check custom categories first
        for pattern, category in self.config.get("custom_categories", {}).items():
            if pattern.lower() in app_lower:
                return category

        # ============ CODING & DEVELOPMENT ============
        coding_keywords = [
            # IDEs
            'vscode', 'visual studio code', 'pycharm', 'intellij', 'webstorm', 'phpstorm',
            'goland', 'rider', 'clion', 'datagrip', 'rubymine', 'appcode',
            'eclipse', 'netbeans', 'android studio', 'xcode', 'sublime', 'atom',
            'brackets', 'notepad++', 'vim', 'emacs', 'nano', 'gedit',
            'code.exe', 'code - insiders',
            # Specialized editors
            'jupyter', 'spyder', 'rstudio', 'matlab', 'octave',
            'postman', 'insomnia', 'swagger',
            # Terminal/Command line
            'terminal', 'iterm', 'cmd.exe', 'powershell', 'wsl', 'bash', 'zsh',
            'windows terminal', 'hyper', 'alacritty', 'kitty', 'terminator',
            'putty', 'winscp', 'filezilla',
            # Version control
            'gitkraken', 'sourcetree', 'github desktop', 'tower', 'smartgit',
            'tortoisegit', 'git gui',
            # Database tools
            'dbeaver', 'mysql workbench', 'pgadmin', 'sequel pro', 'tableplus',
            'mongodb compass', 'redis', 'robo 3t',
            # Dev tools
            'docker', 'kubernetes', 'vagrant', 'virtualbox', 'vmware',
            'wireshark', 'fiddler', 'charles proxy',
        ]

        if any(x in app_lower for x in coding_keywords):
            return "Coding"

        # ============ BROWSERS (with detailed detection) ============
        browser_keywords = ['chrome', 'firefox', 'safari', 'edge', 'brave', 'opera',
                           'vivaldi', 'arc', 'chromium', 'iexplore', 'internet explorer']

        if any(x in app_lower for x in browser_keywords):
            # Development/Learning sites
            if any(x in app_lower for x in [
                'github', 'gitlab', 'bitbucket', 'stackoverflow', 'stack overflow',
                'leetcode', 'hackerrank', 'codepen', 'codesandbox', 'repl.it', 'jsfiddle',
                'glitch', 'stackblitz', 'playcode', 'codeanywhere',
                'mdn', 'w3schools', 'devdocs', 'docs.python', 'docs.microsoft',
                'developer.mozilla', 'documentation', 'api reference', 'tutorial',
                'udemy', 'coursera', 'edx', 'pluralsight', 'skillshare', 'freecodecamp',
                'khan academy', 'codecademy', 'udacity', 'egghead', 'frontend masters',
                'laracasts', 'treehouse', 'lynda', 'datacamp', 'educative',
                # Dev tools sites
                'vercel', 'netlify', 'heroku', 'railway', 'render', 'fly.io',
                'aws console', 'azure portal', 'google cloud', 'digitalocean',
                'cloudflare', 'mongodb atlas', 'supabase', 'planetscale',
                'sentry', 'datadog', 'new relic', 'grafana', 'prometheus',
            ]):
                return "Coding"

            # Social Media
            elif any(x in app_lower for x in [
                'facebook', 'twitter', 'instagram', 'tiktok', 'snapchat',
                'reddit', 'pinterest', 'tumblr', 'linkedin', 'mastodon',
                'threads', 'bluesky', 'whatsapp web', 'telegram web',
            ]):
                return "Social Media"

            # Entertainment/Streaming
            elif any(x in app_lower for x in [
                'youtube', 'netflix', 'twitch', 'hulu', 'disney', 'prime video',
                'spotify', 'soundcloud', 'apple music', 'pandora', 'tidal',
                'crunchyroll', 'funimation', 'hbo', 'peacock', 'paramount',
            ]):
                return "Entertainment"

            # News & Reading
            elif any(x in app_lower for x in [
                'news', 'bbc', 'cnn', 'nytimes', 'guardian', 'reuters', 'medium',
                'substack', 'forbes', 'techcrunch', 'hacker news', 'ycombinator',
                'wikipedia', 'wikihow',
            ]):
                return "Reading"

            # Shopping
            elif any(x in app_lower for x in [
                'amazon', 'ebay', 'etsy', 'aliexpress', 'walmart', 'target',
                'shop', 'store', 'cart', 'checkout',
            ]):
                return "Shopping"

            # Productivity/Tools
            elif any(x in app_lower for x in [
                'gmail', 'outlook', 'calendar', 'google docs', 'google sheets',
                'google drive', 'dropbox', 'notion', 'todoist', 'trello',
                'asana', 'jira', 'monday.com', 'clickup', 'linear', 'airtable',
                'coda', 'miro', 'figma', 'figjam', 'whimsical', 'lucidchart',
                'canva - edit', 'excalidraw', 'obsidian publish',
            ]):
                return "Productivity"

            # General browsing
            return "Browsing"

        # ============ COMMUNICATION ============
        communication_keywords = [
            # Messaging/Chat
            'slack', 'discord', 'teams', 'microsoft teams', 'zoom', 'skype',
            'telegram', 'whatsapp', 'signal', 'element', 'matrix',
            'messenger', 'wechat', 'line', 'viber', 'groupme', 'rocketchat',
            'mattermost', 'zulip', 'gitter', 'chanty', 'flock',
            # Email clients
            'thunderbird', 'outlook', 'mail', 'spark', 'mailspring',
            'mailbird', 'em client', 'postbox', 'claws mail',
            # Video conferencing
            'webex', 'gotomeeting', 'bluejeans', 'jitsi', 'meet',
            'facetime', 'google meet', 'whereby', 'around', 'mmhmm',
            'discord - voice', 'hangouts',
        ]

        if any(x in app_lower for x in communication_keywords):
            return "Communication"

        # ============ PRODUCTIVITY & OFFICE ============
        productivity_keywords = [
            # Microsoft Office
            'word', 'winword', 'excel', 'powerpoint', 'onenote', 'access',
            'publisher', 'outlook', 'microsoft 365', 'office', 'teams - calendar',
            # Google Workspace
            'google docs', 'google sheets', 'google slides', 'google drive',
            'google calendar', 'google keep',
            # Apple
            'pages', 'numbers', 'keynote', 'reminders',
            # Other office suites
            'libreoffice', 'openoffice', 'wps office', 'calligra', 'onlyoffice',
            # Note-taking & Knowledge Management
            'notion', 'obsidian', 'evernote', 'onenote', 'simplenote',
            'bear', 'roam', 'logseq', 'joplin', 'standard notes', 'remnote',
            'typora', 'mark text', 'notable', 'craft', 'amplenote', 'mem',
            'reflect', 'tana', 'capacities', 'anytype',
            # PDF
            'acrobat', 'pdf', 'foxit', 'preview', 'sumatra', 'pdf-xchange',
            # Project management
            'trello', 'asana', 'monday', 'clickup', 'basecamp', 'notion calendar',
            'jira', 'confluence', 'linear', 'height', 'shortcut', 'pivotal tracker',
            'youtrack', 'airtable', 'smartsheet', 'wrike', 'teamwork',
            # Task Management
            'todoist', 'things', 'any.do', 'microsoft to do', 'ticktick',
            'omnifocus', 'taskwarrior', '2do', 'remember the milk',
            # Spreadsheets/Data
            'airtable', 'coda', 'excel', 'notion database', 'fibery',
            # Time Management
            'toggl', 'rescuetime', 'timely', 'clockify', 'harvest',
            # Collaboration
            'miro', 'mural', 'figjam', 'whimsical', 'lucidchart', 'draw.io',
            'excalidraw', 'tldraw',
        ]

        if any(x in app_lower for x in productivity_keywords):
            return "Productivity"

        # ============ DESIGN & CREATIVE ============
        design_keywords = [
            # Photo/Image editing
            'photoshop', 'illustrator', 'indesign', 'lightroom', 'acrobat',
            'gimp', 'inkscape', 'krita', 'affinity photo', 'affinity designer',
            'sketch', 'figma', 'adobe xd', 'invision', 'framer', 'pixelmator',
            'paint.net', 'paintshop', 'corel draw', 'canva', 'penpot',
            'lunacy', 'photopea', 'fotor', 'pixlr',
            # Video editing
            'premiere', 'after effects', 'davinci resolve', 'final cut',
            'imovie', 'filmora', 'camtasia', 'shotcut', 'kdenlive',
            'vegas', 'avid', 'blender', 'olive', 'openshot',
            # 3D modeling
            'maya', 'cinema 4d', 'zbrush', 'houdini', '3ds max',
            'unity', 'unreal', 'godot', 'substance painter', 'marmoset',
            # Audio
            'audacity', 'logic pro', 'ableton', 'fl studio', 'reaper',
            'pro tools', 'garage band', 'cubase', 'studio one', 'ardour',
            'lmms', 'caustic',
            # UI/UX Design
            'penpot', 'figma', 'sketch', 'axure', 'balsamiq', 'mockplus',
            'principle', 'protopie', 'flinto', 'origami studio',
        ]

        if any(x in app_lower for x in design_keywords):
            return "Design"

        # ============ ENTERTAINMENT & MEDIA ============
        entertainment_keywords = [
            # Streaming/Video
            'spotify', 'apple music', 'itunes', 'music', 'vlc', 'windows media',
            'quicktime', 'netflix', 'youtube', 'twitch', 'hulu', 'disney+',
            'plex', 'kodi', 'jellyfin', 'emby', 'amazon prime video',
            'hbo max', 'paramount+', 'peacock', 'apple tv', 'crunchyroll',
            # Gaming platforms
            'steam', 'epic games', 'epicgameslauncher', 'gog galaxy', 'origin', 'uplay',
            'battle.net', 'battlenet', 'blizzard', 'riot client', 'riotclientservices',
            'xbox', 'playstation', 'ea app', 'rockstar games launcher',
            'bethesda launcher', 'itch.io', 'playnite',
            # Games (common ones)
            'minecraft', 'fortnite', 'valorant', 'league of legends', 'leagueoflegends',
            'dota', 'dota2', 'counter-strike', 'csgo', 'cs2', 'overwatch',
            'apex legends', 'apexlegends', 'rocket league', 'roblox', 'among us',
            'fall guys', 'wow', 'world of warcraft', 'destiny', 'call of duty',
            'gta', 'grand theft auto', 'red dead', 'elden ring', 'baldurs gate',
            'cyberpunk', 'witcher', 'skyrim', 'fallout', 'halo', 'warzone',
            'game', '.exe - ',  # catch-all for games
            # Media players
            'soundcloud', 'pandora', 'tidal', 'deezer', 'youtube music',
            'foobar2000', 'winamp', 'clementine', 'rhythmbox',
        ]

        if any(x in app_lower for x in entertainment_keywords):
            return "Entertainment"

        # ============ SOCIAL MEDIA (apps) ============
        social_keywords = [
            'facebook', 'twitter', 'instagram', 'tiktok', 'snapchat',
            'reddit', 'pinterest', 'linkedin', 'mastodon', 'threads',
        ]

        if any(x in app_lower for x in social_keywords):
            return "Social Media"

        # ============ EDUCATION & LEARNING ============
        education_keywords = [
            'anki', 'quizlet', 'duolingo', 'rosetta stone',
            'mathematica', 'maple', 'geogebra', 'desmos',
            'moodle', 'canvas', 'blackboard', 'schoology',
            'zoom', 'google classroom',
        ]

        if any(x in app_lower for x in education_keywords):
            return "Education"

        # ============ UTILITIES & SYSTEM ============
        utility_keywords = [
            'calculator', 'notepad', 'textedit', 'finder', 'explorer',
            'settings', 'control panel', 'system preferences',
            'task manager', 'activity monitor', 'resource monitor',
            '7-zip', 'winrar', 'winzip', 'archive utility',
            'snipping tool', 'screenshot', 'greenshot', 'lightshot',
        ]

        if any(x in app_lower for x in utility_keywords):
            return "Utilities"

        # ============ FINANCE ============
        finance_keywords = [
            'quickbooks', 'quicken', 'mint', 'ynab', 'personal capital',
            'coinbase', 'robinhood', 'webull', 'etrade', 'fidelity',
            'paypal', 'venmo', 'cash app', 'crypto',
        ]

        if any(x in app_lower for x in finance_keywords):
            return "Finance"

        # ============ READING & BOOKS ============
        reading_keywords = [
            'kindle', 'apple books', 'calibre', 'goodreads',
            'pocket', 'instapaper', 'readwise', 'reader',
        ]

        if any(x in app_lower for x in reading_keywords):
            return "Reading"

        return "Other"

    # ============ NEW FEATURES ============

    def set_password(self, password):
        """Set password for viewing stats"""
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()
        self.config["password_hash"] = self.password_hash
        self.save_config()

    def check_password(self, password):
        """Check if password is correct"""
        if not self.password_hash:
            return True
        return hashlib.sha256(password.encode()).hexdigest() == self.password_hash

    def send_notification(self, title, message):
        """Send system notification"""
        if not self.config.get("notifications_enabled", True):
            return
        try:
            if HAS_TRAY:
                notification.notify(title=title, message=message, timeout=10)
            else:
                print(f"📢 {title}: {message}")
        except:
            print(f"📢 {title}: {message}")

    def check_goal_notifications(self):
        """Check and send notifications for goals"""
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data:
            return

        for category, goal_hours in self.config.get("goals", {}).items():
            if category in self.data[today]:
                current_hours = self.data[today][category]["total_seconds"] / 3600

                # Notify when goal is reached
                if current_hours >= goal_hours:
                    notif_key = f"goal_{category}_{today}"
                    if notif_key not in self.last_notification_time:
                        self.send_notification(
                            "🎯 Goal Achieved!",
                            f"You've hit your {category} goal of {goal_hours}h today!"
                        )
                        self.last_notification_time[notif_key] = time.time()

                # Warn when over limit (if it's unproductive category)
                if category == "Entertainment" and current_hours > goal_hours * 1.5:
                    notif_key = f"warn_{category}_{today}"
                    if notif_key not in self.last_notification_time:
                        self.send_notification(
                            "⚠️ Limit Warning",
                            f"You've spent {current_hours:.1f}h on {category} today (limit: {goal_hours}h)"
                        )
                        self.last_notification_time[notif_key] = time.time()

    def check_break_reminder(self):
        """Remind user to take breaks"""
        interval = self.config.get("break_reminder_interval", 3600)
        if time.time() - self.session_start.timestamp() > interval:
            notif_key = f"break_{int(time.time() / interval)}"
            if notif_key not in self.last_notification_time:
                self.send_notification(
                    "💆 Take a Break!",
                    f"You've been working for {interval//60} minutes. Time for a break!"
                )
                self.last_notification_time[notif_key] = time.time()

    def update_streaks(self):
        """Update daily streaks"""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        # Check if goals were met yesterday
        last_date = self.data["streaks"].get("last_date")

        if last_date != today and yesterday in self.data:
            goals_met = True
            for category, goal_hours in self.config.get("goals", {}).items():
                if category in self.config.get("productive_categories", []):
                    actual_hours = self.data[yesterday].get(category, {}).get("total_seconds", 0) / 3600
                    if actual_hours < goal_hours:
                        goals_met = False
                        break

            if goals_met:
                if last_date == yesterday:
                    self.data["streaks"]["current"] += 1
                else:
                    self.data["streaks"]["current"] = 1

                if self.data["streaks"]["current"] > self.data["streaks"]["longest"]:
                    self.data["streaks"]["longest"] = self.data["streaks"]["current"]
                    self.send_notification(
                        "🔥 New Record!",
                        f"New longest streak: {self.data['streaks']['longest']} days!"
                    )
            else:
                if self.data["streaks"]["current"] > 0:
                    self.send_notification(
                        "💔 Streak Broken",
                        f"Your {self.data['streaks']['current']} day streak has ended"
                    )
                self.data["streaks"]["current"] = 0

            self.data["streaks"]["last_date"] = today
            self.save_data()

    def is_app_blocked(self, app_name):
        """Check if app is blocked in focus mode"""
        if not self.focus_mode:
            return False
        app_lower = app_name.lower()
        blocked = self.config.get("focus_mode_blocked", [])
        return any(blocked_app in app_lower for blocked_app in blocked)

    def log_unknown_app(self, app_name):
        """Log apps that were categorized as Other"""
        if self.categorize_app(app_name) == "Other":
            self.unknown_apps.add(app_name)

    def get_session_stats(self):
        """Get current session statistics"""
        session_duration = (datetime.now() - self.session_start).total_seconds()
        today = datetime.now().strftime("%Y-%m-%d")

        stats = {
            "session_duration": session_duration,
            "current_app": self.current_app,
            "current_app_time": time.time() - self.start_time if self.start_time else 0,
            "today_total": 0,
            "today_by_category": {}
        }

        if today in self.data:
            stats["today_total"] = sum(cat["total_seconds"] for cat in self.data[today].values())
            for category, data in self.data[today].items():
                stats["today_by_category"][category] = data["total_seconds"] / 3600

        return stats

    def display_live_dashboard(self):
        """Display real-time dashboard"""
        stats = self.get_session_stats()

        os.system('cls' if os.name == 'nt' else 'clear')
        print("="*70)
        print(" "*20 + "🕐 LIVE TRACKING DASHBOARD")
        print("="*70)

        # Current activity
        print(f"\n📍 Current Activity:")
        if self.current_app:
            current_time = stats["current_app_time"]
            category = self.categorize_app(self.current_app)
            print(f"   App: {self.current_app[:50]}")
            print(f"   Category: {category}")
            print(f"   Duration: {int(current_time//60)}m {int(current_time%60)}s")
        else:
            print("   Idle or paused")

        if self.current_project:
            print(f"   Project: {self.current_project}")

        # Session info
        print(f"\n⏱️  Session Info:")
        print(f"   Started: {self.session_start.strftime('%H:%M:%S')}")
        print(f"   Duration: {int(stats['session_duration']//3600)}h {int((stats['session_duration']%3600)//60)}m")
        if self.focus_mode:
            print(f"   🎯 FOCUS MODE ACTIVE")

        # Today's stats
        print(f"\n📊 Today's Progress:")
        total_hours = stats["today_total"] / 3600
        print(f"   Total: {total_hours:.2f}h tracked")

        for category, hours in sorted(stats["today_by_category"].items(), key=lambda x: x[1], reverse=True):
            bar_length = int(hours * 2)
            bar = "█" * min(bar_length, 30)
            goal_str = ""
            if category in self.config.get("goals", {}):
                goal = self.config["goals"][category]
                progress = (hours / goal * 100) if goal > 0 else 0
                goal_str = f" ({progress:.0f}% of {goal}h goal)"
            print(f"   {category:15} {hours:5.2f}h {bar}{goal_str}")

        # Streaks
        if self.data["streaks"]["current"] > 0:
            print(f"\n🔥 Current Streak: {self.data['streaks']['current']} days")
            print(f"   Longest Streak: {self.data['streaks']['longest']} days")

        print("\n" + "="*70)
        print("Press Ctrl+C to stop tracking")
        print("="*70)

    def create_tray_icon(self):
        """Create system tray icon"""
        if not HAS_TRAY:
            return None

        def create_image(color):
            """Create a colored dot image"""
            image = Image.new('RGB', (64, 64), color)
            dc = ImageDraw.Draw(image)
            dc.ellipse([8, 8, 56, 56], fill=color, outline='white', width=3)
            return image

        def on_quit(icon, item):
            icon.stop()
            self.stop_tracking()

        def on_pause(icon, item):
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.send_notification("⏸️ Paused", "Tracking paused")
            else:
                self.send_notification("▶️ Resumed", "Tracking resumed")

        def on_focus(icon, item):
            self.focus_mode = not self.focus_mode
            if self.focus_mode:
                self.send_notification("🎯 Focus Mode", "Focus mode activated")
            else:
                self.send_notification("🎯 Focus Mode", "Focus mode deactivated")

        menu = Menu(
            MenuItem("Pause/Resume", on_pause),
            MenuItem("Toggle Focus Mode", on_focus),
            MenuItem("Quit", on_quit)
        )

        icon = Icon("TimeTracker", create_image('green'), "Time Tracker", menu)
        return icon

    def start_tray_icon(self):
        """Start system tray icon in background thread"""
        if HAS_TRAY and self.tray_icon:
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def record_time(self, app_name, duration_seconds, project=None):
        """Record time spent on an app"""
        # Check if app is excluded
        if any(excluded in app_name.lower() for excluded in self.config.get("excluded_apps", [])):
            return

        today = datetime.now().strftime("%Y-%m-%d")
        category = self.categorize_app(app_name)

        # Log unknown apps
        self.log_unknown_app(app_name)

        # Initialize data structure
        if today not in self.data:
            self.data[today] = {}

        if category not in self.data[today]:
            self.data[today][category] = {
                "total_seconds": 0,
                "apps": {},
                "projects": {} if project else None
            }

        if app_name not in self.data[today][category]["apps"]:
            self.data[today][category]["apps"][app_name] = 0

        # Add time
        self.data[today][category]["apps"][app_name] += duration_seconds
        self.data[today][category]["total_seconds"] += duration_seconds

        # Track by project if specified
        if project and "projects" in self.data[today][category]:
            if project not in self.data[today][category]["projects"]:
                self.data[today][category]["projects"][project] = 0
            self.data[today][category]["projects"][project] += duration_seconds

    def manual_time_entry(self, app_name, category, duration_minutes, project=None, date=None):
        """Manually add time entry"""
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        if date not in self.data:
            self.data[date] = {}

        if category not in self.data[date]:
            self.data[date][category] = {
                "total_seconds": 0,
                "apps": {},
                "projects": {}
            }

        duration_seconds = duration_minutes * 60

        if app_name not in self.data[date][category]["apps"]:
            self.data[date][category]["apps"][app_name] = 0

        self.data[date][category]["apps"][app_name] += duration_seconds
        self.data[date][category]["total_seconds"] += duration_seconds

        if project:
            if project not in self.data[date][category]["projects"]:
                self.data[date][category]["projects"][project] = 0
            self.data[date][category]["projects"][project] += duration_seconds

        self.save_data()
        print(f"✅ Added {duration_minutes}min to {app_name} ({category})")

    def stop_tracking(self):
        """Gracefully stop tracking"""
        if self.current_app:
            elapsed = time.time() - self.start_time
            self.record_time(self.current_app, elapsed, self.current_project)
        self.save_data()
    
    def display_day(self, date_str):
        """Display stats for a specific day"""
        if date_str not in self.data:
            print(f"\nNo data tracked for {date_str}.")
            return

        print(f"\n{'='*60}")
        print(f"Time Tracking for {date_str}")
        print(f"{'='*60}")

        # Calculate totals
        total_seconds = sum(data["total_seconds"] for data in self.data[date_str].values())
        total_hours = total_seconds / 3600

        for category, data in sorted(self.data[date_str].items(), key=lambda x: x[1]["total_seconds"], reverse=True):
            hours = data["total_seconds"] / 3600
            percentage = (data["total_seconds"] / total_seconds * 100) if total_seconds > 0 else 0

            # Check against goals
            goal_str = ""
            if category in self.config.get("goals", {}):
                goal = self.config["goals"][category]
                if hours >= goal:
                    goal_str = f" ✓ (Goal: {goal}h)"
                else:
                    goal_str = f" (Goal: {goal}h - {goal-hours:.1f}h remaining)"

            print(f"\n{category.upper()}: {hours:.2f}h ({percentage:.1f}%){goal_str}")

            for app, seconds in sorted(data["apps"].items(), key=lambda x: x[1], reverse=True)[:5]:
                app_hours = seconds / 3600
                app_percentage = (seconds / data["total_seconds"] * 100) if data["total_seconds"] > 0 else 0
                print(f"  • {app}: {app_hours:.2f}h ({app_percentage:.1f}%)")

            if len(data["apps"]) > 5:
                print(f"  ... and {len(data['apps']) - 5} more apps")

        print(f"\n{'='*60}")
        print(f"TOTAL TIME TRACKED: {total_hours:.2f} hours")
        print(f"{'='*60}\n")

    def display_today(self):
        """Display today's stats"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.display_day(today)

    def display_week(self):
        """Display current week's stats"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())

        print(f"\n{'='*60}")
        print(f"Weekly Summary (Week of {week_start.strftime('%Y-%m-%d')})")
        print(f"{'='*60}")

        weekly_totals = defaultdict(lambda: {"total_seconds": 0, "apps": defaultdict(int)})

        for i in range(7):
            day = (week_start + timedelta(days=i)).strftime("%Y-%m-%d")
            if day in self.data:
                for category, data in self.data[day].items():
                    weekly_totals[category]["total_seconds"] += data["total_seconds"]
                    for app, seconds in data["apps"].items():
                        weekly_totals[category]["apps"][app] += seconds

        if not weekly_totals:
            print("\nNo data tracked this week.")
            return

        total_seconds = sum(data["total_seconds"] for data in weekly_totals.values())
        total_hours = total_seconds / 3600

        for category, data in sorted(weekly_totals.items(), key=lambda x: x[1]["total_seconds"], reverse=True):
            hours = data["total_seconds"] / 3600
            percentage = (data["total_seconds"] / total_seconds * 100) if total_seconds > 0 else 0
            print(f"\n{category.upper()}: {hours:.2f}h ({percentage:.1f}%)")

            for app, seconds in sorted(data["apps"].items(), key=lambda x: x[1], reverse=True)[:3]:
                app_hours = seconds / 3600
                print(f"  • {app}: {app_hours:.2f}h")

        print(f"\n{'='*60}")
        print(f"TOTAL TIME TRACKED: {total_hours:.2f} hours")
        print(f"{'='*60}\n")

    def display_insights(self):
        """Display productivity insights"""
        if not self.data:
            print("\nNot enough data for insights.")
            return

        print(f"\n{'='*60}")
        print("Productivity Insights")
        print(f"{'='*60}")

        # Get last 7 days
        dates = sorted(self.data.keys())[-7:]

        # Average daily usage
        productive_categories = ["Coding", "Productivity"]
        unproductive_categories = ["Entertainment"]

        productive_hours = []
        unproductive_hours = []
        daily_totals = []

        for date in dates:
            prod_time = sum(self.data[date].get(cat, {}).get("total_seconds", 0) for cat in productive_categories)
            unprod_time = sum(self.data[date].get(cat, {}).get("total_seconds", 0) for cat in unproductive_categories)
            total_time = sum(data["total_seconds"] for data in self.data[date].values())

            productive_hours.append(prod_time / 3600)
            unproductive_hours.append(unprod_time / 3600)
            daily_totals.append(total_time / 3600)

        if productive_hours:
            print(f"\n📊 Last {len(dates)} days average:")
            print(f"  • Productive time: {sum(productive_hours)/len(productive_hours):.2f}h/day")
            print(f"  • Entertainment: {sum(unproductive_hours)/len(unproductive_hours):.2f}h/day")
            print(f"  • Total tracked: {sum(daily_totals)/len(daily_totals):.2f}h/day")

        # Most productive day
        if daily_totals:
            most_productive_idx = productive_hours.index(max(productive_hours))
            print(f"\n🏆 Most productive day: {dates[most_productive_idx]} ({productive_hours[most_productive_idx]:.2f}h productive)")

        # Top apps overall
        all_apps = defaultdict(int)
        for date_data in self.data.values():
            for cat_data in date_data.values():
                for app, seconds in cat_data["apps"].items():
                    all_apps[app] += seconds

        print(f"\n⭐ Top 5 apps overall:")
        for app, seconds in sorted(all_apps.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {app}: {seconds/3600:.2f}h")

        print(f"\n{'='*60}\n")

    def export_csv(self, filename="time_tracking_export.csv"):
        """Export data to CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Category", "App", "Hours"])

            for date in sorted(self.data.keys()):
                for category, data in self.data[date].items():
                    for app, seconds in data["apps"].items():
                        writer.writerow([date, category, app, seconds / 3600])

        print(f"\n✅ Data exported to {filename}")

    def list_previous_days(self, num_days=10):
        """List previous tracked days"""
        dates = sorted(self.data.keys(), reverse=True)[:num_days]

        if not dates:
            print("\nNo previous days tracked.")
            return

        print(f"\n{'='*60}")
        print(f"Last {len(dates)} Tracked Days")
        print(f"{'='*60}\n")

        for date in dates:
            total_seconds = sum(data["total_seconds"] for data in self.data[date].values())
            total_hours = total_seconds / 3600
            categories = ", ".join(self.data[date].keys())
            print(f"{date}: {total_hours:.2f}h tracked ({categories})")
    
    def run(self, check_interval=5, live_dashboard=False):
        """Main tracking loop with enhanced features"""
        print(f"🕐 Time Tracker Started on {system}")
        print(f"Checking every {check_interval} seconds...")
        print(f"Idle threshold: {self.idle_threshold}s")
        if live_dashboard:
            print("Live dashboard enabled")
        print("Press Ctrl+C to stop and view stats\n")

        # Initialize tray icon
        if HAS_TRAY:
            self.tray_icon = self.create_tray_icon()
            self.start_tray_icon()

        # Update streaks
        self.update_streaks()

        dashboard_update_counter = 0
        notification_check_counter = 0

        try:
            while True:
                # Skip if paused
                if self.is_paused:
                    time.sleep(check_interval)
                    continue

                # Check for idle time
                idle_time = self.get_idle_time()

                if idle_time < self.idle_threshold:
                    app = self.get_active_window()

                    if app and app != "Unknown":
                        # Check if app is blocked in focus mode
                        if self.is_app_blocked(app):
                            self.send_notification(
                                "🚫 Blocked App",
                                f"{app[:30]} is blocked in focus mode"
                            )
                            if system == "Windows":
                                # Minimize window (Windows only)
                                try:
                                    window = win32gui.GetForegroundWindow()
                                    win32gui.ShowWindow(window, 6)  # SW_MINIMIZE
                                except:
                                    pass
                            time.sleep(check_interval)
                            continue

                        if self.current_app == app:
                            # Still on same app, add time
                            elapsed = time.time() - self.start_time
                            if elapsed >= check_interval:
                                self.record_time(app, elapsed, self.current_project)
                                self.start_time = time.time()
                                self.save_data()
                        else:
                            # Switched to new app
                            if self.current_app:
                                elapsed = time.time() - self.start_time
                                self.record_time(self.current_app, elapsed, self.current_project)

                            self.current_app = app
                            self.start_time = time.time()
                            if not live_dashboard:
                                print(f"Tracking: {app[:60]}")
                else:
                    # User is idle
                    if self.current_app:
                        if not live_dashboard:
                            print(f"⏸️  Idle detected, pausing tracking...")
                        self.current_app = None
                        self.start_time = None

                # Check notifications every 30 seconds
                notification_check_counter += 1
                if notification_check_counter >= 6:  # 30 seconds at 5s intervals
                    self.check_goal_notifications()
                    self.check_break_reminder()
                    notification_check_counter = 0

                # Update live dashboard every 10 seconds
                if live_dashboard:
                    dashboard_update_counter += 1
                    if dashboard_update_counter >= 2:  # 10 seconds at 5s intervals
                        self.display_live_dashboard()
                        dashboard_update_counter = 0

                time.sleep(check_interval)

        except KeyboardInterrupt:
            # Record final time
            self.stop_tracking()

            # Show unknown apps
            if self.unknown_apps:
                print(f"\n📝 Unknown apps detected ({len(self.unknown_apps)}):")
                for app in list(self.unknown_apps)[:10]:
                    print(f"  • {app[:60]}")
                if len(self.unknown_apps) > 10:
                    print(f"  ... and {len(self.unknown_apps) - 10} more")

            self.display_today()
            print("\n✅ Tracker stopped. Data saved to", self.data_file)

            if self.tray_icon:
                self.tray_icon.stop()

def print_menu():
    """Display menu options"""
    print("\n" + "="*70)
    print(" "*20 + "TIME TRACKER - MAIN MENU")
    print("="*70)
    print("\n📊 TRACKING")
    print("  1. Start tracking (normal mode)")
    print("  2. Start tracking with live dashboard")
    print("  3. Pause/Resume tracking")

    print("\n📈 VIEW STATS")
    print("  4. View today's stats")
    print("  5. View this week's summary")
    print("  6. View previous days")
    print("  7. View specific date")
    print("  8. View insights & analytics")

    print("\n⚙️  FEATURES")
    print("  9. Set/change project")
    print(" 10. Manual time entry")
    print(" 11. Export data to CSV")
    print(" 12. View unknown apps")

    print("\n🎯 GOALS & SETTINGS")
    print(" 13. Set goals")
    print(" 14. Configure settings")
    print(" 15. Focus mode settings")
    print(" 16. Security settings")

    print("\n 0. Exit")
    print("="*70)

def setup_autostart():
    """Setup auto-start on boot"""
    if system == "Windows":
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_path = os.path.abspath(sys.argv[0])
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "TimeTracker", 0, winreg.REG_SZ, f'python "{app_path}" start')
            winreg.CloseKey(key)
            return True
        except:
            return False
    elif system == "Darwin":
        # macOS LaunchAgent
        plist_path = os.path.expanduser("~/Library/LaunchAgents/com.timetracker.plist")
        app_path = os.path.abspath(sys.argv[0])
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.timetracker</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>{app_path}</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>"""
        try:
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            return True
        except:
            return False
    elif system == "Linux":
        # Linux systemd user service or .desktop file
        autostart_dir = os.path.expanduser("~/.config/autostart")
        os.makedirs(autostart_dir, exist_ok=True)
        desktop_path = os.path.join(autostart_dir, "timetracker.desktop")
        app_path = os.path.abspath(sys.argv[0])
        desktop_content = f"""[Desktop Entry]
Type=Application
Name=Time Tracker
Exec=python3 {app_path} start
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true"""
        try:
            with open(desktop_path, 'w') as f:
                f.write(desktop_content)
            return True
        except:
            return False
    return False

def main():
    """Main application entry point"""
    tracker = TimeTracker()

    # Check password if set
    if tracker.password_hash:
        password = input("🔒 Enter password: ").strip()
        if not tracker.check_password(password):
            print("❌ Incorrect password")
            return

    if len(sys.argv) > 1:
        # Command-line arguments
        command = sys.argv[1]
        if command == "start":
            live = "--live" in sys.argv
            tracker.run(check_interval=5, live_dashboard=live)
        elif command == "today":
            tracker.display_today()
        elif command == "week":
            tracker.display_week()
        elif command == "insights":
            tracker.display_insights()
        elif command == "export":
            filename = sys.argv[2] if len(sys.argv) > 2 else "time_tracking_export.csv"
            tracker.export_csv(filename)
        elif command == "history":
            tracker.list_previous_days()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python tracker.py [start|start --live|today|week|insights|export|history]")
        return

    # Interactive menu
    while True:
        print_menu()
        choice = input("\nEnter your choice (0-16): ").strip()

        if choice == "1":
            tracker.run(check_interval=5, live_dashboard=False)
        elif choice == "2":
            tracker.run(check_interval=5, live_dashboard=True)
        elif choice == "3":
            tracker.is_paused = not tracker.is_paused
            print(f"✅ Tracking {'paused' if tracker.is_paused else 'resumed'}")
        elif choice == "4":
            tracker.display_today()
        elif choice == "5":
            tracker.display_week()
        elif choice == "6":
            tracker.list_previous_days()
            date = input("\nEnter date to view (YYYY-MM-DD) or press Enter to go back: ").strip()
            if date:
                tracker.display_day(date)
        elif choice == "7":
            date = input("Enter date (YYYY-MM-DD): ").strip()
            if date:
                tracker.display_day(date)
        elif choice == "8":
            tracker.display_insights()
        elif choice == "9":
            project = input("Enter project name (or blank to clear): ").strip()
            tracker.current_project = project if project else None
            print(f"✅ Project set to: {tracker.current_project or 'None'}")
        elif choice == "10":
            print("\n--- Manual Time Entry ---")
            app = input("App/Activity name: ").strip()
            category = input("Category: ").strip()
            try:
                minutes = int(input("Duration (minutes): ").strip())
                project = input("Project (optional): ").strip() or None
                date = input("Date (YYYY-MM-DD, or blank for today): ").strip() or None
                tracker.manual_time_entry(app, category, minutes, project, date)
            except ValueError:
                print("❌ Invalid input")
        elif choice == "11":
            filename = input("Enter filename (default: time_tracking_export.csv): ").strip()
            tracker.export_csv(filename if filename else "time_tracking_export.csv")
        elif choice == "12":
            if tracker.unknown_apps:
                print(f"\n📝 Unknown Apps ({len(tracker.unknown_apps)}):")
                for i, app in enumerate(list(tracker.unknown_apps), 1):
                    print(f"{i}. {app}")
                print("\nYou can add these to custom categories in settings.")
            else:
                print("\n✅ No unknown apps detected")
        elif choice == "13":
            print("\n--- Set Daily Goals (hours) ---")
            print("Current goals:", tracker.config.get("goals", {}))
            category = input("Category (Coding/Entertainment/Productivity/etc): ").strip()
            if category:
                try:
                    hours = float(input(f"Goal hours for {category}: ").strip())
                    if "goals" not in tracker.config:
                        tracker.config["goals"] = {}
                    tracker.config["goals"][category] = hours
                    tracker.save_config()
                    print(f"✅ Goal set: {category} = {hours}h/day")
                except ValueError:
                    print("❌ Invalid number")
        elif choice == "14":
            print("\n--- Settings ---")
            print(f"1. Idle threshold: {tracker.config.get('idle_threshold_seconds', 300)}s")
            print(f"2. Break reminder interval: {tracker.config.get('break_reminder_interval', 3600)}s")
            print(f"3. Notifications: {'Enabled' if tracker.config.get('notifications_enabled', True) else 'Disabled'}")
            print("4. Add custom category rule")
            print("5. Exclude app from tracking")
            print(f"6. Auto-start on boot: {'Enabled' if tracker.config.get('auto_start', False) else 'Disabled'}")
            sub = input("Choose setting (1-6) or press Enter to go back: ").strip()
            if sub == "1":
                try:
                    seconds = int(input("Enter idle threshold in seconds: ").strip())
                    tracker.config["idle_threshold_seconds"] = seconds
                    tracker.idle_threshold = seconds
                    tracker.save_config()
                    print(f"✅ Idle threshold set to {seconds}s")
                except ValueError:
                    print("❌ Invalid number")
            elif sub == "2":
                try:
                    seconds = int(input("Enter break reminder interval in seconds (0 to disable): ").strip())
                    tracker.config["break_reminder_interval"] = seconds
                    tracker.save_config()
                    print(f"✅ Break reminder set to {seconds}s")
                except ValueError:
                    print("❌ Invalid number")
            elif sub == "3":
                tracker.config["notifications_enabled"] = not tracker.config.get("notifications_enabled", True)
                tracker.save_config()
                print(f"✅ Notifications {'enabled' if tracker.config['notifications_enabled'] else 'disabled'}")
            elif sub == "4":
                pattern = input("Enter app name pattern (e.g., 'notepad'): ").strip()
                category = input("Enter category: ").strip()
                if pattern and category:
                    if "custom_categories" not in tracker.config:
                        tracker.config["custom_categories"] = {}
                    tracker.config["custom_categories"][pattern] = category
                    tracker.save_config()
                    print(f"✅ Added rule: '{pattern}' -> {category}")
            elif sub == "5":
                app = input("Enter app name pattern to exclude: ").strip()
                if app:
                    if "excluded_apps" not in tracker.config:
                        tracker.config["excluded_apps"] = []
                    tracker.config["excluded_apps"].append(app)
                    tracker.save_config()
                    print(f"✅ Added '{app}' to exclusion list")
            elif sub == "6":
                if setup_autostart():
                    tracker.config["auto_start"] = True
                    tracker.save_config()
                    print("✅ Auto-start enabled")
                else:
                    print("❌ Failed to enable auto-start")
        elif choice == "15":
            print("\n--- Focus Mode Settings ---")
            print(f"Focus mode: {'Active' if tracker.focus_mode else 'Inactive'}")
            print("Blocked apps:", tracker.config.get("focus_mode_blocked", []))
            print("\n1. Toggle focus mode")
            print("2. Add blocked app")
            print("3. Remove blocked app")
            sub = input("Choose option (1-3): ").strip()
            if sub == "1":
                tracker.focus_mode = not tracker.focus_mode
                print(f"✅ Focus mode {'activated' if tracker.focus_mode else 'deactivated'}")
            elif sub == "2":
                app = input("Enter app pattern to block: ").strip()
                if app:
                    if "focus_mode_blocked" not in tracker.config:
                        tracker.config["focus_mode_blocked"] = []
                    tracker.config["focus_mode_blocked"].append(app)
                    tracker.save_config()
                    print(f"✅ Added '{app}' to block list")
            elif sub == "3":
                blocked = tracker.config.get("focus_mode_blocked", [])
                if blocked:
                    for i, app in enumerate(blocked, 1):
                        print(f"{i}. {app}")
                    try:
                        idx = int(input("Enter number to remove: ").strip()) - 1
                        removed = blocked.pop(idx)
                        tracker.save_config()
                        print(f"✅ Removed '{removed}'")
                    except:
                        print("❌ Invalid selection")
        elif choice == "16":
            print("\n--- Security Settings ---")
            print(f"Password protection: {'Enabled' if tracker.password_hash else 'Disabled'}")
            print("\n1. Set/change password")
            print("2. Remove password")
            sub = input("Choose option (1-2): ").strip()
            if sub == "1":
                password = input("Enter new password: ").strip()
                confirm = input("Confirm password: ").strip()
                if password == confirm:
                    tracker.set_password(password)
                    print("✅ Password set")
                else:
                    print("❌ Passwords don't match")
            elif sub == "2":
                tracker.config["password_hash"] = None
                tracker.password_hash = None
                tracker.save_config()
                print("✅ Password removed")
        elif choice == "0":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()