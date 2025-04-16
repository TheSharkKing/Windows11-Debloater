import winreg
import logging

# Get the logger
logger = logging.getLogger("DebloaterLogger")

def add_registry_key(key_path, value_name, value_data, value_type=winreg.REG_SZ):
    try:
        logger.info(f"Adding registry key: {key_path}\\{value_name}")
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        logger.info(f"Successfully added registry key: {key_path}\\{value_name}")
        return True
    except Exception as e:
        logger.error(f"Error adding registry key {key_path}\\{value_name}: {e}")
        return False

def modify_registry_key(key_path, value_name, value_data, value_type=winreg.REG_SZ):
    try:
        logger.info(f"Modifying registry key: {key_path}\\{value_name}")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        logger.info(f"Successfully modified registry key: {key_path}\\{value_name}")
        return True
    except FileNotFoundError:
        logger.warning(f"Registry key not found: {key_path}\\{value_name}")
        return False
    except Exception as e:
        logger.error(f"Error modifying registry key {key_path}\\{value_name}: {e}")
        return False

def delete_registry_key(key_path, value_name):
    try:
        logger.info(f"Deleting registry key: {key_path}\\{value_name}")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
        logger.info(f"Successfully deleted registry key: {key_path}\\{value_name}")
        return True
    except FileNotFoundError:
        logger.warning(f"Registry value not found: {key_path}\\{value_name}")
        return False
    except Exception as e:
        logger.error(f"Error deleting registry key {key_path}\\{value_name}: {e}")
        return False

def get_registry_value(key_path, value_name):
    try:
        logger.info(f"Retrieving registry value: {key_path}\\{value_name}")
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, value_type = winreg.QueryValueEx(key, value_name)
            logger.info(f"Successfully retrieved registry value: {key_path}\\{value_name}")
            return value
    except FileNotFoundError:
        logger.warning(f"Registry value not found: {key_path}\\{value_name}")
        return None
    except Exception as e:
        logger.error(f"Error retrieving registry value {key_path}\\{value_name}: {e}")
        return None

def clean_registry():
    """
    Cleans up unnecessary registry keys.
    """
    logger.info("Starting registry cleanup")
    keys_to_remove = [
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run",
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    ]

    for key in keys_to_remove:
        try:
            logger.info(f"Cleaning registry key: {key}")
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as reg_key:
                # Collect all value names first
                value_names = []
                i = 0
                while True:
                    try:
                        value_name, _, _ = winreg.EnumValue(reg_key, i)
                        value_names.append(value_name)
                        i += 1
                    except OSError:
                        break

                # Delete all collected values
                for value_name in value_names:
                    try:
                        winreg.DeleteValue(reg_key, value_name)
                        logger.info(f"Deleted registry value: {key}\\{value_name}")
                    except Exception as e:
                        logger.error(f"Failed to delete registry value {key}\\{value_name}: {e}")
        except FileNotFoundError:
            logger.warning(f"Registry key not found: {key}")
        except Exception as e:
            logger.error(f"Failed to clean registry key {key}: {e}")
    
    logger.info("Registry cleanup completed")

def manage_registry_keys():
    logger.info("Starting registry management")

    # Example: List of unnecessary registry keys to remove
    unnecessary_keys = [
        r"Software\Microsoft\Windows\CurrentVersion\Run\UnneededApp",
        r"Software\UnwantedSoftware"
    ]

    for key_path in unnecessary_keys:
        try:
            # Ask the user for confirmation
            user_input = input(f"Do you want to remove the registry key: {key_path}? (y/n): ").strip().lower()
            if user_input == 'y':
                logger.info(f"User confirmed removal of registry key: {key_path}")
                # Open the registry key
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteKey(key, "")
                logger.info(f"Successfully removed: {key_path}")
            else:
                logger.info(f"User skipped removal of: {key_path}")
        except FileNotFoundError:
            logger.warning(f"Registry key not found: {key_path}")
        except PermissionError:
            logger.error(f"Permission denied: {key_path}")
        except Exception as e:
            logger.error(f"Failed to remove {key_path}: {e}")

    logger.info("Registry management completed")