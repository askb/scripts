#!/usr/bin/env python
"""
usage: python mmake.py [options] [module_name] file1.c [filesX.c]

+ automate linux kernel module's build system.
+ create a make file
+ Need to add:
make prepare
make script
make M=</path/my/module>

ex:
mmake.py file1.c
mmake.py module_name file1.c file2.c
"""

import os
from optparse import OptionParser, SUPPRESS_USAGE
from shutil import rmtree
from string import Template
from subprocess import call
from sys import exit

makefile_content = """\
# If KERNELRELEASE is defined, we've been invoked from the
# kernel build system and can use its language.
ifneq ($(KERNELRELEASE),)
obj-m := $MODULE.o
$MODULE-objs := $FILES

# Otherwise we were called directly from the command
# line; invoke the kernel build system.
else
KDIR := /lib/modules/$(shell uname -r)/build
PWD := $(shell pwd)

default:
$(MAKE) -C $(KDIR) SUBDIRS=$(PWD) modules

endif\
"""

def create_makefile(module_name, files, makefile_location='Makefile',
        makefile_content=makefile_content):
    # Scrub the files list for use in creation of Makefile.
files = [x for x in files if os.path.splitext(os.path.basename(x))[0] !=
        module_name]
files = ' '.join([x + '.o' for x in files])
makefile_template = Template(makefile_content)
makefile_content = makefile_template.safe_substitute(MODULE=module_name,
        FILES=files)
f = open(makefile_location, 'w')
f.write(makefile_content)
f.close()

def build_module(module_name, files, options):
    create_makefile(module_name, files)
verbosity = open(os.devnull, 'w') if not options.verbose else None
call("make", stdout=verbosity, stderr=verbosity)
verbosity.close() if not options.verbose else None

def get_dir_state(path='.'):
    return os.listdir(path)

def set_dir_state(state):
    [os.remove(x) if os.path.isfile(x) else rmtree(x) for x in os.listdir('.') if
            x not in state]

    def make_module(module_name, files, options):
        state = get_dir_state()
build_module(module_name, files, options)
state.append(module_name + '.ko')
if options.remove_temp:
    set_dir_state(state)

if __name__ == '__main__':
    # Use the module doc-string as a descriptor.
OptionParser.format_description = lambda self, formatter: self.description
parser = OptionParser(usage=SUPPRESS_USAGE, description=__doc__)
parser.add_option("-q", "--quiet", dest="verbose", action="store_false",
        default=True, help="supress output")
parser.add_option("-a", dest="remove_temp", action="store_false",
        default=True, help="don't remove make by products")
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
exit(0)
elif len(args) == 1:
    module_name = os.path.splitext(os.path.basename(args[0]))[0]
files = args
else:
    module_name = args[0]
files = args[1:]

make_module(module_name, files, options)
