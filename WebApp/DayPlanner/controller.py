# from calendar import HTMLCalendar
import calendar
from datetime import date, timedelta
from django.core.exceptions import ObjectDoesNotExist

class WeekCalendar:

    # self.calendar = None
    calendar = calendar.Calendar(calendar.SUNDAY)

    week = []
    currentDate = None
    previousWeekDate = None
    nextWeekDate = None
    weekNumber = None
    
    def __init__(self,date):
        self.week = []
        self.currentDate = date
        self.previousWeekDate = self.currentDate - timedelta(days=7)      
        self.nextWeekDate = self.currentDate + timedelta(days=7)

        self.__get_full_week(self.currentDate)

        year,self.weekNumber,DOW = self.currentDate.isocalendar()

    def get_week(self):
        return self.week

    def get_week_span(self):
        return "From:"+ str(self.week[0]) + "  To:" + str(self.week[6])

    def get_week_next(self):
        return str(self.nextWeekDate.year) + "-" + str(self.nextWeekDate.month) + "-" + str(self.nextWeekDate.day)

    def get_week_previous(self):
        return str(self.previousWeekDate.year) + "-" + str(self.previousWeekDate.month) + "-" + str(self.previousWeekDate.day)

    def get_week_number(self):
        return self.weekNumber

    def get_week_schedule(self, stores):
        data = {}
        for store in stores:
            data[store] = {}
            for employee in store.employee_set.all():
                week_schedule = []
                for day in self.week:
                    day_scedule = {}
                    try:
                        day_scedule[day] = employee.dayschedule_set.get(date=day, employee=employee)
                    except ObjectDoesNotExist:
                        day_scedule[day] = None
                    week_schedule.append(day_scedule)

                data[store][employee] = week_schedule
        return data

    def __get_full_week(self, date):

        weekStart = 0
        weekEnd = 6

        currentWeekDay = date.weekday()
        # print currentWeekDay
        pointer = currentWeekDay  + 1

        # TODO fix sunday bug
        # Calenday won't update if sunday

        while pointer > weekStart:
            daysBefore = date - timedelta(days=pointer)
            pointer -= 1
            self.week.append(daysBefore)

        pointer = 0
        currentWeekDay = date.weekday()
        while pointer < weekEnd - currentWeekDay:
            daysAfter = date + timedelta(days=pointer)
            pointer += 1;
            self.week.append(daysAfter)
        # print "--"
        # print "week"
        # return self.week

        print self.week

