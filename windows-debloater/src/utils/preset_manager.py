import logging
from utils.bloatware_removal import remove_selected_bloatware
from utils.onedrive_disabler import disable_onedrive
from utils.performance_optimizer import optimize_performance

# Get the logger
logger = logging.getLogger("DebloaterLogger")

def run_minimal_preset(bloatware_list):
    """
    Run the minimal preset which only removes the most unnecessary bloatware.
    
    Args:
        bloatware_list (list): List of app package names to remove
    """
    logger.info("Starting Minimal Preset cleanup")
    
    try:
        # Remove selected minimal bloatware
        remove_selected_bloatware(bloatware_list)
        logger.info("Minimal Preset completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error during Minimal Preset: {str(e)}")
        return False

def run_full_clean_preset(bloatware_list):
    """
    Run the full clean preset which:
    1. Removes all bloatware
    2. Disables OneDrive
    3. Optimizes system performance
    
    Args:
        bloatware_list (list): List of all app package names to remove
    """
    logger.info("Starting Full System Clean preset")
    
    try:
        # Step 1: Remove all bloatware
        logger.info("Full Clean - Step 1: Removing all bloatware apps")
        remove_selected_bloatware(bloatware_list)
        
        # Step 2: Disable OneDrive
        logger.info("Full Clean - Step 2: Disabling OneDrive")
        disable_onedrive()
        
        # Step 3: Optimize performance
        logger.info("Full Clean - Step 3: Optimizing system performance")
        optimize_performance()
        
        logger.info("Full System Clean preset completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error during Full System Clean preset: {str(e)}")
        return False