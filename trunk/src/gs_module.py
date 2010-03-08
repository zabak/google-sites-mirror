

__author__="hanis"


from Cheetah.Template import Template
import gdata.sites.client
import gdata.sites.data
import gdata.gauth

import atom

import re
import os

from objects import Site
from objects import Page
from objects import ListPage
from objects import ListItem




TEMPLATE_PATH = 'templates/'
OUTPUT_PATH = 'output/'
PAGE_NAME = 'index.html'
SOURCE_NAME = 'test-test-v1'

TMPL_FILE_CABINET = TEMPLATE_PATH + 'file_cabinet_template.py'
TMPL_ANNOUNCEMENTS_PAGE = TEMPLATE_PATH + 'announcements_page_template.py'
TMPL_ANNOUNCEMENT = TEMPLATE_PATH + 'announcement_template.py'
TMPL_LISTPAGE = TEMPLATE_PATH + 'listpage_template.py'
TMPL_DEFAULT_WEBPAGE = TEMPLATE_PATH + 'default_template.py'

PAGE_NAME = 'index.html'


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

PAGE_TYPES = [ANNOUNCEMENTS_PAGE, ANNOUNCEMENT, FILE_CABINET, WEBPAGE, LIST_PAGE]
#---------------------------------------------------------------------


class SiteController():


    def __init__(self, site=None, ssl=False, source=None, domain=None, template=None, password=None, email=None):
        if source is None:
            source = SOURCE_NAME
        if domain:
            self.client = gdata.sites.client.SitesClient(source=source, site=site, domain=domain)
        else:
            self.client = gdata.sites.client.SitesClient(source=source, site=site)
        self.client.ssl = ssl
        if template:
            self.template = TEMPLATE_PATH + template
        else:
            self.template = TMPL_DEFAULT_WEBPAGE        
        if password:
            self.client.client_login(email=email, password=password, source=source)


    def get_template(self, template_path):
        file_template = open(template_path, 'r')
        templateDef = file_template.read()
        file_template.close()
        return Template(templateDef)


    def save_as_file(self, content, path):
        outfile = file(path , 'w')
        outfile.write(content)
        outfile.close()


    def download_attachments(self):
        uri = '%s?kind=%s' % (self.client.make_content_feed_uri(), 'attachment')
        feed = self.client.GetContentFeed(uri=uri)
        for entry in feed.entry:
            self.client.DownloadAttachment(entry, OUTPUT_PATH + entry.title.text)



    def request_page_content(self, page_id):
        uri = '%s%s' % (self.client.make_content_feed_uri(), page_id)
        response = self.client.request(method='GET', uri=uri)
        content_str = str(response.read())
        return content_str[content_str.find('<content'): content_str.find('</content>') + 10]


    def request_page_all(self, page_id):
        uri = '%s%s' % (self.client.make_content_feed_uri(), page_id)
        response = self.client.request(method='GET', uri=uri)
        content_str = str(response.read())
        return content_str



    def get_site_path(self):
        if self.client.domain == 'site':
            path = 'http://sites.google.com/site/%s/' % (self.client.site)
        else:
            path = 'http://sites.google.com/a/%s/%s/' % (self.client.domain, self.client.site)
        return path



    def parse_comment(self, comment):
        temp = comment[comment.find('<td'):comment.rfind('</td')]
        return temp[temp.find('>')+1:]



    def replace_paths(self, page, level):
        site_path = self.get_site_path()
        link_list = re.findall(r'<a href="'+ site_path +'.*?"', page)
        for link in link_list:
            relative_path = level * '../' + link[len(site_path)+9:-1]
            new_link = '<a href="%s/index.html"' % (relative_path)
            page = page.replace(link, new_link)
        return page



    def replace_attachment_source(self, page, attachment, parent, as_announcement=None):
        site_path = self.get_site_path()
        current_src='%s_/rsrc/[^>]*/%s%s' % (site_path, parent.path, attachment.name)
        #print current_src
        src_list = re.findall(r''+current_src, page)
        if as_announcement:
            new_src='./%s/%s' % (parent.pagename, attachment.name)
        else:
            new_src='./%s' % (attachment.name)

        for src_item in src_list:
            page = page.replace(src_item, new_src)
        return page



    def save_site_to_disk(self, site, path, directory):
        path_to_site = path + directory + '/'
        os.mkdir(path_to_site)
        for child in site.childs:
            self.save_page_to_disk(page=child, path=path_to_site, site=site)


    def save_page_to_disk(self, page, path, site):
        full_path = path + page.path
        os.mkdir(full_path)

        if page.kind == WEBPAGE:
            template_out = self.get_template(TMPL_DEFAULT_WEBPAGE)
        elif page.kind == FILE_CABINET:
            template_out = self.get_template(TMPL_FILE_CABINET)
        elif page.kind == ANNOUNCEMENTS_PAGE:
            template_out = self.get_template(TMPL_ANNOUNCEMENTS_PAGE)
        elif page.kind == ANNOUNCEMENT:
            template_out = self.get_template(TMPL_ANNOUNCEMENT)
        elif page.kind == LIST_PAGE:
            template_out = self.get_template(TMPL_LISTPAGE)
            

        template_out.page = page
        template_out.site = site
        self.save_as_file(content=str(template_out), path=full_path + PAGE_NAME)

        for attachment in page.attachments:
            self.save_attachment_to_file(attachment, full_path)

        for child in page.childs:
            self.save_page_to_disk(child, path, site=site)



    def save_attachment_to_file(self, attachment, path):
        uri = '%s%s' % (self.client.MakeContentFeedUri(), attachment.id)
        att_entry = self.client.GetEntry(uri, desired_class=gdata.sites.data.ContentEntry)
        self.client.DownloadAttachment(att_entry, path + attachment.name)


    def get_site(self):
        site = Site()

        for kind in PAGE_TYPES:
            uri = '%s?kind=%s' % (self.client.MakeContentFeedUri(), kind)
            feed = self.client.GetContentFeed(uri=uri)
            for entry in feed.entry:
                if entry.FindParentLink() is None:
                    self.get_page(entry, level=1, parent=site)
        return site


    def get_site_content(self, level=1, parent=None):
        uri = '%s?parent=%s' % (self.client.MakeContentFeedUri(), parent.id)
        feed = self.client.GetContentFeed(uri=uri)
        for entry in feed.entry:
            kind = entry.Kind()
            if kind in PAGE_TYPES:
                self.get_page(entry, level, parent)
            if kind == ATTACHMENT:
                self.get_attachment(entry, parent=parent)
            elif kind == COMMENT:
                self.get_comment(entry, parent)
            elif kind == LIST_ITEM:
                self.get_list_item(entry, parent)
            elif kind == WEB_ATTACHMENT:
                self.get_web_attachment(entry, parent)




    def get_page(self, entry, level, parent):
        page = Page(id=entry.GetNodeId(),
                    kind=entry.Kind(),
                    title=entry.title.text,
                    author_name=entry.author[0].name.text,
                    author_email=entry.author[0].email.text,
                    updated=entry.updated.text,
                    revision=entry.revision.text,
                    pagename=entry.page_name.text,
                    parent=parent)

        if page.kind == LIST_PAGE:
            list_page = ListPage()
            for header in entry.data.column:
                list_page.add_header(header.name)
            page.list_items = list_page

        content_str = self.request_page_content(entry.GetNodeId())
        self.get_site_content(level=level+1, parent=page)

        if page.kind == ANNOUNCEMENT:
            content_str2 = content_str
            content_str2 = self.replace_paths(content_str2, level-1)
            for attachment in page.attachments:
                content_str2 = self.replace_attachment_source(page=content_str2, attachment=attachment, parent=page, as_announcement=True)
            page.embedded_content = content_str2

        content_str = self.replace_paths(content_str, level)
        for attachment in page.attachments:
            content_str = self.replace_attachment_source(page=content_str, attachment=attachment, parent=page)
        page.content = content_str
        parent.add_child(page)



    def get_list_item(self, entry, parent):
        item = ListItem(author_name=entry.author[0].name.text,
                        author_email=entry.author[0].email.text,
                        updated=entry.updated.text,
                        revision=entry.revision.text)

        for cell in entry.field:
            item.add_cell(cell.text)
        parent.list_items.add_list_item(item)

    


    def get_attachment(self, entry, parent):
        parent.add_attachment(id=entry.GetNodeId(),
                                author_name=entry.author[0].name.text,
                                author_email=entry.author[0].email.text,
                                name=entry.title.text,
                                summary=entry.summary.text,
                                updated=entry.updated.text,
                                revision=entry.revision.text)

    def get_web_attachment(self, entry, parent):
        parent.add_web_attachment(id=entry.GetNodeId(),
                                author_name=entry.author[0].name.text,
                                author_email=entry.author[0].email.text,
                                name=entry.title.text,
                                summary=entry.summary.text,
                                updated=entry.updated.text,
                                revision=entry.revision.text,
                                web_src=str(entry.content.src))



    def get_comment(self, entry, parent):
        parent.add_comment(text=self.parse_comment(self.request_page_content(entry.GetNodeId())),
                            author_name=entry.author[0].name.text,
                            author_email=entry.author[0].email.text,
                            updated=entry.updated.text,
                            revision=entry.revision.text)



    def show_sites_content(self):  
        feed = self.client.GetContentFeed()        
        for entry in feed.entry:
            #uri = '%s%s' % (self.client.make_content_feed_uri(), entry2.GetNodeId())
            #entry = self.client.GetEntry(self.client.make_content_feed_uri(), desired_class=gdata.sites.data.ContentEntry, etag='"YD0peyA."')
            #print 'etag: ' + entry.etag
            #print 'title: ' + entry.title.text
            print 'kind: ' + entry.Kind()
            #print 'summary' + entry.summary.text
            print 'id: ' + entry.GetNodeId()
            print 'revision: ' + entry.revision.text
            print 'updated: ' + entry.updated.text
            print 'published: ' + entry.published.text            
            if entry.page_name:
                print 'page name: ' + entry.page_name.text

            if entry.content:
                print 'content: ' + str(entry.content.src)
                #print '--------'
                #print 'all content (get request): ' + self.request_page_all(entry.GetNodeId())
                #print '--------'
            
            parent_link = entry.FindParentLink()
            if parent_link:
                    print 'parent link: ' + parent_link

            if entry.GetAlternateLink():
                print 'link at Sites: ' + entry.GetAlternateLink().href

            if entry.feed_link:
                print 'feed of childs: ' + entry.feed_link.href
            print '---------------------------------------------------'


def main():
    pass
    #site = None
    #domain = None
    #source = None
    #template = None
    #email = None
    #password = None

    #path = None
    #directory = None

    #siteController = SiteController(site=site, domain=domain, template = None,
    #                               source=source, email=email, password=password)
    #siteController.show_sites_content()
    #site = siteController.get_site()
    #siteController.save_site_to_disk(site, path, directory)

if __name__ == "__main__":
    main()