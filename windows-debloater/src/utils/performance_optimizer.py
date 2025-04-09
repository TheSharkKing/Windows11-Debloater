import os
import subprocess

def optimize_performance():
    print("Starting system performance optimization...")

    # 1. Disable unnecessary startup programs
    print("Disabling unnecessary startup programs...")
    subprocess.run("powershell -Command \"Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run | Remove-ItemProperty -Name *\"", shell=True)

    # 2. Set power plan to High Performance
    print("Setting power plan to High Performance...")
    subprocess.run("powercfg -setactive SCHEME_MIN", shell=True)

    # 3. Clear temporary files
    print("Clearing temporary files...")
    temp_dirs = [os.getenv('TEMP'), os.getenv('TMP')]
    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    try:
                        os.remove(os.path.join(root, file))
                    except Exception as e:
                        print(f"Failed to delete {file}: {e}")

    # 4. Optimize system services (example: disabling SysMain for older systems)
    print("Disabling SysMain service (if applicable)...")
    subprocess.run("sc config SysMain start= disabled", shell=True)
    subprocess.run("sc stop SysMain", shell=True)

    print("System performance optimization completed.")