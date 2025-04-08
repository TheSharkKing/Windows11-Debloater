import subprocess

def disable_onedrive():
    """
    Uninstalls and disables OneDrive.
    """
    try:
        print("Uninstalling OneDrive...")
        subprocess.run(
            ["powershell", "-Command", "Start-Process 'C:\\Windows\\SysWOW64\\OneDriveSetup.exe' -ArgumentList '/uninstall' -Wait"],
            check=True,
            shell=True
        )
        print("OneDrive uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to uninstall OneDrive: {e}")

    try:
        print("Disabling OneDrive integration...")
        subprocess.run(
            ["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive", "/v", "DisableFileSync", "/t", "REG_DWORD", "/d", "1", "/f"],
            check=True
        )
        print("OneDrive integration disabled.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable OneDrive: {e}")