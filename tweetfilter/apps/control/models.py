# -*- coding: utf-8 -*-
from time import strptime
import datetime
from django.db import models


class Schedule(models.Model):
    time = models.TimeField()

    # Appliable weekdays
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def days_of_week_list(self):
        """
        Returns a list of ordered integers representing the weekdays marked as True
        """
        res = []
        if self.monday:
            res.append(0)
        if self.tuesday:
            res.append(1)
        if self.wednesday:
            res.append(2)
        if self.thursday:
            res.append(3)
        if self.friday:
            res.append(4)
        if self.saturday:
            res.append(5)
        if self.sunday:
            res.append(6)

        return res

    def days_of_week_word_list(self):
        """
        Returns a list of ordered integers representing the weekdays marked as True
        """
        res = []
        if self.monday:
            res.append("mon")
        if self.tuesday:
            res.append("tue")
        if self.wednesday:
            res.append("wed")
        if self.thursday:
            res.append("thu")
        if self.friday:
            res.append("fri")
        if self.saturday:
            res.append("sat")
        if self.sunday:
            res.append("sun")

        return res

    def days_of_week_string(self):
        return ','.join(self.days_of_week_word_list())


class ScheduleBlock(models.Model):
    start = models.TimeField()  # start time of the day
    end = models.TimeField()    # end time of the day

    # Appliable weekdays
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    def days_of_week_list(self):
        """
        Returns a list of ordered integers representing the weekdays marked as True
        """
        res = []
        if self.monday:
            res.append(0)
        if self.tuesday:
            res.append(1)
        if self.wednesday:
            res.append(2)
        if self.thursday:
            res.append(3)
        if self.friday:
            res.append(4)
        if self.saturday:
            res.append(5)
        if self.sunday:
            res.append(6)

        return res

    def days_of_week_string(self):
        return ','.join(map(str, self.days_of_week_list()))

    def has_weekday(self, day):
        """
        Returns True if day is among the weekdays checked as True
        """
        return day in self.days_of_week_list()

    def has_datetime(self, date_time):
        """
        Returns True if date_time occurs inside this time block
        """
        return self.has_weekday(date_time.weekday()) and self.start <= date_time.time() < self.end

    def get_next_weekday(self):
        """
        Calculates and returns which is the next weekday available
        """
        today = datetime.datetime.now().weekday()
        list = self.days_of_week_list()
        for day in list:
            if day >= today:
                next = day
                break
        else:
            # available days for this week are over, return first day of next week
            next = list[0]
        return next

    def next_datetime(self):
        """
        Returns the next datetime "start" time is gonna happen
        """
        now = datetime.datetime.now()
        today = now.weekday()
        available_days = self.days_of_week_list()

        if today in available_days:
            if self.start <= now.time() < self.end:
                # It's now
                return now
            if now.time() < self.start:
                # It's later today
                return datetime.datetime(
                    year=now.year,
                    month=now.month,
                    day=now.day,
                    hour=self.start.hour,
                    minute=self.start.minute)

        # calculate which is the next available weekday (0-6)
        cursor = 0 if today == 6 else today + 1
        while True:
            if cursor in available_days:
                break
            cursor = 0 if cursor == 6 else cursor + 1

        # calculate how many days from now until next available day
        if cursor > today:
            days_delta = cursor - today
        else:
            days_delta = (7 - today) + cursor

        # calculate complete datetime of next schedule start
        next_date = now + datetime.timedelta(days=days_delta)
        next_datetime = datetime.datetime(
            year=next_date.year,
            month=next_date.month,
            day=next_date.day,
            hour=self.start.hour,
            minute=self.start.minute)

        return next_datetime
