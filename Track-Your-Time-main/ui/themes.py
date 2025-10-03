"""
Theme configuration for the Time Tracker GUI
"""

# Color schemes
DARK_THEME = {
    "bg_color": "#1a1a1a",
    "fg_color": "#ffffff",
    "surface": "#2d2d2d",
    "surface_light": "#3d3d3d",
    "primary": "#4a9eff",
    "primary_hover": "#6ab4ff",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196f3",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "border": "#404040",
    "coding": "#4a9eff",
    "productivity": "#9c27b0",
    "entertainment": "#ff5722",
    "communication": "#00bcd4",
    "design": "#e91e63",
    "social_media": "#ff4081",
    "education": "#8bc34a",
    "reading": "#795548",
    "finance": "#ffc107",
    "browsing": "#607d8b",
}

LIGHT_THEME = {
    "bg_color": "#f5f5f5",
    "fg_color": "#000000",
    "surface": "#ffffff",
    "surface_light": "#fafafa",
    "primary": "#2196f3",
    "primary_hover": "#1976d2",
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196f3",
    "text_primary": "#212121",
    "text_secondary": "#757575",
    "border": "#e0e0e0",
    "coding": "#2196f3",
    "productivity": "#9c27b0",
    "entertainment": "#ff5722",
    "communication": "#00bcd4",
    "design": "#e91e63",
    "social_media": "#ff4081",
    "education": "#8bc34a",
    "reading": "#795548",
    "finance": "#ffc107",
    "browsing": "#607d8b",
}

# Category colors (consistent across themes)
CATEGORY_COLORS = {
    "Coding": "#4a9eff",
    "Productivity": "#9c27b0",
    "Entertainment": "#ff5722",
    "Communication": "#00bcd4",
    "Design": "#e91e63",
    "Social Media": "#ff4081",
    "Education": "#8bc34a",
    "Reading": "#795548",
    "Finance": "#ffc107",
    "Browsing": "#607d8b",
    "Utilities": "#9e9e9e",
    "Shopping": "#ff6f00",
    "Other": "#666666",
}

def get_theme(is_dark=True):
    """Get current theme colors"""
    return DARK_THEME if is_dark else LIGHT_THEME

def get_category_color(category):
    """Get color for a specific category"""
    return CATEGORY_COLORS.get(category, CATEGORY_COLORS["Other"])
