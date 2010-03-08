#! /usr/bin/python


__author__="hanis"


import getopt
import sys


from gs_module import SiteController


def main():

    try:
        opts, args = getopt.getopt(sys.argv[1:], None, ['site=', 'domain=',
                    'path=', 'template=', 'email=', 'password=', 'directory='])

    except getopt.error, msg:
        print "wrong input"
        sys.exit(2)

    site = None
    domain = None
    path = None
    template = None
    password = None
    directory = None
    email = None

    for option, arg in opts:
        if option == '--site':
            site = arg
        elif option == '--domain':
            domain = arg
        elif option == '--path':
            path = arg
        elif option == '--template':
            template = arg
        elif option == '--password':
            password = arg
        elif option == '--directory':
            directory = arg
        elif option == '--email':
            email = arg


    siteController = SiteController(site=site, domain=domain, template=template,
                                    email=email, password=password)
    siteController.save_site_to_disk(siteController.get_site(), path, directory)



if __name__ == "__main__":
    main()