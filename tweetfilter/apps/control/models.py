# -*- coding: utf-8 -*-
from time import strptime
import datetime
from django.db import models


class TimeBlock(models.Model):
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

    def has_weekday(self, day):
        """
        Returns True if day is among the weekdays checked as True
        """
        print "checking existence of day %s in list:" % day
        print self.days_of_week_list()
        return day in self.days_of_week_list()

    def has_datetime(self, date_time):
        """
        Returns True if date_time occurs inside this time block
        """
        print "now = %s" % date_time

        start = datetime.datetime.strptime(self.start, "%H:%M").time()
        end = datetime.datetime.strptime(self.end, "%H:%M").time()

        print "checking time = %s" % date_time.time()
        print "has week day? %s" % self.has_weekday(date_time.weekday())
        print "start = %s" % start
        print "end = %s" % end

        return self.has_weekday(date_time.weekday()) and start <= date_time.time() < end

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
            next = list[0]
        return next

    def next_datetime(self):
        """
        Returns the next datetime "start" time is gonna happen
        """
        now = datetime.datetime.now()
        today = now.weekday()
        if self.has_datetime(now):
            return now
        else:
            next_day = self.get_next_weekday()
            if next_day > today:
                days_delta = next_day - today
            else:
                days_delta = (7 - today) + next_day
            time_delta = self.start - now.time()    # does it work?
            return now + datetime.timedelta(days=days_delta, hours=time_delta.hours, minutes=time_delta.minutes)