import datetime
import requests
import icalendar
import uuid
from hashlib import sha256
from os import environ
from flask import Flask, Response

"""
Dependencies
-icalendar
-requests
-flask

"""

app = Flask(__name__)

application_id = "loblaw-scheduler.lfcode.ca"


def get_schedule(punchin_id: int):
    """
    Get the raw schedule json from an employee
    """
    punchin_id = int(punchin_id)
    if not 0 < punchin_id < (10**7-1):
        raise ValueError("Value is out of range")

    resp = requests.get(f'https://stas.loblaw.ca/lcl-employeeschedule-services/api/rest/v1/services/en/employeeschedules/{punchin_id}')
    return resp.json()


class Shift:
    def __init__(self, start: datetime.datetime, end: datetime.datetime, hours: float, position: str, store: str, badge: int):
        self.start = start
        self.end = end
        self.hours = hours
        self.position = position
        self.store = store
        self.badge = badge

    @classmethod
    def from_api(cls, resp: dict, badge: int):
        """
        Parses a single shift dict into a shift object
        """
        month, day, year = (int(x) for x in resp['date'].split('/'))
        date = datetime.date(year, month, day)
        start_time = datetime.time(*(int(x) for x in resp['startTime'].split(':')))
        end_time = datetime.time(*(int(x) for x in resp['endTime'].split(':')))
        start = datetime.datetime.combine(date, start_time)
        end = datetime.datetime.combine(date, end_time)

        return cls(
            start,
            end,
            resp['netHours'],
            resp['position'],
            resp['storeNumber'],
            badge
        )

    def to_str(self):
        return ":".join([str(self.badge), self.store, self.position, str(self.start.timestamp()), str(self.end.timestamp())])

    def uid(self):
        return sha256(self.to_str().encode()).hexdigest()

    def __repr__(self):
        return '{s.__class__.__name__}(start={s.start!r}, end={s.end!r}, ' \
           'hours={s.hours}, position={s.position!r}, ' \
           'store={s.store!r})'.format(s=self)


def make_calendar(shifts):
    """
    Creates a Calendar object from a list of Shift objects
    """
    cal = icalendar.Calendar()
    cal.add('prodid', '-//Loblaw Calendar Maker//lfcode.ca//')
    cal.add('version', '2.0')
    for shift in shifts:
        event = icalendar.Event()
        event.add('summary', "Go to work")
        event.add('description', f'{shift.position} for {shift.hours} hours')
        event.add('dtstart', shift.start)
        event.add('dtend', shift.end)
        event.add('dtstamp', datetime.datetime.now())
        event.add('uid', shift.uid() + "@" + application_id)
        cal.add_component(event)
    return cal


def extract_shifts(timetable):
    """
    Turns a raw schedule query into a list of individual shifts
    """
    return unnest_lists([weeks["shifts"] for weeks in timetable["weeks"] if len(weeks["shifts"])])


def unnest_lists(lists):
    """
    [[0,1], [2]] -> [0,1,2]
    """
    return [entrie for sublist in lists for entrie in sublist]


def build_calendar(punch_id):
    """
    Populates a Calendar object with shifts
    """
    shifts = [Shift.from_api(shift, punch_id) for shift in extract_shifts(get_schedule(punch_id))]
    return make_calendar(shifts)


@app.route('/badge/<int:punch_id>')
def show_ical(punch_id):
    return Response(build_calendar(punch_id).to_ical(), mimetype='text/calendar')
