#!/usr/bin/env python3

# If you consider the output of this program to be legal advice,
# you're insane.

import os, os.path

from optparse import OptionParser

import pyalpm

# DFSG/OSI-approved licenses, and the various variants in naming them
# I see in my package database

import vrms_arch
import vrms_arch.license_finder



parser = OptionParser()

parser.add_option("-g", "--global-repos",
                  dest="use_global_repos",
                  action="store_true",
                  default=False,
                  help="Check licenses in all packages in all synced repositories, rather than that of locally installed packages")
parser.add_option("-a", "--list-all-licenses",
                  dest="list_all_licenses",
                  action="store_true",
                  default=False,
                  help="List all licenses")
parser.add_option("-u", "--list-unknowns",
                  dest="list_unknowns",
                  action="store_true",
                  default=False,
                  help="List unknown packages instead of non-free packages")

(options, args) = parser.parse_args()

h = pyalpm.Handle("/", "/var/lib/pacman")

dbs_to_visit = []

if(options.use_global_repos):
    for d in os.listdir("/var/lib/pacman/sync"):
        h.register_syncdb(os.path.splitext(d)[0], 0)
    dbs_to_visit = h.get_syncdbs()
else:
    # print("There are %d installed packages." % len(h.get_localdb()))
    dbs_to_visit.append(h.get_localdb())

visitor = vrms_arch.license_finder.LicenseFinder()

for db in dbs_to_visit:
    print("Reading pacman DB: %s" % db.name)
    visitor.visit_db(db)

if options.list_unknowns:
    visitor.list_all_unknown_packages()
if options.list_all_licenses:
    visitor.list_all_licenses_as_python()
else:
    visitor.list_all_nonfree_packages()




# print out a convenient list of all licenses on the box:
# seen_licenses = []
# for pkg in pkgs:
#     for license in pkg.licenses:
#         if license not in seen_licenses:
#             seen_licenses.append(license)
# seen_licenses.sort()
# for lic in seen_licenses:
#     print("    \"%s\"," % lic)

# print("Seen licenses: %s" % seen_licenses)


