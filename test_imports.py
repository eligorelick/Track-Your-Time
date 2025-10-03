"""
Quick test to verify all modules can be imported
Run this to check if all dependencies are installed correctly
"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"[OK] {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"[FAIL] {package_name or module_name} - {str(e)}")
        return False

def main():
    print("=" * 50)
    print("Testing Time Tracker Pro Dependencies")
    print("=" * 50)
    print()

    success_count = 0
    total_count = 0

    # Core dependencies
    print("Core Dependencies:")
    tests = [
        ("psutil", "psutil"),
        ("json", "json (built-in)"),
        ("datetime", "datetime (built-in)"),
        ("collections", "collections (built-in)"),
    ]

    for module, name in tests:
        total_count += 1
        if test_import(module, name):
            success_count += 1

    print()

    # GUI dependencies
    print("GUI Framework:")
    gui_tests = [
        ("customtkinter", "customtkinter"),
        ("tkinter", "tkinter (built-in)"),
    ]

    for module, name in gui_tests:
        total_count += 1
        if test_import(module, name):
            success_count += 1

    print()

    # Feature dependencies
    print("Feature Dependencies:")
    feature_tests = [
        ("matplotlib", "matplotlib (charts)"),
        ("openpyxl", "openpyxl (Excel export)"),
        ("reportlab", "reportlab (PDF export)"),
        ("plyer", "plyer (notifications)"),
        ("pystray", "pystray (system tray)"),
        ("PIL", "Pillow (images)"),
    ]

    for module, name in feature_tests:
        total_count += 1
        if test_import(module, name):
            success_count += 1

    print()

    # Email dependencies
    print("Email Dependencies:")
    email_tests = [
        ("smtplib", "smtplib (built-in)"),
        ("email", "email (built-in)"),
    ]

    for module, name in email_tests:
        total_count += 1
        if test_import(module, name):
            success_count += 1

    print()

    # Windows-specific
    if sys.platform == 'win32':
        print("Windows-specific:")
        win_tests = [
            ("win32gui", "pywin32 (win32gui)"),
            ("win32process", "pywin32 (win32process)"),
        ]

        for module, name in win_tests:
            total_count += 1
            if test_import(module, name):
                success_count += 1
        print()

    # Test our modules
    print("Time Tracker Modules:")
    our_tests = [
        ("ui.themes", "ui.themes"),
        ("ui.analytics_charts", "ui.analytics_charts"),
        ("ui.calendar_view", "ui.calendar_view"),
        ("ui.theme_creator", "ui.theme_creator"),
        ("ui.keyboard_shortcuts", "ui.keyboard_shortcuts"),
        ("ui.email_reports", "ui.email_reports"),
        ("ui.export_formats", "ui.export_formats"),
        ("ui.pomodoro_timer", "ui.pomodoro_timer"),
        ("ui.tags_system", "ui.tags_system"),
    ]

    for module, name in our_tests:
        total_count += 1
        if test_import(module, name):
            success_count += 1

    print()
    print("=" * 50)
    print(f"Result: {success_count}/{total_count} modules imported successfully")
    print("=" * 50)

    if success_count == total_count:
        print("[SUCCESS] ALL TESTS PASSED!")
        print("\nYou're ready to run Time Tracker Pro!")
        return 0
    else:
        print("[ERROR] SOME TESTS FAILED")
        print(f"\nMissing dependencies: {total_count - success_count}")
        print("\nInstall missing packages with:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
