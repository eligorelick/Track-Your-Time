# ⏱️ Time Tracker Pro

A comprehensive, modern time tracking application that automatically monitors your computer usage and provides detailed analytics about how you spend your time.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE.txt)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

---

## 🚀 Quick Start

### Option 1: Use the Executable (Recommended for Users)

**No Python installation required!**

1. Download `TimeTrackerProSetup.exe` from releases
2. Run the installer
3. Follow the setup wizard
4. Start tracking your time!

The installer will:
- ✅ Install the application
- ✅ Create desktop shortcut
- ✅ Set up auto-start (optional)
- ✅ Configure initial settings

### Option 2: Run from Source (For Developers)

**Requires Python 3.7+**

```bash
# 1. Clone or download this repository
git clone <repository-url>
cd Track-Your-Time-main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the GUI version
python gui_tracker.py

# OR run the CLI version
python tracker.py
```

---

## ✨ Features Overview

### 🎯 Core Tracking Features
- ✅ **Automatic Time Tracking** - Tracks active applications and windows automatically
- ✅ **300+ App Recognition** - Smart categorization across 12 categories
- ✅ **Smart Idle Detection** - Pauses when you're away from your computer
- ✅ **Browser URL Tracking** - Categorizes websites (GitHub → Coding, YouTube → Entertainment)
- ✅ **Cross-Platform** - Works on Windows, macOS, and Linux

### 📊 New Advanced Features (v2.0)

#### 📈 Interactive Analytics
- **Charts & Graphs** - Beautiful visualizations of your time data
  - Weekly time distribution (stacked bar chart)
  - Category breakdown (pie chart)
  - 30-day productivity trend (line chart)
- **Calendar View** - Interactive monthly calendar with heat map
  - Click any day to see detailed breakdown
  - Color-coded by productivity level
  - Navigate months easily

#### 🎨 Customization
- **Theme Creator** - Design your own color schemes
  - Visual color picker
  - Live preview
  - Save/load unlimited themes
- **Keyboard Shortcuts** - Customize all hotkeys
  - Record custom key combinations
  - 8 configurable actions
  - Quick access to all features

#### 🍅 Productivity Tools
- **Pomodoro Timer** - Built-in Pomodoro technique support
  - Customizable work/break durations
  - Session tracking
  - Daily goal monitoring
  - Auto-start options
- **Focus Mode** - Block distracting apps/websites
  - One-click activation
  - Customizable block list
  - Automatic app minimization (Windows)

#### 🏷️ Organization
- **Activity Tags** - Tag activities with custom labels
  - Color-coded tags
  - Tag analytics
  - Quick tagging interface
  - Filter by tags
- **Project Tracking** - Track time by project
  - Switch projects instantly
  - View time per project
  - Historical project data

#### 📤 Export & Reporting
- **Multi-Format Export**:
  - 📄 **CSV** - Excel/Google Sheets compatible
  - 📋 **JSON** - Raw data for programming
  - 📊 **Excel** - Formatted spreadsheet with charts
  - 📑 **PDF** - Professional report format
- **Email Reports** - Automated scheduled reports
  - Daily/weekly/monthly schedules
  - HTML email templates
  - CSV attachments
  - SMTP configuration

### 🎯 Existing Features
- **Live Dashboard** - Real-time stats and progress
- **Goal Setting** - Set and track daily goals per category
- **Streak Tracking** - Gamification to maintain productivity
- **Smart Notifications** - Goal achievements, break reminders, warnings
- **Manual Time Entry** - Add offline work sessions
- **Privacy Features** - Password protection, app exclusions
- **System Tray Integration** - Quick access and background operation
- **Auto-Start** - Run automatically on boot

---

## 📋 System Requirements

### For Executable Version (No Installation Needed)
- **OS:** Windows 10/11 (64-bit)
- **RAM:** 200 MB minimum
- **Disk:** 100 MB free space
- **No Python required!**

### For Source Version
- **Python:** 3.7 or higher
- **OS:** Windows, macOS, or Linux
- **Dependencies:** See [requirements.txt](requirements.txt)

---

## 📖 Installation Guide

### Method 1: Windows Installer (Easiest)

1. **Download** the installer: `TimeTrackerProSetup.exe`

2. **Run the installer**
   - Double-click the downloaded file
   - Follow the installation wizard
   - Choose installation location
   - Select optional features:
     - Create desktop shortcut
     - Auto-start with Windows
     - Add to Start Menu

3. **Complete first-run setup**
   - Set your daily goals (optional)
   - Configure preferences (optional)
   - Choose auto-start option
   - Click "Finish"

4. **Start using!**
   - Application launches automatically
   - Icon appears in system tray
   - Click "Start Tracking" to begin

### Method 2: Portable Executable

1. **Download** `TimeTrackerPro.exe`
2. **Place** in any folder
3. **Run** the executable
4. **Complete** first-run wizard
5. **Start tracking!**

No installation, no admin rights needed. Perfect for USB drives or temporary use.

### Method 3: From Source (Developers)

#### Windows

```bash
# 1. Install Python 3.7+ from python.org

# 2. Clone repository
git clone <repository-url>
cd Track-Your-Time-main

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python gui_tracker.py
```

#### macOS

```bash
# 1. Install Python 3.7+ (if not already installed)
brew install python

# 2. Clone repository
git clone <repository-url>
cd Track-Your-Time-main

# 3. Install dependencies
pip3 install -r requirements.txt

# 4. Run application
python3 gui_tracker.py
```

#### Linux

```bash
# 1. Install Python 3.7+ (usually pre-installed)
sudo apt-get install python3 python3-pip

# 2. Install system dependencies
sudo apt-get install xdotool xprintidle

# 3. Clone repository
git clone <repository-url>
cd Track-Your-Time-main

# 4. Install Python dependencies
pip3 install -r requirements.txt

# 5. Run application
python3 gui_tracker.py
```

---

## 🎯 How to Use

### First Launch

When you first run Time Tracker Pro, you'll see a **welcome wizard**:

1. **Welcome Screen** - Introduction to features
2. **Goal Setup** - Set your daily time goals (optional)
   - Example: 4 hours of Coding, 2 hours max Entertainment
3. **Settings** - Configure idle timeout and break reminders
4. **Auto-Start** - Choose if app should run on startup
5. **Summary** - Review and finish setup

**You can skip any step and configure later in Settings!**

### Main Interface

The application has **7 main tabs**:

#### 1. 📊 Dashboard
Your command center for real-time tracking.

**What you see:**
- Current active application and duration
- Today's total time tracked
- Current productivity streak
- Category breakdown with progress bars
- Goal progress indicators

**What you can do:**
- Start/pause tracking (big button at top)
- Monitor real-time activity
- See goal progress
- Check your streak

#### 2. 📈 Analytics
Visual analytics and charts.

**Features:**
- **Weekly Chart** - 7-day time distribution by category
- **Pie Chart** - Today's category breakdown
- **Trend Line** - 30-day productivity trends
- **Interactive** - Click and explore your data

**Use for:**
- Spotting productivity patterns
- Finding time wasters
- Tracking improvements
- Sharing reports

#### 3. 📅 Calendar
Interactive monthly calendar view.

**Features:**
- Heat map showing productivity by day
- Color intensity = hours tracked
- Click any day for detailed breakdown
- Navigate months (Previous/Next/Today buttons)

**Color coding:**
- Dark gray: No activity
- Light blue: 2-4 hours
- Medium blue: 4-6 hours
- Bright blue: 8+ hours

#### 4. 🎯 Goals
Set and track your daily goals.

**How to use:**
1. Click "Add New Goal"
2. Select category (Coding, Productivity, etc.)
3. Set target hours per day
4. Optional: Set maximum limit (for Entertainment)
5. Track progress with visual bars

**Notifications:**
- ✅ Goal achieved
- ⚠️ Limit exceeded
- 🔥 Streak milestones

#### 5. 🍅 Pomodoro
Built-in Pomodoro timer for focused work.

**Default settings:**
- Work: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes
- Long break after: 4 sessions

**How to use:**
1. Click "Start" to begin work session
2. Timer counts down
3. Get notification when session ends
4. Take break (auto-starts or manual)
5. Track daily sessions toward goal

**Settings:**
- Customize all durations
- Set daily session goal
- Enable auto-start for breaks/work
- View session history

#### 6. 🎨 Focus Mode
Block distracting apps and websites.

**How to use:**
1. Go to Focus Mode tab
2. Click "Activate Focus Mode"
3. Distracting apps will be blocked
4. Get notifications if you try to open them
5. Click "Deactivate" when done

**Configure blocked apps:**
- Settings → Focus Mode Settings
- Add app names or websites
- Supports partial matching (e.g., "youtube")

#### 7. 📁 Projects
Track time by project.

**How to use:**
1. Click "New Project"
2. Enter project name
3. Select project from dropdown
4. All tracked time is tagged to that project
5. Switch projects anytime

**View project stats:**
- Total time per project
- Activity breakdown by project
- Historical project data

#### 8. ⚙️ Settings
Configure all application settings.

**Available settings:**
- **Idle Threshold** - Time before pausing (default: 5 minutes)
- **Break Reminders** - Interval for break notifications
- **Notifications** - Enable/disable all notifications
- **Theme** - Dark/Light mode toggle
- **Keyboard Shortcuts** - Customize hotkeys
- **Auto-Start** - Run on system startup
- **Email Reports** - Configure automated reports
- **Custom Categories** - Add custom app categorization
- **Excluded Apps** - Apps to ignore completely

---

## 🔑 Keyboard Shortcuts

### Default Shortcuts
- `Ctrl+Shift+S` - Start tracking
- `Ctrl+Shift+P` - Pause tracking
- `Ctrl+Shift+F` - Toggle focus mode
- `Ctrl+Shift+D` - View dashboard
- `Ctrl+Shift+N` - New project
- `Ctrl+Shift+E` - Export data
- `Ctrl+,` - Open settings
- `Ctrl+Q` - Quit application

**All shortcuts are customizable!** Go to Settings → Keyboard Shortcuts

---

## 🏷️ Using Tags

Tags help organize your activities beyond categories.

### Creating Tags
1. Go to **Tags** tab
2. Enter tag name
3. Click color button to choose color
4. Click "Add Tag"

### Tagging Activities
**Quick tag (current activity):**
- Click tag button at bottom of Tags screen

**Tag manually:**
- Select activity
- Click tag
- Activity is now tagged

### Tag Analytics
- View usage statistics
- See activities per tag
- Filter activities by tag
- Track tag trends

### Example Tags
- 🔴 **Urgent** - High priority tasks
- 💼 **Client-A** - Client-specific work
- 📚 **Learning** - Educational activities
- 🐛 **Bug Fix** - Development debugging
- ✨ **Feature** - New feature development

---

## 📤 Exporting Data

### Quick Export (CSV)
```bash
# CLI version
python tracker.py export my_data.csv

# GUI version
Features → Export → CSV
```

### Advanced Export (GUI)

1. Go to **Export** tab
2. Select **date range**:
   - Last 7 days
   - Last 30 days
   - This month
   - Last month
   - All time
3. Choose **format**:

   **📄 CSV** - Simple, universal format
   - Opens in Excel, Google Sheets
   - Columns: Date, Category, Hours, Project
   - Best for: Spreadsheet analysis

   **📋 JSON** - Raw data format
   - Complete data export
   - Programming-friendly
   - Best for: Automation, backups

   **📊 Excel** - Formatted spreadsheet
   - Multiple sheets (Data + Summary)
   - Styled headers and colors
   - Auto-sized columns
   - Best for: Reports, presentations

   **📑 PDF** - Professional report
   - Category summary table
   - Daily breakdown
   - Print-ready format
   - Best for: Archival, sharing

4. Click format button
5. Choose save location
6. Done!

### Email Reports

Set up automated reports delivered to your inbox.

**Setup:**
1. Settings → Email Reports
2. Configure SMTP:
   - Server: smtp.gmail.com (for Gmail)
   - Port: 587
   - Your email
   - App password (not regular password!)
3. Set recipient email
4. Choose frequency (daily/weekly/monthly)
5. Enable auto-send (optional)

**For Gmail:**
1. Go to myaccount.google.com/apppasswords
2. Generate app password
3. Use that password in Time Tracker

**Manual send:**
- Click "Send Report Now" anytime
- Includes HTML summary + CSV attachment

---

## 🎨 Customization

### Custom Themes

Create your own color schemes!

1. Go to **Settings → Themes**
2. Click "Theme Creator"
3. Click color buttons to pick colors:
   - Primary background
   - Secondary background
   - Primary text
   - Secondary text
   - Accent color
   - Success, Warning, Error colors
4. See live preview
5. Click "Save Theme"
6. Name your theme
7. Load saved themes anytime

### Custom Categories

Add custom rules for app categorization:

1. Settings → Custom Categories
2. Enter app pattern (e.g., "slack")
3. Choose category (e.g., "Work Communication")
4. Click Add
5. App will now be categorized correctly

**Examples:**
- Pattern: `figma` → Category: Design
- Pattern: `notion` → Category: Productivity
- Pattern: `discord` → Category: Communication

### Exclude Apps

Prevent specific apps from being tracked:

1. Settings → Excluded Apps
2. Enter app name pattern
3. Click Add
4. App will no longer be tracked

**Common exclusions:**
- Password managers (KeePass, 1Password)
- Private browsing
- Sensitive applications

---

## 📊 Understanding Categories

Time Tracker Pro automatically categorizes apps into 12 categories:

| Category | Examples | Purpose |
|----------|----------|---------|
| 💻 **Coding** | VS Code, PyCharm, Git, Terminal | Development work |
| 📝 **Productivity** | Word, Excel, Notion, Trello | Office work, planning |
| 💬 **Communication** | Outlook, Slack, Teams, Zoom | Email, messaging, meetings |
| 🎨 **Design** | Photoshop, Figma, Blender | Creative work |
| 🎮 **Entertainment** | Games, Netflix, Spotify | Leisure time |
| 📱 **Social Media** | Facebook, Twitter, Instagram | Social networking |
| 📚 **Education** | Coursera, Khan Academy, Udemy | Learning |
| 🌐 **Browsing** | Chrome, Firefox (general use) | Web browsing |
| 📖 **Reading** | Kindle, Medium, News sites | Reading |
| 💰 **Finance** | Banking apps, PayPal | Financial management |
| 🔧 **Utilities** | File explorers, system tools | System maintenance |
| 🛒 **Shopping** | Amazon, eBay | Online shopping |

**Smart browser detection:**
- github.com → Coding
- youtube.com → Entertainment
- stackoverflow.com → Coding
- facebook.com → Social Media

---

## 🔒 Privacy & Security

### Your Data is Private
- ✅ All data stored **locally** on your computer
- ✅ **No cloud sync** (unless you enable email reports)
- ✅ **No telemetry** or analytics sent to anyone
- ✅ **Open source** - audit the code yourself
- ✅ **Full control** - you own your data

### Password Protection
Enable password protection:
1. Settings → Security
2. Click "Set Password"
3. Enter password
4. Confirm password
5. Stats now require password to view

### Data Locations
Your data is stored here:
- **Windows:** `%USERPROFILE%` (usually `C:\Users\YourName\`)
- **macOS:** `~/` (home directory)
- **Linux:** `~/` (home directory)

**Files:**
- `time_tracking.json` - Your time data
- `tracker_config.json` - Your settings
- Plus feature-specific configs (themes, tags, etc.)

### Backup Your Data
Simply copy these JSON files to backup:
```bash
# Windows
copy %USERPROFILE%\time_tracking.json backup\
copy %USERPROFILE%\tracker_config.json backup\

# macOS/Linux
cp ~/time_tracking.json ~/backup/
cp ~/tracker_config.json ~/backup/
```

---

## 🐛 Troubleshooting

### App Won't Start

**Problem:** Application doesn't launch

**Solutions:**
1. Check if dependencies are installed:
   ```bash
   python test_imports.py
   ```
2. Install missing dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
3. Run from command line to see errors:
   ```bash
   python gui_tracker.py
   ```

### Tracking Not Working

**Problem:** Time not being recorded

**Solutions:**
1. Check if tracking is active (button should show "Pause")
2. Verify idle threshold isn't too low (Settings → Idle Threshold)
3. Check excluded apps list (Settings → Excluded Apps)
4. Make sure app has necessary permissions (Windows may ask)

### System Tray Icon Missing

**Problem:** No icon in system tray

**Solutions:**
```bash
pip install pystray pillow
```

If still not working, restart the application.

### Notifications Not Working

**Problem:** No notification popups

**Solutions:**
1. Install notification library:
   ```bash
   pip install plyer
   ```
2. Enable notifications: Settings → Notifications
3. Check Windows notification settings (system level)

### Charts Not Showing

**Problem:** Analytics tab shows errors

**Solutions:**
1. Install matplotlib:
   ```bash
   pip install matplotlib
   ```
2. Restart application

### Excel Export Fails

**Problem:** Can't export to Excel format

**Solutions:**
1. Install openpyxl:
   ```bash
   pip install openpyxl
   ```
2. Use CSV export as alternative

### PDF Export Fails

**Problem:** Can't export to PDF format

**Solutions:**
1. Install reportlab:
   ```bash
   pip install reportlab
   ```
2. Use CSV or Excel export as alternative

### Email Reports Not Sending

**Problem:** Email reports fail to send

**Solutions:**
1. For Gmail, use **App Password** (not regular password)
   - Go to: myaccount.google.com/apppasswords
   - Generate new app password
   - Use that in Time Tracker
2. Check SMTP settings are correct
3. Test email with "Send Test Email" button
4. Check firewall isn't blocking SMTP (port 587)

### High CPU Usage

**Problem:** Application using too much CPU

**Solutions:**
1. Increase update interval (reduces checks)
2. Disable live dashboard when not needed
3. Close analytics charts when not viewing

### Data Not Saving

**Problem:** Data disappears after restart

**Solutions:**
1. Check write permissions in user directory
2. Look for `time_tracking.json` in `%USERPROFILE%`
3. Check disk space
4. Run application as administrator (Windows)

---

## 💡 Tips & Best Practices

### Getting Started
1. ✅ **Start simple** - Don't configure everything at once
2. ✅ **Set realistic goals** - Start with 2-3 hours, increase gradually
3. ✅ **Enable auto-start** - Let it run in background
4. ✅ **Review daily** - Check dashboard at end of day

### For Maximum Accuracy
1. 🎯 **Keep app running** - Minimize to system tray
2. 🎯 **Use projects** - Tag time for better attribution
3. 🎯 **Add custom rules** - Categorize your specific apps
4. 🎯 **Use manual entry** - Add offline work sessions

### For Productivity
1. 🚀 **Use Pomodoro timer** - Stay focused with timed sessions
2. 🚀 **Enable focus mode** - Block distractions during work
3. 🚀 **Set daily goals** - Stay motivated with targets
4. 🚀 **Track streaks** - Build consistency
5. 🚀 **Review weekly** - Analyze patterns and improve

### For Privacy
1. 🔒 **Exclude sensitive apps** - Password managers, banking
2. 🔒 **Enable password protection** - Protect your stats
3. 🔒 **Backup regularly** - Copy JSON files
4. 🔒 **Review unknown apps** - Add to custom categories

### For Teams
1. 👥 **Export reports** - Share PDF reports with team
2. 👥 **Use projects** - Track client/project time
3. 👥 **Tag activities** - Organize work by type
4. 👥 **Share themes** - Export/import theme JSON

---

## 🔨 Building from Source

Want to create your own executable?

### Quick Build (Windows)

```bash
# Run the automated build script
build_all.bat
```

This will:
1. Install dependencies
2. Build executable
3. Create installer (if Inno Setup installed)
4. Output to `dist/` folder

### Manual Build

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Build executable
python installer/build_exe.py

# 3. Find executable at:
# dist/TimeTrackerPro.exe
```

### Create Installer

Requires [Inno Setup 6](https://jrsoftware.org/isdl.php)

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

Output: `dist/installer/TimeTrackerProSetup.exe`

**See [BUILD.md](BUILD.md) for detailed instructions.**

---

## 📚 Additional Resources

- **[QUICKSTART.md](QUICKSTART.md)** - Fast-track guide to get started
- **[BUILD.md](BUILD.md)** - Detailed build instructions
- **[FEATURES_ADDED.md](FEATURES_ADDED.md)** - Complete feature documentation
- **[GUI_FEATURES.md](GUI_FEATURES.md)** - GUI design details
- **[LICENSE.txt](LICENSE.txt)** - MIT License

---

## 🤝 Support & Contributing

### Get Help
- Check this README first
- Run `python test_imports.py` to diagnose issues
- Check the [Troubleshooting](#-troubleshooting) section

### Report Bugs
Please include:
- Your OS and version
- Python version (if running from source)
- Error message or description
- Steps to reproduce

### Contribute
We welcome contributions!
- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🌐 Translations
- 🎨 UI/UX enhancements

---

## 📄 License

**MIT License** - Free to use, modify, and distribute.

See [LICENSE.txt](LICENSE.txt) for full details.

---

## 🌟 Acknowledgments

Built with:
- **Python** - Core language
- **CustomTkinter** - Modern GUI framework
- **Matplotlib** - Data visualization
- **PyInstaller** - Executable creation
- **Inno Setup** - Windows installer

Special thanks to all contributors and users!

---

## 📞 Quick Reference Card

```
┌─────────────────────────────────────────┐
│        TIME TRACKER PRO v2.0            │
├─────────────────────────────────────────┤
│                                         │
│  QUICK START:                           │
│  1. Run TimeTrackerProSetup.exe        │
│  2. Complete setup wizard               │
│  3. Click "Start Tracking"             │
│  4. Minimize to tray                    │
│                                         │
│  TABS:                                  │
│  📊 Dashboard  - Real-time tracking    │
│  📈 Analytics  - Charts & graphs       │
│  📅 Calendar   - Monthly view          │
│  🎯 Goals      - Set daily targets     │
│  🍅 Pomodoro   - Focus timer           │
│  📁 Projects   - Project tracking      │
│  🏷️ Tags       - Organize activities   │
│  ⚙️ Settings   - Configure app         │
│                                         │
│  SHORTCUTS:                             │
│  Ctrl+Shift+S  - Start tracking        │
│  Ctrl+Shift+P  - Pause                 │
│  Ctrl+Shift+F  - Focus mode            │
│  Ctrl+Q        - Quit                  │
│                                         │
│  DATA LOCATION:                         │
│  %USERPROFILE%\time_tracking.json      │
│                                         │
│  EXPORT FORMATS:                        │
│  CSV, JSON, Excel, PDF                 │
│                                         │
└─────────────────────────────────────────┘
```

---

**Ready to track your time like a pro? Download and start today! ⏱️✨**
