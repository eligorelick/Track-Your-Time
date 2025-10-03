"""
Custom Theme Creator for Time Tracker
"""

import customtkinter as ctk
from tkinter import colorchooser, messagebox
import json
import os

class ThemeCreator:
    """Custom theme creation and management"""

    def __init__(self, parent, app_instance):
        self.parent = parent
        self.app = app_instance
        self.theme_file = "custom_themes.json"
        self.themes = self.load_themes()
        self.current_theme = {
            "name": "Custom Theme",
            "bg_primary": "#1e1e1e",
            "bg_secondary": "#2b2b2b",
            "fg_primary": "#ffffff",
            "fg_secondary": "#b0b0b0",
            "accent_color": "#2196F3",
            "success_color": "#4CAF50",
            "warning_color": "#FF9800",
            "error_color": "#F44336"
        }

    def load_themes(self):
        """Load saved custom themes"""
        if os.path.exists(self.theme_file):
            try:
                with open(self.theme_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_themes(self):
        """Save themes to file"""
        with open(self.theme_file, 'w') as f:
            json.dump(self.themes, f, indent=2)

    def create_theme_editor(self, frame):
        """Create the theme editor UI"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkLabel(
            frame,
            text="🎨 Theme Creator",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=20)

        # Main content
        content_frame = ctk.CTkFrame(frame)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left side - Color pickers
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Theme name
        name_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        name_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(
            name_frame,
            text="Theme Name:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=5)

        self.theme_name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="My Custom Theme",
            width=200
        )
        self.theme_name_entry.pack(side="left", padx=5)
        self.theme_name_entry.insert(0, self.current_theme["name"])

        # Color pickers
        color_settings = [
            ("Primary Background", "bg_primary"),
            ("Secondary Background", "bg_secondary"),
            ("Primary Text", "fg_primary"),
            ("Secondary Text", "fg_secondary"),
            ("Accent Color", "accent_color"),
            ("Success Color", "success_color"),
            ("Warning Color", "warning_color"),
            ("Error Color", "error_color")
        ]

        self.color_buttons = {}

        for label, key in color_settings:
            color_frame = ctk.CTkFrame(left_frame)
            color_frame.pack(fill="x", pady=8, padx=10)

            ctk.CTkLabel(
                color_frame,
                text=label,
                font=ctk.CTkFont(size=13),
                width=180,
                anchor="w"
            ).pack(side="left", padx=5)

            color_btn = ctk.CTkButton(
                color_frame,
                text=self.current_theme[key],
                command=lambda k=key: self.pick_color(k),
                fg_color=self.current_theme[key],
                width=120,
                height=35
            )
            color_btn.pack(side="left", padx=5)
            self.color_buttons[key] = color_btn

        # Right side - Preview
        right_frame = ctk.CTkFrame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        preview_label = ctk.CTkLabel(
            right_frame,
            text="Preview",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        preview_label.pack(pady=10)

        self.preview_frame = ctk.CTkFrame(
            right_frame,
            fg_color=self.current_theme["bg_primary"]
        )
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.update_preview()

        # Bottom buttons
        button_frame = ctk.CTkFrame(frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20, padx=20)

        ctk.CTkButton(
            button_frame,
            text="💾 Save Theme",
            command=self.save_current_theme,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="✓ Apply Theme",
            command=self.apply_theme,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="📋 Load Theme",
            command=self.load_theme_dialog,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Default",
            command=self.reset_theme,
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00"
        ).pack(side="left", padx=5)

    def pick_color(self, key):
        """Open color picker"""
        color = colorchooser.askcolor(
            initialcolor=self.current_theme[key],
            title=f"Choose {key.replace('_', ' ').title()}"
        )

        if color[1]:  # color[1] is hex value
            self.current_theme[key] = color[1]
            self.color_buttons[key].configure(
                text=color[1],
                fg_color=color[1]
            )
            self.update_preview()

    def update_preview(self):
        """Update the preview panel"""
        # Clear preview
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        self.preview_frame.configure(fg_color=self.current_theme["bg_primary"])

        # Add sample elements
        header = ctk.CTkLabel(
            self.preview_frame,
            text="Sample Header",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.current_theme["fg_primary"]
        )
        header.pack(pady=10)

        text = ctk.CTkLabel(
            self.preview_frame,
            text="Sample secondary text",
            text_color=self.current_theme["fg_secondary"]
        )
        text.pack(pady=5)

        card = ctk.CTkFrame(
            self.preview_frame,
            fg_color=self.current_theme["bg_secondary"]
        )
        card.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            card,
            text="Card with secondary background",
            text_color=self.current_theme["fg_primary"]
        ).pack(pady=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Accent",
            fg_color=self.current_theme["accent_color"]
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Success",
            fg_color=self.current_theme["success_color"]
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Warning",
            fg_color=self.current_theme["warning_color"]
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Error",
            fg_color=self.current_theme["error_color"]
        ).pack(side="left", padx=5)

    def save_current_theme(self):
        """Save the current theme"""
        name = self.theme_name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a theme name")
            return

        self.current_theme["name"] = name
        self.themes[name] = self.current_theme.copy()
        self.save_themes()
        messagebox.showinfo("Success", f"Theme '{name}' saved successfully!")

    def apply_theme(self):
        """Apply the current theme to the app"""
        # This would require modifying the app's color scheme
        # For now, just show a message
        messagebox.showinfo(
            "Apply Theme",
            "Theme application will be implemented in the next update!\n\n"
            "For now, themes are saved and can be loaded later."
        )

    def load_theme_dialog(self):
        """Show dialog to load a saved theme"""
        if not self.themes:
            messagebox.showinfo("No Themes", "No saved themes found. Create one first!")
            return

        # Create selection dialog
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Load Theme")
        dialog.geometry("400x500")

        ctk.CTkLabel(
            dialog,
            text="Select a Theme",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=20)

        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        for name, theme in self.themes.items():
            theme_frame = ctk.CTkFrame(scroll_frame)
            theme_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(
                theme_frame,
                text=name,
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=10, pady=10)

            ctk.CTkButton(
                theme_frame,
                text="Load",
                command=lambda t=theme: self.load_theme(t, dialog),
                width=80
            ).pack(side="right", padx=10)

    def load_theme(self, theme, dialog):
        """Load a specific theme"""
        self.current_theme = theme.copy()
        dialog.destroy()
        self.create_theme_editor(self.parent)
        messagebox.showinfo("Success", f"Theme '{theme['name']}' loaded!")

    def reset_theme(self):
        """Reset to default theme"""
        self.current_theme = {
            "name": "Custom Theme",
            "bg_primary": "#1e1e1e",
            "bg_secondary": "#2b2b2b",
            "fg_primary": "#ffffff",
            "fg_secondary": "#b0b0b0",
            "accent_color": "#2196F3",
            "success_color": "#4CAF50",
            "warning_color": "#FF9800",
            "error_color": "#F44336"
        }
        self.create_theme_editor(self.parent)
