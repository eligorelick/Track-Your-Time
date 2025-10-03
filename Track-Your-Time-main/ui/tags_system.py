"""
Tags System for Time Tracker
Allows tagging activities with custom labels for better organization
"""

import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
from collections import defaultdict

class TagsSystem:
    """Manage activity tags"""

    def __init__(self, parent, tracker):
        self.parent = parent
        self.tracker = tracker
        self.tags_file = "activity_tags.json"
        self.tags_data = self.load_tags()

    def load_tags(self):
        """Load tags data"""
        if os.path.exists(self.tags_file):
            try:
                with open(self.tags_file, 'r') as f:
                    return json.load(f)
            except:
                return {"tags": [], "activity_tags": {}}
        return {"tags": [], "activity_tags": {}}

    def save_tags(self):
        """Save tags data"""
        with open(self.tags_file, 'w') as f:
            json.dump(self.tags_data, f, indent=2)

    def create_tags_ui(self, frame):
        """Create tags management UI"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header
        header = ctk.CTkLabel(
            frame,
            text="🏷️ Activity Tags",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        header.pack(pady=20)

        # Main content with two panels
        content_frame = ctk.CTkFrame(frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Tag management
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            left_panel,
            text="Available Tags",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        # Tag list
        tags_scroll = ctk.CTkScrollableFrame(left_panel, height=300)
        tags_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.tag_frames = {}
        self.refresh_tag_list(tags_scroll)

        # Add new tag
        add_frame = ctk.CTkFrame(left_panel)
        add_frame.pack(fill="x", padx=10, pady=10)

        self.new_tag_entry = ctk.CTkEntry(
            add_frame,
            placeholder_text="New tag name...",
            height=40
        )
        self.new_tag_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.color_var = ctk.StringVar(value="#2196F3")
        color_btn = ctk.CTkButton(
            add_frame,
            text="🎨",
            command=self.pick_tag_color,
            width=50,
            height=40,
            fg_color=self.color_var.get()
        )
        color_btn.pack(side="left", padx=5)
        self.color_btn = color_btn

        ctk.CTkButton(
            add_frame,
            text="➕ Add Tag",
            command=self.add_new_tag,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049"
        ).pack(side="left", padx=5)

        # Right panel - Tag analytics
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(
            right_panel,
            text="Tag Analytics",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=15)

        # Analytics scroll
        analytics_scroll = ctk.CTkScrollableFrame(right_panel)
        analytics_scroll.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_analytics(analytics_scroll)

        # Bottom panel - Quick tag selector
        quick_panel = ctk.CTkFrame(frame)
        quick_panel.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(
            quick_panel,
            text="Quick Tag Current Activity",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))

        # Current activity display
        current_app = self.tracker.current_app or "No active tracking"
        self.current_activity_label = ctk.CTkLabel(
            quick_panel,
            text=f"Current: {current_app}",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.current_activity_label.pack(pady=5)

        # Quick tag buttons
        quick_tags_frame = ctk.CTkFrame(quick_panel, fg_color="transparent")
        quick_tags_frame.pack(fill="x", padx=20, pady=10)

        for tag in self.tags_data.get("tags", [])[:6]:  # Show first 6 tags
            tag_btn = ctk.CTkButton(
                quick_tags_frame,
                text=f"🏷️ {tag['name']}",
                command=lambda t=tag: self.quick_tag_activity(t),
                fg_color=tag.get('color', '#2196F3'),
                height=35
            )
            tag_btn.pack(side="left", padx=5, expand=True)

    def refresh_tag_list(self, parent):
        """Refresh the tag list display"""
        # Clear existing
        for widget in parent.winfo_children():
            widget.destroy()

        tags = self.tags_data.get("tags", [])

        if not tags:
            ctk.CTkLabel(
                parent,
                text="No tags yet. Create one below!",
                text_color="gray"
            ).pack(pady=20)
            return

        for tag in tags:
            tag_frame = ctk.CTkFrame(parent)
            tag_frame.pack(fill="x", pady=5, padx=5)

            # Color indicator
            color_box = ctk.CTkFrame(
                tag_frame,
                width=30,
                height=30,
                fg_color=tag.get('color', '#2196F3'),
                corner_radius=6
            )
            color_box.pack(side="left", padx=10, pady=5)

            # Tag name
            ctk.CTkLabel(
                tag_frame,
                text=tag['name'],
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(side="left", padx=10)

            # Usage count
            usage_count = self.get_tag_usage_count(tag['name'])
            ctk.CTkLabel(
                tag_frame,
                text=f"({usage_count} uses)",
                font=ctk.CTkFont(size=12),
                text_color="gray"
            ).pack(side="left", padx=5)

            # Delete button
            ctk.CTkButton(
                tag_frame,
                text="✖",
                command=lambda t=tag: self.delete_tag(t),
                width=35,
                height=35,
                fg_color="#F44336",
                hover_color="#D32F2F"
            ).pack(side="right", padx=5)

    def refresh_analytics(self, parent):
        """Refresh analytics display"""
        # Clear existing
        for widget in parent.winfo_children():
            widget.destroy()

        # Calculate tag statistics
        tag_stats = defaultdict(lambda: {'count': 0, 'total_time': 0})

        for activity, tags in self.tags_data.get("activity_tags", {}).items():
            for tag_name in tags:
                tag_stats[tag_name]['count'] += 1
                # You could add time tracking here if available
                tag_stats[tag_name]['total_time'] += 1  # Placeholder

        if not tag_stats:
            ctk.CTkLabel(
                parent,
                text="No tag data yet.\nStart tagging activities!",
                text_color="gray",
                justify="center"
            ).pack(pady=20)
            return

        # Display stats
        for tag_name, stats in sorted(tag_stats.items(), key=lambda x: x[1]['count'], reverse=True):
            tag = self.get_tag_by_name(tag_name)
            if not tag:
                continue

            stat_frame = ctk.CTkFrame(parent)
            stat_frame.pack(fill="x", pady=8, padx=5)

            # Tag color
            color_box = ctk.CTkFrame(
                stat_frame,
                width=25,
                height=25,
                fg_color=tag.get('color', '#2196F3'),
                corner_radius=4
            )
            color_box.pack(side="left", padx=10, pady=10)

            # Tag info
            info_frame = ctk.CTkFrame(stat_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="x", expand=True, padx=5)

            ctk.CTkLabel(
                info_frame,
                text=tag_name,
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            ).pack(anchor="w")

            ctk.CTkLabel(
                info_frame,
                text=f"{stats['count']} activities tagged",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            ).pack(anchor="w")

    def pick_tag_color(self):
        """Pick color for new tag"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(initialcolor=self.color_var.get())
        if color[1]:
            self.color_var.set(color[1])
            self.color_btn.configure(fg_color=color[1])

    def add_new_tag(self):
        """Add a new tag"""
        tag_name = self.new_tag_entry.get().strip()

        if not tag_name:
            messagebox.showerror("Error", "Please enter a tag name")
            return

        # Check if tag exists
        if any(t['name'].lower() == tag_name.lower() for t in self.tags_data.get("tags", [])):
            messagebox.showerror("Error", "Tag already exists")
            return

        # Add tag
        if "tags" not in self.tags_data:
            self.tags_data["tags"] = []

        self.tags_data["tags"].append({
            "name": tag_name,
            "color": self.color_var.get(),
            "created": datetime.now().isoformat()
        })

        self.save_tags()
        self.new_tag_entry.delete(0, 'end')

        # Refresh UI
        self.create_tags_ui(self.parent)
        messagebox.showinfo("Success", f"Tag '{tag_name}' created!")

    def delete_tag(self, tag):
        """Delete a tag"""
        if messagebox.askyesno("Confirm Delete", f"Delete tag '{tag['name']}'?"):
            # Remove from tags list
            self.tags_data["tags"] = [t for t in self.tags_data.get("tags", [])
                                      if t['name'] != tag['name']]

            # Remove from all activities
            activity_tags = self.tags_data.get("activity_tags", {})
            for activity in activity_tags:
                if tag['name'] in activity_tags[activity]:
                    activity_tags[activity].remove(tag['name'])

            self.save_tags()
            self.create_tags_ui(self.parent)

    def quick_tag_activity(self, tag):
        """Quickly tag the current activity"""
        if not self.tracker.current_app:
            messagebox.showinfo("No Activity", "No active tracking to tag")
            return

        activity = self.tracker.current_app

        if "activity_tags" not in self.tags_data:
            self.tags_data["activity_tags"] = {}

        if activity not in self.tags_data["activity_tags"]:
            self.tags_data["activity_tags"][activity] = []

        if tag['name'] not in self.tags_data["activity_tags"][activity]:
            self.tags_data["activity_tags"][activity].append(tag['name'])
            self.save_tags()
            messagebox.showinfo("Success", f"Tagged '{activity}' with '{tag['name']}'")
            self.refresh_analytics(self.parent)
        else:
            messagebox.showinfo("Already Tagged", f"'{activity}' already has tag '{tag['name']}'")

    def get_tag_by_name(self, name):
        """Get tag object by name"""
        for tag in self.tags_data.get("tags", []):
            if tag['name'] == name:
                return tag
        return None

    def get_tag_usage_count(self, tag_name):
        """Get usage count for a tag"""
        count = 0
        for activity, tags in self.tags_data.get("activity_tags", {}).items():
            if tag_name in tags:
                count += 1
        return count

    def get_activities_by_tag(self, tag_name):
        """Get all activities with a specific tag"""
        activities = []
        for activity, tags in self.tags_data.get("activity_tags", {}).items():
            if tag_name in tags:
                activities.append(activity)
        return activities

    def get_tags_for_activity(self, activity):
        """Get all tags for a specific activity"""
        return self.tags_data.get("activity_tags", {}).get(activity, [])

    def create_tag_filter_view(self, frame):
        """Create a view to filter activities by tag"""
        # Clear frame
        for widget in frame.winfo_children():
            widget.destroy()

        # Header
        ctk.CTkLabel(
            frame,
            text="Filter by Tag",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Tag selector
        tag_frame = ctk.CTkFrame(frame)
        tag_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            tag_frame,
            text="Select Tag:",
            font=ctk.CTkFont(size=14)
        ).pack(side="left", padx=10)

        tag_names = [t['name'] for t in self.tags_data.get("tags", [])]
        if not tag_names:
            tag_names = ["No tags available"]

        self.filter_tag_var = ctk.StringVar(value=tag_names[0] if tag_names else "")
        tag_menu = ctk.CTkOptionMenu(
            tag_frame,
            values=tag_names,
            variable=self.filter_tag_var,
            command=lambda x: self.show_filtered_activities(frame),
            width=200
        )
        tag_menu.pack(side="left", padx=10)

        # Results frame
        self.results_frame = ctk.CTkScrollableFrame(frame)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Initial display
        if tag_names[0] != "No tags available":
            self.show_filtered_activities(frame)

    def show_filtered_activities(self, parent_frame):
        """Show activities filtered by selected tag"""
        # Clear results
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        selected_tag = self.filter_tag_var.get()
        activities = self.get_activities_by_tag(selected_tag)

        if not activities:
            ctk.CTkLabel(
                self.results_frame,
                text=f"No activities tagged with '{selected_tag}'",
                text_color="gray"
            ).pack(pady=20)
            return

        for activity in activities:
            activity_frame = ctk.CTkFrame(self.results_frame)
            activity_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(
                activity_frame,
                text=activity,
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=15, pady=10)

            # Show all tags for this activity
            other_tags = [t for t in self.get_tags_for_activity(activity) if t != selected_tag]
            if other_tags:
                tags_text = ", ".join(other_tags)
                ctk.CTkLabel(
                    activity_frame,
                    text=f"Also: {tags_text}",
                    font=ctk.CTkFont(size=11),
                    text_color="gray"
                ).pack(side="left", padx=5)
