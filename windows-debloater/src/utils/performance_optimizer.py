import os
import subprocess
import logging

# Get the logger
logger = logging.getLogger("DebloaterLogger")

def optimize_performance():
    logger.info("Starting system performance optimization...")

    # 1. Disable unnecessary startup programs
    logger.info("Disabling unnecessary startup programs...")
    try:
        result = subprocess.run(
            "powershell -Command \"Get-ItemProperty HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run | Remove-ItemProperty -Name *\"", 
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stderr:
            logger.warning(f"Startup program disabling stderr: {result.stderr}")
        logger.info("Successfully disabled startup programs")
    except Exception as e:
        logger.error(f"Failed to disable startup programs: {str(e)}")

    # 2. Set power plan to High Performance
    logger.info("Setting power plan to High Performance...")
    try:
        result = subprocess.run(
            "powercfg -setactive SCHEME_MIN", 
            shell=True,
            capture_output=True,
            text=True
        )
        if result.stderr:
            logger.warning(f"Power plan setting stderr: {result.stderr}")
        logger.info("Successfully set power plan to High Performance")
    except Exception as e:
        logger.error(f"Failed to set power plan: {str(e)}")

    # 3. Clear temporary files
    logger.info("Clearing temporary files...")
    temp_dirs = [os.getenv('TEMP'), os.getenv('TMP')]
    deleted_count = 0
    error_count = 0
    
    for temp_dir in temp_dirs:
        if temp_dir and os.path.exists(temp_dir):
            logger.info(f"Processing temp directory: {temp_dir}")
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        deleted_count += 1
                    except Exception as e:
                        logger.debug(f"Failed to delete {file_path}: {e}")
                        error_count += 1
    
    logger.info(f"Temporary files cleanup completed. Files deleted: {deleted_count}, Errors: {error_count}")

    # 4. Optimize system services (example: disabling SysMain for older systems)
    logger.info("Disabling SysMain service (if applicable)...")
    try:
        config_result = subprocess.run(
            "sc config SysMain start= disabled", 
            shell=True,
            capture_output=True,
            text=True
        )
        stop_result = subprocess.run(
            "sc stop SysMain", 
            shell=True, 
            capture_output=True,
            text=True
        )
        
        if config_result.stderr:
            logger.warning(f"SysMain config stderr: {config_result.stderr}")
        if stop_result.stderr:
            logger.warning(f"SysMain stop stderr: {stop_result.stderr}")
            
        logger.info("SysMain service has been disabled")
    except Exception as e:
        logger.error(f"Failed to disable SysMain service: {str(e)}")

    logger.info("System performance optimization completed.")