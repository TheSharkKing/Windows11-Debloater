import subprocess
import logging
import os

# Get the logger
logger = logging.getLogger("DebloaterLogger")

def disable_onedrive():
    """
    Uninstalls and disables OneDrive.
    """
    logger.info("Starting OneDrive disabling process")
    
    # First, check if OneDrive is installed
    onedrive_path_64 = os.path.expandvars("%SystemRoot%\\SysWOW64\\OneDriveSetup.exe")
    onedrive_path_32 = os.path.expandvars("%SystemRoot%\\System32\\OneDriveSetup.exe")
    
    if os.path.exists(onedrive_path_64):
        onedrive_path = onedrive_path_64
        logger.info("Found 64-bit OneDrive setup")
    elif os.path.exists(onedrive_path_32):
        onedrive_path = onedrive_path_32
        logger.info("Found 32-bit OneDrive setup")
    else:
        logger.warning("OneDrive setup not found in expected locations")
        onedrive_path = None
    
    if onedrive_path:
        try:
            logger.info("Uninstalling OneDrive...")
            result = subprocess.run(
                ["powershell", "-Command", f"Start-Process '{onedrive_path}' -ArgumentList '/uninstall' -Wait"],
                check=True,
                shell=True,
                capture_output=True,
                text=True
            )
            if result.stderr:
                logger.warning(f"OneDrive uninstall stderr: {result.stderr}")
            logger.info("OneDrive uninstalled successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to uninstall OneDrive: {e}")
            logger.error(f"Error output: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
        except Exception as e:
            logger.error(f"Unexpected error uninstalling OneDrive: {str(e)}")
    else:
        logger.info("Skipping OneDrive uninstallation as setup was not found")

    try:
        logger.info("Disabling OneDrive integration via registry...")
        result = subprocess.run(
            ["reg", "add", "HKLM\\Software\\Policies\\Microsoft\\Windows\\OneDrive", "/v", "DisableFileSync", "/t", "REG_DWORD", "/d", "1", "/f"],
            check=True,
            capture_output=True,
            text=True
        )
        if result.stderr:
            logger.warning(f"Registry modification stderr: {result.stderr}")
        logger.info("OneDrive integration disabled successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to disable OneDrive integration: {e}")
        logger.error(f"Error output: {e.stderr if hasattr(e, 'stderr') else 'No error output'}")
    except Exception as e:
        logger.error(f"Unexpected error disabling OneDrive integration: {str(e)}")

    logger.info("OneDrive disabling process completed")