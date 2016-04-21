import datetime
from dateutil.parser import parse
import pytz

import app_config

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
Tools for managing charts
"""
class TimeTools:
    @staticmethod
    def seconds_since(a):
        now = datetime.datetime.now(pytz.timezone(app_config.PROJECT_TIMEZONE))
        return (now - a).total_seconds()

    @staticmethod
    def time_bucket(t):
        if not t:
            return False

        # For some reason, dates with timezones tend to be returned as unicode
        if type(t) is not datetime.datetime:
            t = parse(t)

        seconds = TimeTools.seconds_since(t)

        # 7th message, 2nd day midnight + 10 hours
        # 8th message, 2nd day midnight + 15 hours
        second_day_midnight_after_publishing = t + datetime.timedelta(days=2)
        second_day_midnight_after_publishing.replace(hour = 0, minute = 0, second=0, microsecond = 0)
        seconds_since_second_day = TimeTools.seconds_since(second_day_midnight_after_publishing)

        if seconds_since_second_day > 15 * 60 * 60: # 15 hours
            return 'day 2 hour 15'

        if seconds_since_second_day > 10 * 60 * 60: # 10 hours
            return 'day 2 hour 10'

        # 5th message, 1st day midnight + 10 hours
        # 6th message, 1st day midnight + 15 hours
        midnight_after_publishing = t + datetime.timedelta(days=1)
        midnight_after_publishing.replace(hour = 0, minute = 0, second=0, microsecond = 0)
        seconds_since_first_day = TimeTools.seconds_since(midnight_after_publishing)

        if seconds_since_second_day > 10 * 60 * 60: # 15 hours
            return 'day 1 hour 15'

        if seconds_since_second_day > 10 * 60 * 60: # 10 hours
            return 'day 1 hour 10'

        # 2nd message, tracking start + 4 hours
        # 3rd message, tracking start + 8 hours
        # 4th message, tracking start + 12 hours
        if seconds > 12 * 60 * 60: # 12 hours
            return 'hour 12'

        if seconds > 8 * 60 * 60: # 8 hours
            return 'hour 8'

        if seconds > 4 * 60 * 60: # 4 hours
            return 'hour 4'

        # Too soon to check
        return False

    @staticmethod
    def humanist_time_bucket(linger):
        time = ''
        if linger['minutes'] > 0:
            time += str(linger['minutes'])
            if linger['minutes'] == 1:
                time += ' minute'
            else:
                time += ' minutes'

        if linger['seconds'] > 0:
            if linger['minutes'] > 0:
                time += ' '

            time += str(linger['seconds'])
            if linger['seconds'] == 1:
                time += ' second'
            else:
                time += ' seconds'

        return time
