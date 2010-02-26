import date
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hanis"
__date__ ="$25.2.2010 16:50:26$"



CZ = 'cz'
EN = 'en'


class CollectiveObject:
    title = None
    revision = None
    updated = None

    def set_date(self, updated):
        self.updated = Date(updated)



class Author():
    def __init__(self, name, email):
        self.email = email
        self.name = name

class FileCabinet(CollectiveObject):
    files=[]

    def add_file(self, author_name, author_email, name, summary, updated, revision):
        author = Author(author_name, author_email)
        file = File(author, name, summary, updated, revision)
        self.files.append(file)

class File(CollectiveObject):

    def __init__(self, author, name, summary, updated, revision):
        self.author = author
        self.summary = summary
        self.name = name
        self.updated = Date(updated)
        self.revision = revision


class Tee():
    def write_it(self, date):
        return Date().parse_date(date)

class Date():

    months={'1':'Jan', '2':'Feb', '3':'Mar', '4':'Apr', '5':'May',
            '6':'Jun', '7':'Jul', '8':'Aug', '9':'Sep', '10':'Oct',
            '11':'Nov', '12':'Dec'}



    def __init__(self, date_string):
        self.cz=self.parse_date(date_string, CZ)
        self.en=self.parse_date(date_string, EN)


    def parse_date(self, date_string, format):
        date = date_string[0:10].split('-')
        time = date_string[11:19].split(':')
        year=date[0]
        month=date[1]
        if month[0] == '0':
            month=month[1:]
        day=date[2]
        if day[0] == '0':
            day=day[1:]

        hours=time[0]
        minutes=time[1]
        if format==EN:
            period = 'AM'
            hour_num = int(hours)
            if hour_num > 11:
                hour_num = hour_num - 12
                hours = str(hour_num)
                period ='PM'
            return '%s %s, %s %s:%s %s' % (self.months[month], day, year, hours, minutes, period)
        elif format==CZ:
            return '%s. %s. %s %s:%s' % (day, month, year, hours, minutes)


if __name__ == "__main__":
    date = Date('1997-07-16T19:20:30.45+01:00')
    print date.cz
    print date.en


