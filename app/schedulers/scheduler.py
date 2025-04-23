from app.services.data_service import refresh_all_data
import logging

logger = logging.getLogger(__name__)

def schedule_jobs(scheduler):
    """
    Add jobs to the scheduler.
    This is called by the Flask-APScheduler during initialization.
    """
    # Jobs are defined in the config.py JOBS dictionary
    logger.info("Jobs scheduled as per configuration")

def refresh_data_job():
    """
    Job function to refresh all data.
    This is called by the scheduler as defined in config.py.
    """
    logger.info("Scheduled job: Refreshing all data")
    result = refresh_all_data()
    if result:
        logger.info("Successfully refreshed all data")
    else:
        logger.warning("Error refreshing some data")
    return result
