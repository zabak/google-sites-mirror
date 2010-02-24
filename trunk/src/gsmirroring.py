#! /usr/bin/python


__author__="hanis"


import getopt
import sys


from gs_module import SiteController


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], None, ['site=', 'domain=', 'path=', 'template='])
    except getopt.error, msg:
        print "wrong input"
        sys.exit(2)


    site = None
    domain = None
    path = None
    template = None

    for option, arg in opts:
        if option == '--site':
            site = arg
        elif option == '--domain':
            domain = arg
        elif option == '--path':
            path = arg
        elif option == '--template':
            template = arg


    siteController = SiteController(site=site, domain=domain, template=template)
    siteController.save_site(path)
    

if __name__ == "__main__":
    main()