import os
import sys
import ctypes
import subprocess

def is_admin():
    """
    Check if the current process has administrator privileges.
    Returns True if running as admin, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """
    Re-runs the current script with administrator privileges if not already running as admin.
    Returns True if already admin or successfully restarted with admin privileges.
    Returns False if failed to restart with admin privileges.
    """
    if is_admin():
        return True
    else:
        try:
            # Get the full path of the current script
            script = os.path.abspath(sys.argv[0])
            params = ' '.join([f'"{item}"' for item in sys.argv[1:]])
            
            # Use ctypes to trigger UAC and restart with admin privileges
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{script}" {params}', 
                None, 
                1
            )
            # Exit the current non-admin process
            sys.exit()
        except Exception as e:
            return False