#! /usr/bin/python


__author__="hanis (Jan Rychtar)"


import getopt
import sys


from gs_module import SiteController


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], None, ['site=', 'domain=',
                    'path=', 'directory='])

    except getopt.error, msg:
        print "wrong input"
        sys.exit(2)

    site = None
    domain = None
    path = None
    directory = None

    for option, arg in opts:
        if option == '--site':
            site = arg
        elif option == '--domain':
            domain = arg
        elif option == '--path':
            path = arg
        elif option == '--directory':
            directory = arg



    siteController = SiteController(site=site, domain=domain)

    siteController.process_modification_doc(path, directory)
    if siteController.modified_since_lasttime():
        site = siteController.get_site()
        siteController.save_site_to_disk(site, path, directory)


if __name__ == "__main__":
    main()


 