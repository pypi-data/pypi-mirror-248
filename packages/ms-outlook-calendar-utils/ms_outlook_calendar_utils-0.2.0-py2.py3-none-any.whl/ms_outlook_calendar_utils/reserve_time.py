# -*- coding: utf-8 -*-
import datetime as dt
import os
import sys

# import time
from datetime import date, datetime, timedelta
from distutils.util import strtobool
from typing import Dict, Tuple

import win32com.client
from dotenv import load_dotenv
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich import print as rprint
from rich.prompt import Prompt

load_dotenv()

# The question number
qnum = 0

issue_url = "https://jira.regeneron.com/browse"

event_categories = [
    "Data Processing",
    "DNAnexus-to-Redshift Data Transfer",
    "Flinders matrix generation",
    "IMS",
    "OMOP Matrix Generation R-scripts",
    "ooo",
    "PB ETL",
]

DEFAULT_RESERVE_TIME_TITLE_PREFIX = "JS reserved: "
DEFAULT_MEETING_CATEGORY = "JS reserved"
DEFAULT_SET_REMINDER = False
DEFAULT_ORGANIZER = "Jay Sundaram"
DEFAULT_UTC_HOURS = 5

# creating the date object of today's date
todays_date = date.today()

Outlook = win32com.client.Dispatch("Outlook.Application")


def prompt_user(msg: str) -> str:
    global qnum
    qnum += 1
    return Prompt.ask(f"\n[bold blue]Q{qnum}.[/] {msg}")


def get_start_date_time(start_hour: int, start_min: int):
    """This will derive the datetime.datime for the specified start time

    Args:
        start_hour (int): the hour the event should start
        start_min (int): the minute the event should start
    """
    # todays_date = date.today()
    # print(f"{todays_date=}")
    # start_date = dt.datetime(todays_date.year, todays_date.month, todays_date.day)
    # print(f"{start_date=}")
    start_date_time = dt.datetime(
        todays_date.year,
        todays_date.month,
        todays_date.day,
        start_hour,
        start_min,
    )

    # print(f"{start_date_time=}")
    return start_date_time


def get_start_time() -> Tuple[int, int]:
    """Get the start hour and start minute.

    This will present a proposed start time and then
    will allow the user to either acccept that proposed
    start time or else enter the desired start hour and start
    minute."""
    global qnum
    qnum += 1
    start_hour, start_min = get_proposed_start_time()
    ans = None
    start_hour_str = str(start_hour)
    start_min_str = str(start_min)
    if start_min_str == "0":
        start_min_str = "00"
    while ans is None:
        ans = prompt_user(
            f"Is this start time correct: {start_hour_str}:{start_min_str}? [Y/n]"
        )
        ans = ans.strip().lower()
        if ans == "":
            ans = "y"
        if not ans.startswith("y"):
            start_hour = int(get_start_hour()) - DEFAULT_UTC_HOURS
            start_min = int(get_start_minutes())
            break
        else:
            start_hour -= DEFAULT_UTC_HOURS
            break
    return start_hour, start_min


def get_proposed_start_time() -> Tuple[int, int]:
    """Derive a start time.

    This will select the current our and nearest 30 minute increment."""

    now = datetime.now()

    current_hour = int(now.strftime("%H"))
    current_min = int(now.strftime("%M"))

    start_hour = current_hour
    start_min = None

    if current_min < 15:
        start_min = 00
    elif current_min >= 15 and current_min < 30:
        start_min = 30
    elif current_min >= 30 and current_min < 45:
        start_min = 30
    elif current_min >= 45 and current_min <= 59:
        start_min = 00
        start_hour += 1
    return start_hour, start_min


def add_event(
    start_date_time,
    subject: str = None,
    meeting_category: str = None,
    duration: int = None,
    organizer: str = DEFAULT_ORGANIZER,
    body: str = None,
    set_reminder: bool = DEFAULT_SET_REMINDER,
) -> None:
    """Add an event to the Outlook Calendar."""
    appointment = Outlook.CreateItem(1)  # 1=outlook appointment item
    appointment.Start = start_date_time
    appointment.Subject = subject
    appointment.Duration = duration
    appointment.Categories = meeting_category
    appointment.ReminderSet = set_reminder
    if organizer is not None:
        appointment.Body = f"The organizer is '{organizer}'.\n{body}"
    appointment.MeetingStatus = 1

    appointment.Save()
    rprint(f"\n[green]Appointment with subject '{subject}' has been created[/]")


def get_start_hour() -> str:
    """Prompt the user for the start hour"""
    global qnum
    qnum += 1

    start_hour = None
    while start_hour is None or start_hour == "":
        start_hour = prompt_user("What is the start time (using 24 hour clock)?")
    return start_hour


def get_start_minutes() -> str:
    """Prompt the user for the start minute."""
    global qnum
    qnum += 1

    start_minutes = None
    while start_minutes is None or start_minutes == "":
        start_minutes = prompt_user("What is the start minutes?")
    return start_minutes


def get_duration() -> str:
    """Prompt the user for the duration of the event."""
    global qnum
    qnum += 1

    duration = None
    while duration is None or duration == "":
        duration = prompt_user("What is the duration in minutes [30]?")
        if duration == "":
            duration = 30
    return duration


def get_organizer() -> str:
    """Prompt the user for the organizer of the event."""
    organizer = None
    while organizer is None or organizer == "":
        organizer = prompt_user(f"Who is the organizer [{DEFAULT_ORGANIZER}]?")
        if organizer == "":
            organizer = DEFAULT_ORGANIZER
    return organizer.strip()


def get_event_category() -> str:
    """Prompt the user for the event category."""
    global qnum
    qnum += 1

    rprint(f"\n[bold blue]Q{qnum}.[/] Select event category\n")

    for category in event_categories:
        print(f"{category}")

    completer = WordCompleter(event_categories)
    category = prompt(
        "\nWhich category? [just start typing for autocompletion] ",
        completer=completer,
        mouse_support=True,
    )
    if category is None or category == "":
        return "TBD"
    return category


def get_event_title() -> str:
    """Prompt the user for the event title."""
    event_title = None
    while event_title is None or event_title == "":
        # event_title = input("\n[blue]Q1.[/]What is the event title? ")
        event_title = prompt_user("What is the event title?")

    return event_title


def get_issue_id() -> str:
    """Prompt the user for the issue id."""
    issue_id = None
    issue_id = prompt_user("Is there an issue tracking id? [N/issue id]")
    issue_id = issue_id.strip().lower()
    if issue_id is None or issue_id == "" or issue_id.startswith("n"):
        return None
    return issue_id.upper()


def main():

    event_title = get_event_title()
    category = get_event_category()
    start_hour, start_min = get_start_time()
    duration = int(get_duration())
    issue_id = get_issue_id()
    start_date_time = get_start_date_time(start_hour, start_min)
    body = "Reserved time for focussed work"
    subject = f"{DEFAULT_RESERVE_TIME_TITLE_PREFIX}{event_title}"

    if issue_id is not None:
        body += f"\n{issue_url}/{issue_id}"
        subject += f" {issue_id}"

    add_event(
        start_date_time,
        subject=subject,
        meeting_category=category,
        duration=duration,
        body=body,
    )


if __name__ == "__main__":
    main()
