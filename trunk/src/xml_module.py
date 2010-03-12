
__author__="hanis"


from xml.dom import minidom

import time


class ETagDocument():


    ATTACHMENT = 'attachment'
    PAGE = 'page'


    def __init__(self):
        self.document=None
        self.attachment_map = {}
        self.page_map = {}

    def create(self):
        self.document = minidom.Document()
        site_element = self.document.createElement('site')        
        self.document.appendChild(site_element)

        attachments_element = self.document.createElement('attachments')
        pages_element = self.document.createElement('pages')
        site_element.appendChild(attachments_element)
        site_element.appendChild(pages_element)


    def set_modification_time(self, time):
        self.document.getElementsByTagName('site')[0].setAttribute('updated', time)



    def check_attachment(self, id, etag):
        """ returns true if an attachment with id=id is modified or new"""
        if self.attachment_map.has_key(id):
            old_etag = self.attachment_map[id][0]
            del self.attachment_map[id]
            return not old_etag == etag
        else:
            return True


    def get_deleted_attachments(self):
        return self.attachment_map.values()


    def get_parent_element(self, type):
        if type == self.ATTACHMENT:
            return 'attachments'
        elif type == self.PAGE:
            return 'pages'


    def add_element(self, id, source, etag, type):
        element = self.document.createElement(type)
        element.setAttribute('id', str(id))
        element.setAttribute('source', str(source))
        element.setAttribute('etag', str(etag))
        self.document.getElementsByTagName(self.get_parent_element(type))[0].appendChild(element)

    def add_attachment(self, id, source, etag):
        att_element = self.document.createElement('attachment')
        att_element.setAttribute('id', str(id))
        att_element.setAttribute('source', str(source))
        att_element.setAttribute('etag', str(etag))
        self.document.getElementsByTagName.firstChild.appendChild(att_element)


    def get_modification_time(self):
        return self.document.getElementsByTagName('site')[0].getAttribute('updated')

    def get_document(self, path):
        self.document = minidom.parse(path)

        for node in self.document.getElementsByTagName('attachment'):
            self.attachment_map[node.getAttribute('id')]=[node.getAttribute('etag'),node.getAttribute('source')]



    def to_string(self):
        return self.document.toprettyxml(encoding='UTF-8')




if __name__ == "__main__":
    pass
    