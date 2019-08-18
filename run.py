"""
Bot for doing time calculations around the world
"""

import os
import re
import string
import datetime

import pytz
import dateutil.parser
from mmpy_bot.bot import Bot, respond_to


IGNORE_NOTIFIES = ['@channel', '@all']
LOCAL_TIMEZONE = os.getenv('LOCAL_TIMEZONE', 'Australia/Sydney')
local_tz = pytz.timezone(LOCAL_TIMEZONE)

default_date_format = '%Y-%m-%d %H:%M:%S %Z%z'

timezone_map = {
    'washington': 'America/New_York',
    'washington dc': 'America/New_York',
    'london': 'Europe/London',
    'paris': 'Europe/Paris',
}

# Use this table to remove punctuation from location names
punctuation_table = str.maketrans(dict.fromkeys(string.punctuation))


@respond_to("^(what'?s the )?time in (.*)", re.IGNORECASE)
def get_time_in(message, _, location):
    # Remove any punctuation from the location name
    location = location.translate(punctuation_table)
    location_lower = location.lower().translate(punctuation_table)
    try:
        timezone_name = timezone_map[location_lower]
    except KeyError:
        message.reply("Sorry, I don't know the timezone for '{}'".format(location))
        return

    remote_timezone = pytz.timezone(timezone_name)
    now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)

    remote_time = now.astimezone(remote_timezone)

    message.reply('Time in {} is {}'.format(location, remote_time.strftime(default_date_format)))


@respond_to('get the time in (.*?) ((in|on|next) .*)', re.IGNORECASE)
def get_relative_time(message, location, date_string, _):
    message.reply('Getting the time in {} {}'.format(location, date_string))

    # Remove any punctuation from the location name
    location = location.translate(punctuation_table)
    location_lower = location.lower()

    try:
        timezone_name = timezone_map[location_lower]
    except KeyError:
        message.reply("Sorry, I don't know the timezone for '{}'".format(location))
        return

    remote_timezone = pytz.timezone(timezone_name)

    # Attempt to parse the user provided string
    # Remove the word next as it doesn't work for some reason
    date_string = date_string.replace('next ', '')
    try:
        relative_time = dateutil.parser.parse(date_string)
    except ValueError:
        message.reply("Sorry, I don't know when '{}' is".format(date_string))
        return

    relative_time = local_tz.localize(relative_time)

    remote_time = relative_time.astimezone(remote_timezone)

    message.reply('Time in {} {} is {}'.format(location, date_string, remote_time.strftime(default_date_format)))


if __name__ == "__main__":
    Bot().run()
