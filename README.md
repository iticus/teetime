# teetime

## About
This application uses selenium to book tee times.

## Install

Needed libraries (tested on `Amazon Ubuntu` and `Python 3`)

  - firefox (`aptitude install firefox`)
  - xvfb (`aptitude install xvfb`)
  - pyvirtualdisplay (`pip3 install pyvirtualdisplay`)
  - selenium (`pip3 install selenuium`)

## Run
The application is meant to be run using crontab but you can run it using `python3 teetime.py` as well
Pay attention to the timezone setting; on Ubuntu you can configure it using  `dpkg-reconfigure tzdata`.

## Settings
The most important settings (see `settings.py`) are:

 - an account on the desired page
 - the day to book and the time interval
 - the number of players

## Schedule

By default the application tries to create a booking for max two weeks from now, if you want to change this behavior change the `days_to_dates` function in `utils.py`:
```
...today+datetime.timedelta(days=14)
...today = today + datetime.timedelta(days=7)
```
