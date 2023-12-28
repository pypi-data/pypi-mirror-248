# -*- coding: utf-8 -*-
import datetime as dt
import os
from typing import Dict, Tuple
from datetime import date, timedelta

import win32com.client

PRE_MEETING_BUFFER_PREFIX = '[JS PRE-MEETING BUFFER] '
POST_MEETING_BUFFER_PREFIX = '[JS POST-MEETING BUFFER] '
SHADOW_MEETING_PREFIX = "[YOUR] shadow"

DAYS = 7

IGNORE_SUBJECT_PREFIX = "JS reserved:"

# creating the date object of today's date
todays_date = date.today()

PREFIX = "[YOUR] "


start_date = dt.datetime(todays_date.year, todays_date.month, todays_date.day)
end_date = start_date + timedelta(days=int(DAYS))
print(f"start date '{start_date}' end date '{end_date}'")
# sys.exit(1)
# end_date = dt.datetime(todays_date.year, todays_date.month, todays_date.day + 1)

print(
    f"Will retrieve calendar appointments between start date {start_date.strftime('%Y-%m-%d')} and end date {end_date.strftime('%Y-%m-%d')}"
)

matched_buffer_ctr = 0
unmatched_buffer_ctr = 0

Outlook = win32com.client.Dispatch("Outlook.Application")


def get_calendar(start_date, end_date):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    calendar = outlook.getDefaultFolder(9).Items
    calendar.IncludeRecurrences = True
    calendar.Sort("[Start]")
    restriction = (
        "[Start] >= '"
        + start_date.strftime("%m/%d/%Y")
        + "' AND [END] <= '"
        + end_date.strftime("%m/%d/%Y")
        + "'"
    )
    calendar = calendar.Restrict(restriction)
    print("Retrieved calendar")
    return calendar


def get_appointments(
    calendar,
) -> Tuple[
    Dict[Tuple[str, str], Dict[str, str]], Dict[Tuple[str, str], Dict[str, str]]
]:
    """Get the appointments from the calendar."""
    shadow_appointments_lookup = {}
    appointments_lookup = {}
    pre_meeting_buffer_appointments_lookup = {}
    post_meeting_buffer_appointments_lookup = {}

    ctr = 0
    for app in calendar:
        ctr += 1
        subject = app.subject
        if (
            subject == "ooo"
            or subject == "out-of-office"
            or subject.startswith(IGNORE_SUBJECT_PREFIX)
            or subject.startswith("PE - ")
        ):
            print(f"Will ignore appointment with subject '{subject}'")
            continue

        # organizer = app.organizer
        organizer = "TBD organizer"

        # body = app.body
        body = "TBD body"

        lookup = {
            "start": app.start,
            "end": app.end,
            "duration": app.duration,
            "organizer": organizer,
            "body": body,
            "appointment": app,
        }

        key = (subject, app.start)

        print(
            f"Found appointment '{ctr}' subject '{subject}' start '{app.start}' end '{app.end}' duration '{app.duration}' organizer '{organizer}'"
        )

        if subject.startswith("[YOUR] ") or subject.startswith("Canceled"):

            if key not in shadow_appointments_lookup:
                shadow_appointments_lookup[key] = {}
            shadow_appointments_lookup[key] = lookup

        elif subject.startswith(PRE_MEETING_BUFFER_PREFIX):

            if key not in pre_meeting_buffer_appointments_lookup:
                pre_meeting_buffer_appointments_lookup[key] = {}
            pre_meeting_buffer_appointments_lookup[key] = lookup

        elif subject.startswith(POST_MEETING_BUFFER_PREFIX):

            if key not in post_meeting_buffer_appointments_lookup:
                post_meeting_buffer_appointments_lookup[key] = {}
            post_meeting_buffer_appointments_lookup[key] = lookup

        else:

            if key not in appointments_lookup:
                appointments_lookup[key] = {}
            appointments_lookup[key] = lookup

    return (
        appointments_lookup,
        shadow_appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    )

def main():

    calendar = get_calendar(start_date, end_date)
    (
        appointments_lookup,
        shadow_appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    ) = get_appointments(calendar)



if __name__ == "__main__":
    main()
