# from calendar import HTMLCalendar
import calendar
from datetime import date, timedelta

class WeekCalendar:

    # self.calendar = None
    calendar = calendar.Calendar(calendar.SUNDAY)

    currentDate = None
    previousWeekDate = None
    nextWeekDate = None
    weekNumber = None
    
    def __init__(self,date):
        self.currentDate = date
        self.previousWeekDate = self.currentDate - timedelta(days=7)      
        self.nextWeekDate = self.currentDate + timedelta(days=7)  

        year,self.weekNumber,DOW = self.currentDate.isocalendar()

    def formatWeek(self):
        weekDict = {0:"Monday",1:"Tuesday",2:"Wednesday",3:"Thursday",4:"Friday",5:"Saturday",6:"Sunday"}
        currentWeek = self.getFullWeek(self.currentDate)
        finishedWeek = []
        for day in currentWeek: 
            stringDate = self.formatday(day)
            finishedWeek.append((day,weekDict[day.weekday()],stringDate))
        return finishedWeek
        
    def getNextWeek(self):
        return str(self.nextWeekDate.year) + "-" + str(self.nextWeekDate.month) + "-" + str(self.nextWeekDate.day)

    def getPreviousWeek(self):
        return str(self.previousWeekDate.year) + "-" + str(self.previousWeekDate.month) + "-" + str(self.previousWeekDate.day)

    def getWeekNumber(self):
        return self.weekNumber


    def getFullWeek(self,date):
        week = []
        
        weekStart = 0
        weekEnd = 6

        currentWeekDay = date.weekday()
        pointer = currentWeekDay  + 1
        while pointer > weekStart:
            daysBefore = date - timedelta(days=pointer)
            pointer -= 1
            week.append(daysBefore)

        pointer = 0
        currentWeekDay = date.weekday()
        while pointer < weekEnd - currentWeekDay:
            daysAfter = date + timedelta(days=pointer)
            pointer += 1;
            week.append(daysAfter)

        return week

    def formatday(self,day):
        monthDict={1:"January", 2:"Febuary", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        year = str(day.year)
        month = monthDict[day.month]
        currentDay = str(day.day)
        stringDate = currentDay + " " + month + " " + year

        return stringDate