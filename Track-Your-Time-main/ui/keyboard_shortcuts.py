"""
Configurable Keyboard Shortcuts for Time Tracker
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os

class KeyboardShortcuts:
    """Manage keyboard shortcuts for the app"""

    def __init__(self, parent, app_instance):
        self.parent = parent
        self.app = app_instance
        self.shortcuts_file = "shortcuts.json"
        self.shortcuts = self.load_shortcuts()
        self.recording_key = None

        # Default shortcuts
        self.default_shortcuts = {
            "start_tracking": "Ctrl+Shift+S",
            "pause_tracking": "Ctrl+Shift+P",
            "focus_mode": "Ctrl+Shift+F",
            "view_stats": "Ctrl+Shift+D",
            "new_project": "Ctrl+Shift+N",
            "export_data": "Ctrl+Shift+E",
            "settings": "Ctrl+,",
            "quit": "Ctrl+Q"
        }

    def load_shortcuts(self):
        """Load shortcuts from file"""
        if os.path.exists(self.shortcuts_file):
            try:
                with open(self.shortcuts_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_shortcuts()
        return self.get_default_shortcuts()

    def get_default_shortcuts(self):
        """Get default shortcuts"""
        return self.default_shortcuts.copy()

    def save_shortcuts(self):
        """Save shortcuts to file"""
        with open(self.shortcuts_file, 'w') as f:
            json.dump(self.shortcuts, f, indent=2)

    def create_shortcuts_editor(self, frame):
        """Create shortcuts editor UI"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkLabel(
            frame,
            text="⌨️ Keyboard Shortcuts",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=20)

        # Info
        info = ctk.CTkLabel(
            frame,
            text="Click 'Record' and press your desired key combination",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        info.pack(pady=(0, 20))

        # Scrollable frame for shortcuts
        scroll_frame = ctk.CTkScrollableFrame(frame)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Shortcut actions with descriptions
        actions = [
            ("start_tracking", "Start Tracking", "Begin tracking your time"),
            ("pause_tracking", "Pause Tracking", "Pause/resume tracking"),
            ("focus_mode", "Toggle Focus Mode", "Enable/disable focus mode"),
            ("view_stats", "View Dashboard", "Open dashboard view"),
            ("new_project", "New Project", "Create a new project"),
            ("export_data", "Export Data", "Export tracking data"),
            ("settings", "Open Settings", "Open settings panel"),
            ("quit", "Quit Application", "Close the application")
        ]

        self.shortcut_labels = {}

        for action_key, action_name, description in actions:
            # Action frame
            action_frame = ctk.CTkFrame(scroll_frame)
            action_frame.pack(fill="x", pady=8, padx=10)

            # Left side - action info
            info_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

            ctk.CTkLabel(
                info_frame,
                text=action_name,
                font=ctk.CTkFont(size=15, weight="bold"),
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info_frame,
                text=description,
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            ).pack(anchor="w")

            # Right side - shortcut and buttons
            control_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
            control_frame.pack(side="right", padx=10)

            # Shortcut display
            shortcut_label = ctk.CTkLabel(
                control_frame,
                text=self.shortcuts.get(action_key, "Not set"),
                font=ctk.CTkFont(size=13, weight="bold"),
                fg_color="#2b2b2b",
                corner_radius=6,
                width=150,
                height=35
            )
            shortcut_label.pack(side="left", padx=5)
            self.shortcut_labels[action_key] = shortcut_label

            # Record button
            record_btn = ctk.CTkButton(
                control_frame,
                text="⏺ Record",
                command=lambda k=action_key: self.start_recording(k),
                width=90,
                height=35,
                fg_color="#FF5722",
                hover_color="#E64A19"
            )
            record_btn.pack(side="left", padx=5)

            # Clear button
            clear_btn = ctk.CTkButton(
                control_frame,
                text="✖",
                command=lambda k=action_key: self.clear_shortcut(k),
                width=35,
                height=35,
                fg_color="#757575",
                hover_color="#616161"
            )
            clear_btn.pack(side="left", padx=5)

        # Bottom buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20, padx=20)

        ctk.CTkButton(
            button_frame,
            text="💾 Save Shortcuts",
            command=self.save_current_shortcuts,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Defaults",
            command=self.reset_shortcuts,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="✓ Apply Shortcuts",
            command=self.apply_shortcuts,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=5)

    def start_recording(self, action_key):
        """Start recording a keyboard shortcut"""
        self.recording_key = action_key
        self.shortcut_labels[action_key].configure(text="Press keys...")

        # Bind key press
        self.parent.bind("<Key>", self.on_key_press)

    def on_key_press(self, event):
        """Handle key press during recording"""
        if self.recording_key is None:
            return

        # Build shortcut string
        modifiers = []
        if event.state & 0x0004:  # Control
            modifiers.append("Ctrl")
        if event.state & 0x0001:  # Shift
            modifiers.append("Shift")
        if event.state & 0x0008 or event.state & 0x0080:  # Alt
            modifiers.append("Alt")

        # Get key
        key = event.keysym
        if key in ['Control_L', 'Control_R', 'Shift_L', 'Shift_R', 'Alt_L', 'Alt_R']:
            return  # Don't record modifier-only

        # Build shortcut
        if modifiers:
            shortcut = "+".join(modifiers) + "+" + key
        else:
            shortcut = key

        # Update
        self.shortcuts[self.recording_key] = shortcut
        self.shortcut_labels[self.recording_key].configure(text=shortcut)

        # Unbind
        self.parent.unbind("<Key>")
        self.recording_key = None

    def clear_shortcut(self, action_key):
        """Clear a shortcut"""
        self.shortcuts[action_key] = "Not set"
        self.shortcut_labels[action_key].configure(text="Not set")

    def save_current_shortcuts(self):
        """Save current shortcuts"""
        self.save_shortcuts()
        messagebox.showinfo("Success", "Shortcuts saved successfully!")

    def reset_shortcuts(self):
        """Reset to default shortcuts"""
        self.shortcuts = self.get_default_shortcuts()
        for action_key, shortcut in self.shortcuts.items():
            if action_key in self.shortcut_labels:
                self.shortcut_labels[action_key].configure(text=shortcut)
        messagebox.showinfo("Success", "Shortcuts reset to defaults!")

    def apply_shortcuts(self):
        """Apply shortcuts to the app"""
        # Bind shortcuts
        try:
            for action, shortcut in self.shortcuts.items():
                if shortcut != "Not set":
                    self.bind_shortcut(action, shortcut)
            messagebox.showinfo("Success", "Shortcuts applied successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply shortcuts: {str(e)}")

    def bind_shortcut(self, action, shortcut):
        """Bind a specific shortcut"""
        # Convert shortcut to tkinter format
        tk_shortcut = shortcut.replace("Ctrl", "Control").replace("+", "-")

        # Map actions to functions
        action_map = {
            "start_tracking": lambda e: self.app.start_tracking() if hasattr(self.app, 'start_tracking') else None,
            "pause_tracking": lambda e: self.app.stop_tracking() if hasattr(self.app, 'stop_tracking') else None,
            "focus_mode": lambda e: self.app.toggle_focus_mode() if hasattr(self.app, 'toggle_focus_mode') else None,
            "view_stats": lambda e: self.app.tabview.set("Dashboard") if hasattr(self.app, 'tabview') else None,
            "settings": lambda e: self.app.tabview.set("Settings") if hasattr(self.app, 'tabview') else None,
            "quit": lambda e: self.app.quit()
        }

        if action in action_map:
            try:
                self.app.bind(f"<{tk_shortcut}>", action_map[action])
            except:
                pass  # Skip if binding fails
