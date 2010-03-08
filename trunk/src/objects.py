
__author__="hanis"

CZ = 'cz'
EN = 'en'


#------------possible kinds of content entries------------------------
ANNOUNCEMENT = 'announcement'
ANNOUNCEMENTS_PAGE = 'announcementspage'
ATTACHMENT = 'attachment'
COMMENT = 'comment'
FILE_CABINET = 'filecabinet'
LIST_ITEM = 'listitem'
LIST_PAGE = 'listpage'
WEBPAGE = 'webpage'
WEB_ATTACHMENT = 'webattachment'
#---------------------------------------------------------------------



class Author():
    def __init__(self, name, email):
        self.email = email
        self.name = name


class CollectiveObject:
    revision = None
    updated = None
    author = None
    def set_author(self, author_name, author_email):
        self.author = Author(author_name, author_email)
    def set_date_and_revision(self, updated, revision):
        self.updated = Date(updated)
        self.revision = revision


class Commentable():
    def add_comment(self, text, author_name, author_email, updated, revision):        
        self.comments.append(Comment(text, author_name, author_email, updated, revision))


class Parent():
    def add_child(self, child):
        self.childs.append(child)



class Attachmentable():
    def add_attachment(self, id, author_name, author_email, name, summary, updated, revision):
        self.attachments.append(Attachment(id, author_name, author_email, name, summary, updated, revision))
    def add_web_attachment(self, id, author_name, author_email, name, summary, updated, revision, web_src):
        self.web_attachments.append(Attachment(id, author_name, author_email, name, summary, updated, revision, web_src))




class Site(Parent, Attachmentable):
    def __init__(self):
        self.childs = []
        self.attachments = []
        self.path=''
        self.path_to_root=''




class Page(CollectiveObject, Commentable, Parent, Attachmentable):
    def __init__(self, id, title, pagename, kind, author_name, author_email,
                    updated, revision, parent, content=None,
                    embedded_content=None):
        self.id = id
        self.kind = kind
        self.set_author(author_name, author_email)
        self.set_date_and_revision(updated, revision)
        self.title = title
        self.content = content
        self.embedded_content = embedded_content #only for announcemects
        self.comments = []
        self.childs = []
        self.attachments = []
        self.web_attachments = [] #only for file cabinets
        self.parent = parent
        self.pagename = pagename
        self.subpage_path = './' + self.pagename + '/index.html'
        self.path=self.parent.path + self.pagename + '/'
        self.path_to_root=parent.path_to_root + '../'
        self.list_items=None #only for list pages



    def get_predecessors(self):
        predecessors = []
        page = self
        while True:
            page = page.parent
            if isinstance(page, Site):
                break
            print page.path
            predecessors.append(page)
        predecessors.reverse()
        return predecessors


    def get_announcements(self):
        announcements = []
        for page in self.childs:
            if page.kind == ANNOUNCEMENT:
                announcements.append(page)
        return announcements



    def get_alternative_path_to(self, page):
        return page.path_to_root + self.path + 'index.html'




class Comment(CollectiveObject):
    def __init__(self, text, author_name, author_email, updated, revision):
        self.set_author(author_name, author_email)
        self.text = text
        self.set_date_and_revision(updated, revision)



class Attachment(CollectiveObject):
    def __init__(self, id, author_name, author_email, name, summary, updated, revision, web_src=None):
        self.id = id
        self.set_author(author_name, author_email)
        self.summary = summary
        self.name = name
        self.set_date_and_revision(updated, revision)
        self.link = './' + name
        self.web_src = web_src #only for web attachments


class ListPage():
    def __init__(self):
        self.headers = []
        self.items = []
    def add_header(self, header):
        self.headers.append(header)
    def add_list_item(self, item):
        self.items.append(item)

class ListItem(CollectiveObject):
    def __init__(self, author_name, author_email, updated, revision):
        self.cells = []
        self.set_author(author_name, author_email)
        self.set_date_and_revision(updated, revision)
    def add_cell(self, cell):
        self.cells.append(cell)




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
    date = Date('2010-07-16T19:20:30.45+01:00')
    print date.cz
    print date.en

