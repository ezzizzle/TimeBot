# TimeBot: Mattermost Bot to work with Times

Allows you to ask the bot for the time in other locations.

Uses the [dateutil.parser](https://github.com/dateutil/dateutil) class to parse human language time offsets.

# Usage

Uses the [mmpy_bot](https://github.com/attzonko/mmpy_bot) package for connecting to Mattermost. Configure the connection using the details [here](https://github.com/attzonko/mmpy_bot#configuration).

Specify your local timezone using the environment variable `LOCAL_TIMEZONE`. Timezone should be in the [IANA standard](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).

```bash
export LOCAL_TIMEZONE=Australia/Sydney
python run.py
```

You can ask TimeBot what the current time is in a particular location.

```
@timebot what's time in London?

@sender Time in London is 2019-08-18 12:11:28 BST+0100
```

You can ask TimeBot for the time in a particular location relative to local time.

```
@timebot get the time in London next Monday at 1pm

@sender Time in London Monday at 1pm is 2019-08-19 04:00:00 BST+0100
```

# ToDo

* Move `timezone_map` to a separate file so more locations can be added
