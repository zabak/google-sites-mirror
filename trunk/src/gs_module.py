

__author__="hanis"


from Cheetah.Template import Template
import gdata.sites.client
import gdata.sites.data
import gdata.gauth

import re
import string
import os



TEMPLATE_PATH = 'templates/'
OUTPUT_PATH = 'output/'
PAGE_NAME = 'index.html'
SOURCE_NAME = 'test-test-v1'

TMPL_FILE_CABINET = TEMPLATE_PATH + 'file_cabinet_template.py'
TMPL_ANNOUNCEMENTS = TEMPLATE_PATH + 'announcements_template.py'
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
#---------------------------------------------------------------------


class SiteController():


    def __init__(self, site=None, ssl=False, source=None, domain=None, template=None):
        self.path_to_site=''
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



    def apply_template(self, content):
        file_template = open(self.template, 'r')
        templateDef = file_template.read()
        file_template.close()
        template_out = Template(templateDef)
        template_out.title = 'ddd'
        template_out.content = content
        return str(template_out)



    def request_page_content(self, page_id):
        uri = '%s%s' % (self.client.make_content_feed_uri(), page_id)
        response = self.client.request(method='GET', uri=uri)
        content_str = str(response.read())
        return content_str[content_str.find('<content'): content_str.find('</content>') + 10]



    def get_site_path(self):
        if self.client.domain == 'site':
            path = 'http://sites.google.com/site/%s/' % (self.client.site)
        else:
            path = 'http://sites.google.com/a/%s/%s/' % (self.client.domain, self.client.site)
        return path



    def replace_paths(self, page, level):
        site_path = self.get_site_path()
        link_list = re.findall(r'<a href="'+ site_path +'.*?"', page)
        for link in link_list:
            relative_path = level * '../' + link[len(site_path)+9:-1]
            new_link = '<a href="%s/index.html"' % (relative_path)
            page = page.replace(link, new_link)
        return page




    def replace_attachment_source(self, page, entry, path):
        site_path = self.get_site_path()
        for att in entry:
            current_src='%s_/rsrc/[^>]*/%s%s' % (site_path, path[len(self.path_to_site):], att.title.text)
            src_list = re.findall(r''+current_src, page)
            new_src='./%s' % (att.title.text)
            for src_item in src_list:
                page = page.replace(src_item, new_src)
        return page










    def save_site(self, path):
        self.path_to_site = OUTPUT_PATH + path + '/'
        os.mkdir(self.path_to_site)
        self.save_site_content(path=self.path_to_site, level=1)



    def save_site_content(self, path, parent=None, level=1):
        if parent:
            uri = '%s?parent=%s' % (self.client.MakeContentFeedUri(), parent)
            feed = self.client.GetContentFeed(uri=uri)
        else:
            feed = self.client.GetContentFeed(self.client.MakeContentFeedUri())

        for entry in feed.entry:
            if parent or entry.FindParentLink() is None:
                kind = entry.Kind()
                if kind == WEBPAGE:
                    new_path = path + entry.page_name.text + '/'
                    print '...webpage (%s) ---> %s' %(entry.page_name.text, new_path)
                    os.mkdir(new_path)
                    self.save_page(new_path, entry, level)
                    self.save_site_content(new_path, entry.GetNodeId(), level+1)
                elif kind == ATTACHMENT:
                    print '...attachment (%s) ---> %s' %(entry.title.text, path)
                    self.save_attachment(entry, path=path)
                elif kind == FILE_CABINET:
                    new_path = path + entry.page_name.text + '/'
                    print '...file cabinet (%s) ---> %s' %(entry.title.text, new_path)
                    os.mkdir(new_path)
                    self.save_file_cabinet(new_path, entry)
                elif kind == ANNOUNCEMENTS_PAGE:
                    new_path = path + entry.page_name.text + '/'
                    print '...annoucement page (%s) ---> %s' %(entry.page_name.text, new_path)
                    os.mkdir(new_path)
                    self.save_announcements(new_path, entry, level)
                elif kind == LIST_PAGE:
                    new_path = path + entry.page_name.text + '/'
                    print '...listpage (%s) ---> %s' %(entry.page_name.text, new_path)
                    os.mkdir(new_path)
                    self.save_listpage(new_path, entry, level)




    def save_announcements(self, path, entry, level):
        template_out = self.get_template(TMPL_ANNOUNCEMENTS)
        template_out.title = entry.title.text
        template_out.revision = entry.revision.text
        template_out.updated = entry.updated.text

        feed = self.client.GetContentFeed(uri=entry.feed_link.href)
        entries = feed.entry
        ann_pages=[]
        i=0
        for sub_entry in entries:
            new_path = path + sub_entry.page_name.text + '/'
            os.mkdir(new_path)
            self.save_page(entry=sub_entry, path=new_path, level=level+1)
            ann_pages.insert(i, self.request_page_content(sub_entry.GetNodeId()))
            i=i+1
        template_out.pages = ann_pages
        self.save_as_file(content=str(template_out), path=path + PAGE_NAME)


    def save_listpage(self, path, entry, level):
        template_out = self.get_template(TMPL_LISTPAGE)
        template_out.title = entry.title.text
        template_out.content = self.request_page_content(entry.GetNodeId())
        template_out.headers = entry.data.column

        feed = self.client.GetContentFeed(uri=entry.feed_link.href)
    
        entries = []
        for entry in feed.entry:
            row = []
            for item in entry.field:
                row.append(item.text)
            entries.append(row)
        
        template_out.entries = entries
        self.save_as_file(content=str(template_out), path=path + PAGE_NAME)


    def save_file_cabinet(self, path, entry):
        template_out = self.get_template(TMPL_FILE_CABINET)
        template_out.title = entry.title.text
        template_out.revision = entry.revision.text
        template_out.updated = entry.updated.text

        feed = self.client.GetContentFeed(uri=entry.feed_link.href)
        entries = feed.entry
        template_out.entries = entries
        for sub_entry in entries:
            self.save_attachment(entry=sub_entry, path=path)
        self.save_as_file(content=str(template_out), path=path + PAGE_NAME)


    def save_attachment(self, entry, path):
        self.client.DownloadAttachment(entry, path + str(entry.title.text))




    def save_page(self, path, entry, level):
        content_str = self.request_page_content(entry.GetNodeId())
        if self.template:
            output = self.apply_template(content_str)
        else:
            output = content_str
        uri = '%s?parent=%s&kind=%s' % (self.client.MakeContentFeedUri(), str(entry.GetNodeId()),ATTACHMENT)
        feed = self.client.GetContentFeed(uri=uri)
        
        output = self.replace_paths(output, level)
        output = self.replace_attachment_source(page=output, entry=feed.entry, path=path)

        self.save_as_file(content=output, path=path + PAGE_NAME)








#    def get_replacement_map(self, webpage):
#        uri = '%s?path=/%s' % (self.client.make_content_feed_uri(), webpage)
#        #client = gdata.client.GDClient()
#        #response = self.client.request(method='GET', uri='http://sites.google.com/feeds/content/staremapy.cz/www?path=/home')
#        response = self.client.request(method='GET', uri=uri)
#        content_str = response.read()
#        replacement_keys=[]
#        replacement_values=[]
#        replacements = {}
#        i=0
#        for item in re.findall(r'a name="(.*?)"', content_str):
#            replacement_keys.insert(i, item)
#            i=i+1
#        j=0
#        for item in re.findall(r'<[hH][2-5].*?><a name=.*?</[Hh][2-5]>', content_str):
#            replacement_values.insert(j, item)
#            j=j+1
#        k=0
#        for item in replacement_keys:
#            replacements[replacement_keys[k]]=replacement_values[k]
#            k=k+1
#        return replacements
#    GetReplacementMap = get_replacement_map




#    def parse_page(self, page_content, page_name):
#        replacements = self.GetReplacementMap(page_name)
#        parse_str = string.replace(str(page_content), 'html:', '')
#
#        for key in replacements.iteritems():
#            exp='<[hH][2-5].*?><a name="' + key[0] + '".*?</[Hh][2-5]>'
#            #reg = re.compile(exp)
#            parse_str = re.sub(r'<[hH][2-5][^<]*><a name="' + key[0] + '".*?</[Hh][2-5]>', key[1], parse_str)
#        return parse_str




    def show_sites_content(self):        
        feed = self.client.GetContentFeed()
        for entry in feed.entry:
            print 'title: ' + entry.title.text
            print 'kind: ' + entry.Kind()

            print 'id: ' + entry.GetNodeId()
            print 'revision: ' + entry.revision.text
            print 'updated: ' + entry.updated.text

            if entry.page_name:
                print 'page name: ' + entry.page_name.text

            if entry.content:
                print 'content: ' + str(entry.content)
                print '--------'
                print 'content (get request): ' + self.request_page_content(entry.GetNodeId())
            
            parent_link = entry.FindParentLink()
            if parent_link:
                    print 'parent link: ' + parent_link

            if entry.GetAlternateLink():
                print 'link at Sites: ' + entry.GetAlternateLink().href

            if entry.feed_link:
                print 'feed of childs: ' + entry.feed_link.href
            print '---------------------------------------------------'




def main():

    siteController = SiteController(site='gsmirrortest2', template = 'my_template.py')
    siteController.save_site('site')



if __name__ == "__main__":
    main()