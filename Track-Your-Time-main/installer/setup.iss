; Time Tracker Pro - InnoSetup Installer Script
; This creates a professional Windows installer with auto-start capability

#define MyAppName "Time Tracker Pro"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Your Company"
#define MyAppURL "https://yourwebsite.com"
#define MyAppExeName "TimeTrackerPro.exe"

[Setup]
; App information
AppId={{8A9B5C6D-1234-5678-9ABC-DEF012345678}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Output
OutputDir=..\dist\installer
OutputBaseFilename=TimeTrackerProSetup
UninstallDisplayIcon={app}\{#MyAppExeName}

; Compression
Compression=lzma2/max
SolidCompression=yes

; Windows version
MinVersion=10.0
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

; Privileges
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; Appearance
WizardStyle=modern
DisableWelcomePage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Start {#MyAppName} automatically when Windows starts"; GroupDescription: "Startup Options:"

[Files]
; Main executable
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "..\dist\README.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; DestName: "README_FULL.md"; Flags: ignoreversion

; Dependencies check script (optional)
Source: "first_run.py"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; Desktop icon (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; Startup folder (auto-start)
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Parameters: "start --minimized"; Tasks: autostart

[Run]
; Run first-time setup
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  FirstRunPage: TInputOptionWizardPage;
  AutoStartCheckBox: TNewCheckBox;
  MinimizeToTrayCheckBox: TNewCheckBox;

procedure InitializeWizard;
begin
  // Create custom page for first-run options
  FirstRunPage := CreateInputOptionPage(wpSelectTasks,
    'Initial Configuration', 'Configure your time tracking preferences',
    'Please select your preferred settings. You can change these later in the application.',
    False, False);

  FirstRunPage.Add('Enable notifications');
  FirstRunPage.Add('Enable focus mode alerts');
  FirstRunPage.Add('Track browser activity');

  // Set defaults
  FirstRunPage.Values[0] := True;  // Notifications enabled
  FirstRunPage.Values[1] := True;  // Focus mode enabled
  FirstRunPage.Values[2] := True;  // Browser tracking enabled
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigFile: String;
  ConfigContent: TStringList;
begin
  if CurStep = ssPostInstall then
  begin
    // Create initial config file based on user selections
    ConfigFile := ExpandConstant('{%USERPROFILE}') + '\tracker_config.json';

    if not FileExists(ConfigFile) then
    begin
      ConfigContent := TStringList.Create;
      try
        ConfigContent.Add('{');
        ConfigContent.Add('  "idle_threshold_seconds": 300,');

        if FirstRunPage.Values[0] then
          ConfigContent.Add('  "notifications_enabled": true,')
        else
          ConfigContent.Add('  "notifications_enabled": false,');

        if FirstRunPage.Values[1] then
          ConfigContent.Add('  "focus_mode_alerts": true,')
        else
          ConfigContent.Add('  "focus_mode_alerts": false,');

        if FirstRunPage.Values[2] then
          ConfigContent.Add('  "track_browser": true,')
        else
          ConfigContent.Add('  "track_browser": false,');

        ConfigContent.Add('  "goals": {');
        ConfigContent.Add('    "Coding": 4,');
        ConfigContent.Add('    "Entertainment": 2');
        ConfigContent.Add('  },');
        ConfigContent.Add('  "custom_categories": {},');
        ConfigContent.Add('  "first_run": true');
        ConfigContent.Add('}');

        ConfigContent.SaveToFile(ConfigFile);
      finally
        ConfigContent.Free;
      end;
    end;
  end;
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if already installed
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\{#MyAppName}') then
  begin
    if MsgBox('Time Tracker Pro is already installed. Do you want to reinstall it?',
              mbConfirmation, MB_YESNO) = IDNO then
    begin
      Result := False;
      Exit;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  DataFile, ConfigFile: String;
  ResultCode: Integer;
begin
  if CurUninstallStep = usPostUninstall then
  begin
    DataFile := ExpandConstant('{%USERPROFILE}') + '\time_tracking.json';
    ConfigFile := ExpandConstant('{%USERPROFILE}') + '\tracker_config.json';

    // Ask if user wants to keep data
    if FileExists(DataFile) or FileExists(ConfigFile) then
    begin
      if MsgBox('Do you want to keep your tracking data and settings?' + #13#10 +
                'Choose "No" to delete all data.',
                mbConfirmation, MB_YESNO) = IDNO then
      begin
        if FileExists(DataFile) then
          DeleteFile(DataFile);
        if FileExists(ConfigFile) then
          DeleteFile(ConfigFile);
      end;
    end;
  end;
end;

[UninstallDelete]
Type: files; Name: "{app}\*.log"
Type: files; Name: "{app}\*.tmp"

[Registry]
; Register application for auto-update checks
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "Version"; ValueData: "{#MyAppVersion}"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"; Flags: uninsdeletekey

[Messages]
WelcomeLabel2=This will install [name/ver] on your computer.%n%nTime Tracker Pro is a powerful time tracking application that helps you understand how you spend your time.%n%nFeatures:%n• Automatic time tracking%n• Beautiful dashboard%n• Goal setting%n• Focus mode%n• Project tracking%n%nIt is recommended that you close all other applications before continuing.
