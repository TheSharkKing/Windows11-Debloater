import winreg

def add_registry_key(key_path, value_name, value_data, value_type=winreg.REG_SZ):
    try:
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        return True
    except Exception as e:
        print(f"Error adding registry key: {e}")
        return False

def modify_registry_key(key_path, value_name, value_data, value_type=winreg.REG_SZ):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, value_name, 0, value_type, value_data)
        return True
    except FileNotFoundError:
        print("Registry key not found.")
        return False
    except Exception as e:
        print(f"Error modifying registry key: {e}")
        return False

def delete_registry_key(key_path, value_name):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, value_name)
        return True
    except FileNotFoundError:
        print("Registry value not found.")
        return False
    except Exception as e:
        print(f"Error deleting registry key: {e}")
        return False

def get_registry_value(key_path, value_name):
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            value, value_type = winreg.QueryValueEx(key, value_name)
            return value
    except FileNotFoundError:
        print("Registry value not found.")
        return None
    except Exception as e:
        print(f"Error retrieving registry value: {e}")
        return None

def clean_registry():
    """
    Cleans up unnecessary registry keys.
    """
    keys_to_remove = [
        r"Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run",
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    ]

    for key in keys_to_remove:
        try:
            print(f"Cleaning registry key: {key}")
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
                        print(f"Deleted registry value: {value_name}")
                    except Exception as e:
                        print(f"Failed to delete registry value {value_name}: {e}")
        except FileNotFoundError:
            print(f"Registry key not found: {key}")
        except Exception as e:
            print(f"Failed to clean registry key {key}: {e}")

def manage_registry_keys():
    print("Managing registry keys...")

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
                # Open the registry key
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteKey(key, "")
                print(f"Successfully removed: {key_path}")
            else:
                print(f"Skipped: {key_path}")
        except FileNotFoundError:
            print(f"Registry key not found: {key_path}")
        except PermissionError:
            print(f"Permission denied: {key_path}")
        except Exception as e:
            print(f"Failed to remove {key_path}: {e}")

    print("Registry management completed.")