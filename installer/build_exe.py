"""
Build script for creating Time Tracker executable
Uses PyInstaller to create a standalone EXE
"""

import PyInstaller.__main__
import os
import sys
import shutil
from pathlib import Path

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.absolute()
DIST_DIR = ROOT_DIR / "dist"
BUILD_DIR = ROOT_DIR / "build"

def clean_build():
    """Clean previous build artifacts"""
    print("[*] Cleaning previous builds...")
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    spec_file = ROOT_DIR / "gui_tracker.spec"
    if spec_file.exists():
        spec_file.unlink()
    print("[OK] Clean complete\n")

def create_icon():
    """Create a simple icon if none exists"""
    icon_path = ROOT_DIR / "assets" / "icon.ico"
    if not icon_path.exists():
        print("[*] Creating default icon...")
        os.makedirs(ROOT_DIR / "assets", exist_ok=True)

        # Create a simple icon using PIL
        try:
            from PIL import Image, ImageDraw

            # Create image
            img = Image.new('RGB', (256, 256), color='#1a1a1a')
            draw = ImageDraw.Draw(img)

            # Draw clock face
            draw.ellipse([28, 28, 228, 228], fill='#4a9eff', outline='white', width=4)

            # Draw clock hands
            center = (128, 128)
            # Hour hand
            draw.line([center, (128, 80)], fill='white', width=8)
            # Minute hand
            draw.line([center, (160, 128)], fill='white', width=6)

            # Save as ICO
            img.save(icon_path, format='ICO', sizes=[(256, 256)])
            print(f"[OK] Icon created at {icon_path}\n")
        except Exception as e:
            print(f"[WARN] Could not create icon: {e}")
            return None

    return str(icon_path)

def build_exe():
    """Build the executable using PyInstaller"""
    print("🔨 Building Time Tracker executable...\n")

    # Create icon
    icon_path = create_icon()

    # PyInstaller arguments
    args = [
        str(ROOT_DIR / "gui_tracker.py"),  # Main script
        "--name=TimeTrackerPro",
        "--onefile",  # Single executable
        "--windowed",  # No console window
        "--clean",
        f"--distpath={DIST_DIR}",
        f"--workpath={BUILD_DIR}",
        f"--specpath={ROOT_DIR}",

        # Add icon
        f"--icon={icon_path}" if icon_path else "",

        # Hidden imports (important!)
        "--hidden-import=win32gui",
        "--hidden-import=win32process",
        "--hidden-import=psutil",
        "--hidden-import=plyer",
        "--hidden-import=pystray",
        "--hidden-import=PIL",
        "--hidden-import=customtkinter",
        "--hidden-import=tkinter",
        "--hidden-import=matplotlib",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=openpyxl",
        "--hidden-import=reportlab",

        # Add data files
        f"--add-data={ROOT_DIR / 'ui'};ui",

        # Exclude unnecessary modules to reduce size
        "--exclude-module=tests",
        "--exclude-module=jupyter",
        "--exclude-module=notebook",
        "--exclude-module=IPython",
        "--exclude-module=pandas",
        "--exclude-module=numpy.distutils",
        "--exclude-module=tensorflow",
        "--exclude-module=torch",
        "--exclude-module=scipy",

        # Optimization
        "--optimize=2",

        # No UPX (causes issues with some antivirus)
        "--noupx",
    ]

    # Filter empty strings
    args = [arg for arg in args if arg]

    print("📦 PyInstaller arguments:")
    for arg in args:
        print(f"   {arg}")
    print()

    # Run PyInstaller
    try:
        PyInstaller.__main__.run(args)
        print("\n✅ Build completed successfully!")
        print(f"📁 Executable location: {DIST_DIR / 'TimeTrackerPro.exe'}")
        print(f"📊 Size: {(DIST_DIR / 'TimeTrackerPro.exe').stat().st_size / 1024 / 1024:.1f} MB")
        return True
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        return False

def test_exe():
    """Test if the executable works"""
    exe_path = DIST_DIR / "TimeTrackerPro.exe"
    if not exe_path.exists():
        print("❌ Executable not found!")
        return False

    print("\n🧪 Testing executable...")
    print("   (The app should launch. Close it to continue)")

    import subprocess
    try:
        # Launch the exe (will block until closed)
        result = subprocess.run([str(exe_path)], timeout=30)
        if result.returncode == 0:
            print("✅ Test passed!")
            return True
        else:
            print(f"⚠️  Exe exited with code {result.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print("✅ Exe is running (timeout reached, assuming success)")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_readme():
    """Create README for distribution"""
    readme_path = DIST_DIR / "README.txt"
    content = """
===========================================
    Time Tracker Pro - Installation
===========================================

Thank you for downloading Time Tracker Pro!

QUICK START:
1. Double-click TimeTrackerPro.exe to launch
2. Click "Start Tracking" to begin
3. The app will track your time automatically

FEATURES:
- Automatic time tracking
- Real-time dashboard
- Goal setting and tracking
- Focus mode
- Project tracking
- And much more!

FIRST TIME SETUP:
On first run, the app will:
- Request necessary permissions
- Configure auto-start (optional)
- Create data files in your user directory

DATA LOCATION:
Your tracking data is stored at:
%USERPROFILE%\\time_tracking.json

SUPPORT:
For help and documentation, visit:
https://github.com/yourusername/time-tracker

REQUIREMENTS:
- Windows 10/11 (64-bit)
- No additional software needed!

===========================================
        © 2024 Time Tracker Pro
===========================================
"""
    with open(readme_path, 'w') as f:
        f.write(content)
    print(f"📝 Created {readme_path}")

def main():
    """Main build process"""
    print("="*60)
    print("  TIME TRACKER PRO - EXE BUILD SCRIPT")
    print("="*60)
    print()

    # Step 1: Clean
    clean_build()

    # Step 2: Build
    if not build_exe():
        sys.exit(1)

    # Step 3: Create README
    create_readme()

    # Step 4: Test (optional)
    test_choice = input("\n🧪 Would you like to test the executable? (y/n): ")
    if test_choice.lower() == 'y':
        test_exe()

    print("\n" + "="*60)
    print("  BUILD COMPLETE!")
    print("="*60)
    print(f"\n📁 Output directory: {DIST_DIR}")
    print("\nNext steps:")
    print("1. Test TimeTrackerPro.exe manually")
    print("2. Run InnoSetup to create installer (installer/setup.iss)")
    print("3. Distribute TimeTrackerSetup.exe to users")
    print()

if __name__ == "__main__":
    main()
