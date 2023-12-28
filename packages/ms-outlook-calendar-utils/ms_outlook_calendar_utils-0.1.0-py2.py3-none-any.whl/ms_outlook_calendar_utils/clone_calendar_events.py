# -*- coding: utf-8 -*-
import datetime as dt
import os
import sys
import time
from distutils.util import strtobool
from typing import Dict, Tuple
from datetime import date, timedelta

import win32com.client
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SHADOW_MEETING_PREFIX = "[YOUR] shadow"

DEFAULT_DAYS = 7

DEFAULT_IGNORE_SUBJECT_PREFIX = "JS reserved:"

# If set to True, will create the shadow meeting appointments
# that correspond with some regular meeting appointment
DEFAULT_CREATE_SHADOW_MEETINGS = True

# If set to True, will delete the shadow meeting appointments
# that do not corresponding with any regular meeting appointment
DEFAULT_DELETE_SHADOW_MEETINGS = True

# If set to True, will create the pre-meeting buffer appointments
# that correspond with some regular meeting appointment
DEFAULT_CREATE_PRE_MEETING_BUFFERS = True

# If set to True, will delete the pre-meeting buffer appointments
# that do not corresponding with any regular meeting appointment
DEFAULT_DELETE_PRE_MEETING_BUFFERS = True

# If set to True, will create the post-meeting buffer appointments
# that correspond with some regular meeting appointment
DEFAULT_CREATE_POST_MEETING_BUFFERS = True

# If set to True, will delete the post-meeting buffer appointments
# that do not corresponding with any regular meeting appointment
DEFAULT_DELETE_POST_MEETING_BUFFERS = True

# creating the date object of today's date
todays_date = date.today()

IGNORE_SUBJECT_PREFIX = os.getenv("IGNORE_SUBJECT_PREFIX", None)
if IGNORE_SUBJECT_PREFIX is None:
    IGNORE_SUBJECT_PREFIX = DEFAULT_IGNORE_SUBJECT_PREFIX
    print(f"IGNORE_SUBJECT_PREFIX was not defined in the .env file so was set to default '{IGNORE_SUBJECT_PREFIX}'")

SHADOW_MEETING_PREFIX = os.getenv("SHADOW_MEETING_PREFIX", None)
if SHADOW_MEETING_PREFIX is None:
    SHADOW_MEETING_PREFIX = DEFAULT_SHADOW_MEETING_PREFIX
    print(f"SHADOW_MEETING_PREFIX was not defined in the .env file so was set to default '{SHADOW_MEETING_PREFIX}'")

PREFIX = os.getenv("PREFIX", None)
if PREFIX is None:
    raise Exception(
        "environment variable PREFIX was not defined - please set the environment variable or update the .env file)"
    )

PRE_MEETING_BUFFER_PREFIX = os.getenv("PRE_MEETING_BUFFER_PREFIX", None)
if PRE_MEETING_BUFFER_PREFIX is None:
    raise Exception(
        "environment variable PRE_MEETING_BUFFER_PREFIX was not defined - please set the environment variable or update the .env file)"
    )

PRE_MEETING_BUFFER_MINUTES = os.getenv("PRE_MEETING_BUFFER_MINUTES", None)
if PRE_MEETING_BUFFER_MINUTES is None:
    raise Exception(
        "environment variable PRE_MEETING_BUFFER_MINUTES was not defined - please set the environment variable or update the .env file)"
    )

PRE_MEETING_SUBJECT_SUFFIX = os.getenv("PRE_MEETING_SUBJECT_SUFFIX", None)
if PRE_MEETING_SUBJECT_SUFFIX is None:
    raise Exception(
        "environment variable PRE_MEETING_SUBJECT_SUFFIX was not defined - please set the environment variable or update the .env file)"
    )

POST_MEETING_BUFFER_PREFIX = os.getenv("POST_MEETING_BUFFER_PREFIX", None)
if POST_MEETING_BUFFER_PREFIX is None:
    raise Exception(
        "environment variable POST_MEETING_BUFFER_PREFIX was not defined - please set the environment variable or update the .env file)"
    )


POST_MEETING_BUFFER_MINUTES = os.getenv("POST_MEETING_BUFFER_MINUTES", None)
if POST_MEETING_BUFFER_MINUTES is None:
    raise Exception(
        "environment variable POST_MEETING_BUFFER_MINUTES was not defined - please set the environment variable or update the .env file)"
    )

POST_MEETING_SUBJECT_SUFFIX = os.getenv("POST_MEETING_SUBJECT_SUFFIX", None)
if POST_MEETING_SUBJECT_SUFFIX is None:
    raise Exception(
        "environment variable POST_MEETING_SUBJECT_SUFFIX was not defined - please set the environment variable or update the .env file)"
    )

RECIPIENT = os.getenv("RECIPIENT", None)
if RECIPIENT is None:
    raise Exception(
        "environment variable RECIPIENT was not defined - please set the environment variable or update the .env file)"
    )

SEND_INVITE_FOR_BUFFER_MEETINGS = bool(
    strtobool(os.getenv("SEND_INVITE_FOR_BUFFER_MEETINGS", False))
)
if SEND_INVITE_FOR_BUFFER_MEETINGS is None:
    raise Exception(
        "environment variable SEND_INVITE_FOR_BUFFER_MEETINGS was not defined - please set the environment variable or update the .env file)"
    )

CREATE_SHADOW_MEETINGS = bool(
    strtobool(os.getenv("CREATE_SHADOW_MEETINGS", False))
)
if CREATE_SHADOW_MEETINGS is None:
    CREATE_SHADOW_MEETINGS = DEFAULT_CREATE_SHADOW_MEETINGS
    print(f"CREATE_SHADOW_MEETINGS was not defined in the .env file and therefore was set to default '{CREATE_SHADOW_MEETINGS}'")

DELETE_SHADOW_MEETINGS = bool(
    strtobool(os.getenv("DELETE_SHADOW_MEETINGS", False))
)
if DELETE_SHADOW_MEETINGS is None:
    DELETE_SHADOW_MEETINGS = DEFAULT_DELETE_SHADOW_MEETINGS
    print(f"DELETE_SHADOW_MEETINGS was not defined in the .env file and therefore was set to default '{DELETE_SHADOW_MEETINGS}'")

CREATE_PRE_MEETING_BUFFERS = bool(
    strtobool(os.getenv("CREATE_PRE_MEETING_BUFFERS", False))
)
if CREATE_PRE_MEETING_BUFFERS is None:
    CREATE_PRE_MEETING_BUFFERS = DEFAULT_CREATE_PRE_MEETING_BUFFERS
    print(f"CREATE_PRE_MEETING_BUFFERS was not defined in the .env file and therefore was set to default '{CREATE_PRE_MEETING_BUFFERS}'")

DELETE_PRE_MEETING_BUFFERS = bool(
    strtobool(os.getenv("DELETE_PRE_MEETING_BUFFERS", False))
)
if DELETE_PRE_MEETING_BUFFERS is None:
    DELETE_PRE_MEETING_BUFFERS = DEFAULT_DELETE_PRE_MEETING_BUFFERS
    print(f"DELETE_PRE_MEETING_BUFFERS was not defined in the .env file and therefore was set to default '{DELETE_PRE_MEETING_BUFFERS}'")

CREATE_POST_MEETING_BUFFERS = bool(
    strtobool(os.getenv("CREATE_POST_MEETING_BUFFERS", False))
)
if CREATE_POST_MEETING_BUFFERS is None:
    CREATE_POST_MEETING_BUFFERS = DEFAULT_CREATE_POST_MEETING_BUFFERS
    print(f"CREATE_POST_MEETING_BUFFERS was not defined in the .env file and therefore was set to default '{CREATE_POST_MEETING_BUFFERS}'")

DELETE_POST_MEETING_BUFFERS = bool(
    strtobool(os.getenv("DELETE_POST_MEETING_BUFFERS", False))
)
if DELETE_POST_MEETING_BUFFERS is None:
    DELETE_POST_MEETING_BUFFERS = DEFAULT_DELETE_POST_MEETING_BUFFERS
    print(f"DELETE_POST_MEETING_BUFFERS was not defined in the .env file and therefore was set to default '{DELETE_POST_MEETING_BUFFERS}'")


DAYS = os.getenv("DAYS", None)
if DAYS is None:
    DAYS = DEFAULT_DAYS
    print(
        f"environment variable DAYS was not defined - and therefore was set to default '{DAYS}'"
    )

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
        start = app.start
        end = app.end
        duration = app.duration
        organizer = app.organizer
        body = app.body

        print(
            f"Found appointment '{ctr}' subject '{subject}' start '{start}' end '{end}' duration '{duration}' organizer '{organizer}'"
        )

        if subject.startswith("[YOUR] ") or subject.startswith("Canceled"):
            key = (subject, start)
            if key not in shadow_appointments_lookup:
                shadow_appointments_lookup[key] = {}
            shadow_appointments_lookup[key] = {
                "start": start,
                "end": end,
                "duration": duration,
                "appointment": app,
                "organizer": organizer,
                "body": body,
            }
        elif subject.startswith(PRE_MEETING_BUFFER_PREFIX):
            key = (subject, start)
            if key not in pre_meeting_buffer_appointments_lookup:
                pre_meeting_buffer_appointments_lookup[key] = {}
            pre_meeting_buffer_appointments_lookup[key] = {
                "start": start,
                "end": end,
                "duration": duration,
                "appointment": app,
                "organizer": organizer,
                "body": body,
            }
        elif subject.startswith(POST_MEETING_BUFFER_PREFIX):
            key = (subject, start)
            if key not in post_meeting_buffer_appointments_lookup:
                post_meeting_buffer_appointments_lookup[key] = {}
            post_meeting_buffer_appointments_lookup[key] = {
                "start": start,
                "end": end,
                "duration": duration,
                "appointment": app,
                "organizer": organizer,
                "body": body,
            }
        else:

            key = (subject, start)
            if key not in appointments_lookup:
                appointments_lookup[key] = {}
            appointments_lookup[key] = {
                "start": start,
                "end": end,
                "duration": duration,
                "organizer": organizer,
                "body": body,
            }

    return (
        appointments_lookup,
        shadow_appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    )


def adjust_appointments(
    appointments_lookup,
    shadow_appointments_lookup,
    pre_meeting_buffer_appointments_lookup,
    post_meeting_buffer_appointments_lookup,
) -> None:

    if CREATE_SHADOW_MEETINGS:
        create_shadow_appointments(appointments_lookup, shadow_appointments_lookup)
    else:
        print(f"Will not attempt to create any shadow meetings")
    if DELETE_SHADOW_MEETINGS:
        remove_shadow_appointments(appointments_lookup, shadow_appointments_lookup)
    else:
        print(f"Will not attempt to delete any shadow meetings")

    create_buffer_appointments(
        appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    )
    remove_buffer_appointments(
        appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    )


def create_shadow_appointments(appointments_lookup, shadow_appointments_lookup) -> None:
    print(
        f"Will attempt to create the shadow appointments i.e.: with prefix '{PREFIX}'"
    )

    matched_ctr = 0
    unmatched_ctr = 0
    for app_tuple_key in appointments_lookup:
        app_subject = app_tuple_key[0]
        app_start = app_tuple_key[1]

        shadow_subject = PREFIX + app_subject
        shadow_tuple_key = (shadow_subject, app_start)

        if shadow_tuple_key in shadow_appointments_lookup:
            matched_ctr += 1
            print(
                f"Shadow appointment already exists with subject '{shadow_subject}' start date '{app_start}'"
            )
        else:
            unmatched_ctr += 1
            appointment = appointments_lookup[app_tuple_key]
            duration = appointment.get("duration", None)
            if duration is None:
                raise Exception(
                    f"duration was not define for appointment with subject '{app_subject}, start date '{app_start}'"
                )
            add_event(
                app_start, shadow_subject, duration, appointment.get("organizer", None)
            )


def remove_shadow_appointments(appointments_lookup, shadow_appointments_lookup) -> None:
    print(
        f"Will attempt to remove the shadow appointments i.e.: with prefix '{PREFIX}'"
    )

    for shadow_app_tuple_key in shadow_appointments_lookup:
        shadow_app_subject = shadow_app_tuple_key[0]
        shadow_app_start = shadow_app_tuple_key[1]

        if shadow_app_subject.startswith(PREFIX) or shadow_app_subject.startswith(
            "Canceled"
        ):
            print(f"Qualified shadow appointment has subject '{shadow_app_subject}'")
        else:
            raise Exception(
                f"Encountered a shadow appointment with subject that does not start with the prefix '{PREFIX}' nor 'Canceled': '{shadow_app_subject}' with start date '{shadow_app_start}'"
            )

        app_subject = shadow_app_subject.replace(PREFIX, "")
        app_tuple_key = (app_subject, shadow_app_start)

        if app_tuple_key not in appointments_lookup:
            app = shadow_appointments_lookup[shadow_app_tuple_key]
            appointment = app.get("appointment", None)
            if appointment is None:
                raise Exception(
                    f"appointment was not defined for subject '{shadow_app_subject}' start date '{shadow_app_start}'"
                )
            print(
                f"Will attempt to delete shadow appointment with subject '{shadow_app_subject}' start date '{shadow_app_start}'"
            )
            appointment.Delete()


def create_buffer_appointments(
    appointments_lookup,
    pre_meeting_buffer_appointments_lookup,
    post_meeting_buffer_appointments_lookup,
) -> None:
    print(
        f"Will attempt to create the pre-meeting buffer appointments with prefix '{PRE_MEETING_BUFFER_PREFIX}' and post-meeting buffer appointments with prefix '{POST_MEETING_BUFFER_PREFIX}'"
    )

    for app_tuple_key in appointments_lookup:
        app_subject = app_tuple_key[0]
        app_start = app_tuple_key[1]
        # bstart = app_start - timedelta(hours=0, minutes=int(PRE_MEETING_BUFFER_MINUTES))
        # print(f"{app_subject=} {app_start=} {bstart=}")
        # sys.exit(1)

        appointment = appointments_lookup[app_tuple_key]
        duration = appointment.get("duration", None)
        if duration is None:
            raise Exception(
                f"duration was not define for appointment with subject '{app_subject}, start date '{app_start}'"
            )

        if CREATE_PRE_MEETING_BUFFERS:
            create_pre_meeting_buffer_appointment(
                pre_meeting_buffer_appointments_lookup,
                app_subject,
                app_start,
                appointment.get("organizer", None),
            )
        else:
            print(f"Will not attempt to create pre-meeting buffer meetings")

        if CREATE_POST_MEETING_BUFFERS:
            create_post_meeting_buffer_appointment(
                post_meeting_buffer_appointments_lookup,
                app_subject,
                app_start,
                duration,
                appointment.get("organizer", None),
            )
        else:
            print(f"Will not attempt to create post-meeting buffer meetings")


def create_pre_meeting_buffer_appointment(
    pre_meeting_buffer_appointments_lookup,
    app_subject,
    app_start,
    organizer: str = None,
) -> None:

    global unmatched_buffer_ctr
    global matched_buffer_ctr

    pre_meeting_buffer_subject = (
        f"{PRE_MEETING_BUFFER_PREFIX}{app_subject}{PRE_MEETING_SUBJECT_SUFFIX}"
    )

    pre_meeting_buffer_start_time = app_start - timedelta(
        hours=0, minutes=int(PRE_MEETING_BUFFER_MINUTES)
    )

    pre_meeting_buffer_tuple_key = (
        pre_meeting_buffer_subject,
        pre_meeting_buffer_start_time,
    )

    if pre_meeting_buffer_tuple_key in pre_meeting_buffer_appointments_lookup:
        matched_buffer_ctr += 1
        print(
            f"pre-meeting buffer appointment already exists with subject '{pre_meeting_buffer_subject}' start time '{pre_meeting_buffer_start_time}'"
        )
    else:
        unmatched_buffer_ctr += 1
        print(
            f"Will attempt to create a pre-meeting buffer appointment with pre-meeting buffer start time '{pre_meeting_buffer_start_time} for appointment with subject '{app_subject}' and start time '{app_start}'"
        )
        add_event(
            pre_meeting_buffer_start_time,
            pre_meeting_buffer_subject,
            PRE_MEETING_BUFFER_MINUTES,  # duration of the pre-meeting buffer appointment
            organizer,
        )


def create_post_meeting_buffer_appointment(
    post_meeting_buffer_appointments_lookup,
    app_subject,
    app_start,
    duration,
    organizer: str = None,
) -> None:

    global unmatched_buffer_ctr
    global matched_buffer_ctr

    post_meeting_buffer_subject = (
        f"{POST_MEETING_BUFFER_PREFIX}{app_subject}{POST_MEETING_SUBJECT_SUFFIX}"
    )

    post_meeting_buffer_start_time = app_start + timedelta(
        hours=0, minutes=int(duration)
    )  #  + timedelta(hours=0, minutes=int(POST_MEETING_BUFFER_MINUTES))

    post_meeting_buffer_tuple_key = (
        post_meeting_buffer_subject,
        post_meeting_buffer_start_time,
    )

    if post_meeting_buffer_tuple_key in post_meeting_buffer_appointments_lookup:
        matched_buffer_ctr += 1
        print(
            f"post-meeting buffer appointment already exists with subject '{post_meeting_buffer_subject}' start date '{post_meeting_buffer_start_time}'"
        )
    else:
        unmatched_buffer_ctr += 1

        print(
            f"Will attempt to create a post-meeting buffer appointment with post-meeting buffer start time '{post_meeting_buffer_start_time} for appointment with subject '{app_subject}' and start time '{app_start}'"
        )

        body = f"duration: {duration}"
        add_event(
            post_meeting_buffer_start_time,
            post_meeting_buffer_subject,
            POST_MEETING_BUFFER_MINUTES,  # duration of the post-meeting buffer appointment
            organizer,
            body=body,
        )


def remove_buffer_appointments(
    appointments_lookup,
    pre_meeting_buffer_appointments_lookup,
    post_meeting_buffer_appointments_lookup,
) -> None:

    # If the pre-meeting buffer appointment has a corresponding regular appointment which starts at the time
    # that the pre-meeting buffer appointment ends and the subjects are similar, then delete the pre-meeting buffer
    # appointment and corresponding post-meeting buffer appointment.
    if DELETE_PRE_MEETING_BUFFERS:
        print(
            f"Will attempt to remove the pre-meeting buffer appointments i.e.: with prefix '{PRE_MEETING_BUFFER_PREFIX}'"
        )

        remove_pre_meeting_buffer_appointments(
            appointments_lookup, pre_meeting_buffer_appointments_lookup
        )
    else:
        print(f"Will not attempt to delete pre-meeting buffer meetings")

    if DELETE_POST_MEETING_BUFFERS:
        print(
            f"Will attempt to remove the post-meeting buffer appointments i.e.: with prefix '{POST_MEETING_BUFFER_PREFIX}'"
        )
        remove_post_meeting_buffer_appointments(
            appointments_lookup, post_meeting_buffer_appointments_lookup
        )
    else:
        print(f"Will not attempt to delete post-meeting buffer meetings")


def remove_pre_meeting_buffer_appointments(
    appointments_lookup, pre_meeting_buffer_appointments_lookup
) -> None:

    for buffer_app_tuple_key in pre_meeting_buffer_appointments_lookup:
        buffer_app_subject = buffer_app_tuple_key[0]
        buffer_app_start = buffer_app_tuple_key[1]

        if buffer_app_subject.startswith(
            PRE_MEETING_BUFFER_PREFIX
        ) or buffer_app_subject.startswith("Canceled"):
            print(
                f"Will consider whether to delete pre-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )
        else:
            raise Exception(
                f"Encountered a pre-meeting buffer appointment with subject that does not start with the prefix '{PRE_MEETING_BUFFER_PREFIX}' nor 'Canceled': with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )

        # To derive the original regular appointment subject, remove the prefix and suffix
        # from the pre-meeting buffer subject
        app_subject = buffer_app_subject.replace(PRE_MEETING_BUFFER_PREFIX, "").replace(
            PRE_MEETING_SUBJECT_SUFFIX, ""
        )

        print(
            f">> {buffer_app_subject=} {app_subject=} {PRE_MEETING_BUFFER_PREFIX=} {PRE_MEETING_SUBJECT_SUFFIX=}"
        )
        # The regular appointment start time shoudl be the time the pre-meeting buffer appointment
        # ends
        app_start_time = buffer_app_start + timedelta(
            hours=0, minutes=int(PRE_MEETING_BUFFER_MINUTES)
        )

        app_tuple_key = (app_subject, app_start_time)

        if app_tuple_key not in appointments_lookup:
            print(
                f"Did not find a regular appointment with subject '{app_subject}' start time '{app_start_time}' in the appointments lookup while processing pre-meeting buffer appointment with subject '{buffer_app_subject}' and start time '{buffer_app_start}'"
            )

            app = pre_meeting_buffer_appointments_lookup[buffer_app_tuple_key]
            print(f"buffer appointment: {app}")

            appointment = app.get("appointment", None)
            if appointment is None:
                raise Exception(
                    f"appointment was not defined for regular meeting with subject '{app_subject}' and start date '{app_start_time}' while processing pre-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
                )
            print(
                f"Will attempt to delete pre-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )
            appointment.Delete()
        else:
            print(
                f"Found regular appointment with subject '{app_subject}' start time '{app_start_time}' in the appointments lookup - so will not attempt remove this pre-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )


def remove_post_meeting_buffer_appointments(
    appointments_lookup, post_meeting_buffer_appointments_lookup
) -> None:

    for buffer_app_tuple_key in post_meeting_buffer_appointments_lookup:
        buffer_app_subject = buffer_app_tuple_key[0]
        buffer_app_start = buffer_app_tuple_key[1]

        if buffer_app_subject.startswith(
            POST_MEETING_BUFFER_PREFIX
        ) or buffer_app_subject.startswith("Canceled"):
            print(
                f"Will consider whether to delete post-meeting buffer appointment with subject '{buffer_app_subject}' and start time '{buffer_app_start}'"
            )
        else:
            raise Exception(
                f"Encountered a post-meeting buffer appointment with subject that does not start with the prefix '{POST_MEETING_BUFFER_PREFIX}' nor 'Canceled' - having subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )

        # To derive the original regular appointment subject, remove the prefix and suffix
        # from the pre-meeting buffer subject
        app_subject = buffer_app_subject.replace(
            POST_MEETING_BUFFER_PREFIX, ""
        ).replace(POST_MEETING_SUBJECT_SUFFIX, "")

        reg_meeting_duration = get_regular_meeting_duration(
            post_meeting_buffer_appointments_lookup[buffer_app_tuple_key]
        )
        app_start_time = buffer_app_start - timedelta(
            hours=0, minutes=int(reg_meeting_duration)
        )

        app_tuple_key = (app_subject, app_start_time)

        if app_tuple_key not in appointments_lookup:

            app = post_meeting_buffer_appointments_lookup[buffer_app_tuple_key]
            appointment = app.get("appointment", None)
            if appointment is None:
                raise Exception(
                    f"appointment was not defined for regular appointment with subject '{app_subject}' and start time '{app_start_time}' while processing post-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
                )
            print(
                f"Will attempt to delete post-meeting buffer appointment with subject '{buffer_app_subject}' and start date '{buffer_app_start}'"
            )
            appointment.Delete()
        else:
            print(
                f"Found regular appointment with subject '{app_subject}' and start time '{app_start_time}' in the appointments lookup - so will not attempt remove this post-meeting buffer appointment with subject '{buffer_app_subject}' start date '{buffer_app_start}'"
            )


def get_regular_meeting_duration(post_meeting_buffer_appointment):
    """Derive the corresponding regular appointment's start time."""
    if "body" in post_meeting_buffer_appointment:
        body = post_meeting_buffer_appointment["body"]
        for line in body.split("\n"):
            if line.lower().startswith("duration: "):
                return line.lower().lstrip("duration: ")
        raise Exception(
            f"Could not derive the duration for the post-meeting buffer appointment"
        )
    else:
        raise Exception(
            f"post-meeting buffer appointment does not have a body: {post_meeting_buffer_appointment}"
        )


def add_event(start, subject, duration, organizer, body: str = None):

    appointment = Outlook.CreateItem(1)  # 1=outlook appointment item
    appointment.Start = start
    appointment.Subject = subject
    appointment.Duration = duration
    appointment.Categories = SHADOW_MEETING_PREFIX
    appointment.ReminderSet = False
    if organizer is not None:
        appointment.Body = f"The organizer is '{organizer}'.\n{body}"
    appointment.MeetingStatus = 1

    if PRE_MEETING_BUFFER_PREFIX in subject or POST_MEETING_BUFFER_PREFIX in subject:
        if SEND_INVITE_FOR_BUFFER_MEETINGS:
            appointment.Recipients.Add(RECIPIENT)
            print(f"Will send meeting invite for meeting with subject '{subject}'")
        else:
            print(f"Will not send meeting invite for meeting with subject '{subject}'")
    else:
        appointment.Recipients.Add(RECIPIENT)
        print(f"Will send meeting invite for meeting with subject '{subject}'")

    appointment.Save()
    appointment.Send()


def main():

    calendar = get_calendar(start_date, end_date)
    (
        appointments_lookup,
        shadow_appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    ) = get_appointments(calendar)

    adjust_appointments(
        appointments_lookup,
        shadow_appointments_lookup,
        pre_meeting_buffer_appointments_lookup,
        post_meeting_buffer_appointments_lookup,
    )


if __name__ == "__main__":
    main()
