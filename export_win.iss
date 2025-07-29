[Setup]
AppName=Mantapy
AppVersion=1.0
DefaultDirName={pf}\Mantapy
DefaultGroupName=Mantapy
OutputBaseFilename=mantapy_installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs
Source: "assets\logo_mantapy.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Mantapy"; Filename: "{app}\main.exe"; IconFilename: "{app}\logo_mantapy.ico"

