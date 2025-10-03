"""
Simple build script without Unicode characters
"""
import PyInstaller.__main__
import sys
from pathlib import Path

ROOT = Path(__file__).parent
print("="*60)
print("Building Time Tracker Pro...")
print("="*60)

try:
    PyInstaller.__main__.run([
        str(ROOT / "gui_tracker.py"),
        "--name=TimeTrackerPro",
        "--onefile",
        "--windowed",
        "--clean",

        # Hidden imports
        "--hidden-import=win32gui",
        "--hidden-import=win32process",
        "--hidden-import=psutil",
        "--hidden-import=customtkinter",
        "--hidden-import=matplotlib.backends.backend_tkagg",

        # Add UI files
        f"--add-data={ROOT / 'ui'};ui",

        # Exclude heavy modules
        "--exclude-module=pandas",
        "--exclude-module=tensorflow",
        "--exclude-module=torch",
        "--exclude-module=scipy",
        "--exclude-module=IPython",
        "--exclude-module=jupyter",

        # Optimize
        "--optimize=2",
        "--noupx",
    ])
    print("\n" + "="*60)
    print("BUILD COMPLETE!")
    print("="*60)
    print(f"Output: dist/TimeTrackerPro.exe")
except Exception as e:
    print(f"\nBUILD FAILED: {e}")
    sys.exit(1)
