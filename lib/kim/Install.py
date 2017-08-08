#!/usr/bin/env python

# install.py tool to download, compile, and setup the kim-api library
# used to automate the steps described in the README file in this dir

from __future__ import print_function
import sys,os,re,subprocess

help = """
Syntax from src dir: make lib-kim args="-b -v version  -a kim-name"
                 or: make lib-kim args="-b -a everything"
                 or: make lib-kim args="-n -a kim-name"
                 or: make lib-kim args="-p /usr/local/open-kim -a kim-name"
Syntax from lib dir: python Install.py -b -v version  -a kim-name
                 or: python Install.py -b -a everything
                 or: python Install.py -n -a kim-name
                 or: python Install.py -p /usr/local/open-kim -a kim-name

specify one or more options, order does not matter

  -v = version of KIM API library to use
       default = kim-api-v1.8.2 (current as of June 2017)
  -b = download and build base KIM API library with example Models
       this will delete any previous installation in the current folder
  -n = do NOT download and build base KIM API library.
       Use an existing installation 
  -p = specify location of KIM API installation (implies -n)
  -a = add single KIM model or model driver with kim-name
       to existing KIM API lib (see example below).
       If kim-name = everything, then rebuild KIM API library with
       *all* available OpenKIM Models (make take a long time).
  -vv = be more verbose about what is happening while the script runs

Examples:

make lib-kim args="-b" # install KIM API lib with only example models
make lib-kim args="-a Glue_Ercolessi_Adams_Al__MO_324507536345_001"  # Ditto plus one model
make lib-kim args="-b -a everything"   # install KIM API lib with all models
make lib-kim args="-n -a EAM_Dynamo_Ackland_W__MO_141627196590_002"   # only add one model or model driver

See the list of KIM model drivers here:
https://openkim.org/kim-items/model-drivers/alphabetical

See the list of all KIM models here:
https://openkim.org/kim-items/models/by-model-drivers

See the list of example KIM models included by default here:
https://openkim.org/kim-api
in the "What is in the KIM API source package?" section
"""

def error(str=None):
  if not str: print(help)
  else: print("ERROR",str)
  sys.exit()

# expand to full path name
# process leading '~' or relative path

def fullpath(path):
  return os.path.abspath(os.path.expanduser(path))

def geturl(url,fname):
  cmd = 'curl -L -o "%s" %s' % (fname,url)
  txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  return txt

# parse args

args = sys.argv[1:]
nargs = len(args)
if nargs == 0: error()

thisdir = os.environ['PWD']
version = "kim-api-v1.8.2"

buildflag = False
everythingflag = False
addflag = False
verboseflag = False
pathflag = False

iarg = 0
while iarg < len(args):
  if args[iarg] == "-v":
    if iarg+2 > len(args): error()
    version = args[iarg+1]
    iarg += 2
  elif args[iarg] == "-b":
    buildflag = True
    iarg += 1
  elif args[iarg] == "-n":
    buildflag = False
    iarg += 1
  elif args[iarg] == "-p":
    if iarg+2 > len(args): error()
    kimdir = fullpath(args[iarg+1])
    pathflag = True
    buildflag = False
    iarg += 2
  elif args[iarg] == "-a":
    addflag = True
    if iarg+2 > len(args): error()
    addmodelname = args[iarg+1]
    if addmodelname == "everything":
      buildflag = True
      everythingflag = True
      addflag = False
    iarg += 2
  elif args[iarg] == "-vv":
    verboseflag = True
    iarg += 1
  else: error()

thisdir = os.path.abspath(thisdir)
url = "https://s3.openkim.org/kim-api/%s.tgz" % version

# set KIM API directory

if pathflag:
  if not os.path.isdir(kimdir):
    print("\nkim-api is not installed at %s" % kimdir)
    error()

  # configure LAMMPS to use existing kim-api installation
  with open("%s/Makefile.KIM_DIR" % thisdir, 'w') as mkfile:
    mkfile.write("KIM_INSTALL_DIR=%s\n\n" % kimdir)
    mkfile.write(".DUMMY: print_dir\n\n")
    mkfile.write("print_dir:\n")
    mkfile.write("	@printf $(KIM_INSTALL_DIR)\n")

  with open("%s/Makefile.KIM_Config" % thisdir, 'w') as cfgfile:
    cfgfile.write("include %s/lib/kim-api/Makefile.KIM_Config" % kimdir)

  print("Created %s/Makefile.KIM_DIR\n  using %s" % (thisdir,kimdir))
else:
  kimdir = os.path.join(os.path.abspath(thisdir), "installed-" + version)

# download KIM tarball, unpack, build KIM
if buildflag:

  # check to see if an installed kim-api already exists and wipe it out.

  if os.path.isdir(kimdir):
    print("kim-api is already installed at %s.\nRemoving it for re-install" % kimdir)
    cmd = 'rm -rf "%s"' % kimdir
    subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

  # configure LAMMPS to use kim-api to be installed

  with open("%s/Makefile.KIM_DIR" % thisdir, 'w') as mkfile:
    mkfile.write("KIM_INSTALL_DIR=%s\n\n" % kimdir)
    mkfile.write(".DUMMY: print_dir\n\n")
    mkfile.write("print_dir:\n")
    mkfile.write("	@printf $(KIM_INSTALL_DIR)\n")

  with open("%s/Makefile.KIM_Config" % thisdir, 'w') as cfgfile:
    cfgfile.write("include %s/lib/kim-api/Makefile.KIM_Config" % kimdir)

  print("Created %s/Makefile.KIM_DIR\n  using %s" % (thisdir,kimdir))

  # download entire kim-api tarball

  print("Downloading kim-api tarball ...")
  geturl(url,"%s/%s.tgz" % (thisdir,version))
  print("Unpacking kim-api tarball ...")
  cmd = 'cd "%s"; rm -rf "%s"; tar -xzvf %s.tgz' % (thisdir,version,version)
  subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

  # configure kim-api

  print("Configuring kim-api ...")
  cmd = 'cd "%s/%s"; ./configure --prefix="%s"' % (thisdir,version,kimdir)
  subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

  # build kim-api

  print("Configuring example Models")
  cmd = 'cd "%s/%s"; make add-examples' % (thisdir,version)
  txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  if verboseflag: print (txt.decode("UTF-8"))

  if everythingflag:
    print("Configuring all OpenKIM models, this will take a while ...")
    cmd = 'cd "%s/%s"; make add-OpenKIM' % (thisdir,version)
    txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    if verboseflag: print(txt.decode("UTF-8"))

  print("Building kim-api ...")
  cmd = 'cd "%s/%s"; make' % (thisdir,version)
  txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  if verboseflag: print(txt.decode("UTF-8"))

  # install kim-api

  print("Installing kim-api ...")
  cmd = 'cd "%s/%s"; make install' % (thisdir,version)
  txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  if verboseflag: print(txt.decode("UTF-8"))

  cmd = 'cd "%s/%s"; make install-set-default-to-v1' %(thisdir,version)
  txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  if verboseflag: print(txt.decode("UTF-8"))

  # remove source files

  print("Removing kim-api source and build files ...")
  cmd = 'cd "%s"; rm -rf %s; rm -rf %s.tgz' % (thisdir,version,version)
  subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

# add a single model (and possibly its driver) to existing KIM installation

if addflag:

  if not os.path.isdir(kimdir):
    print("\nkim-api is not installed")
    error()

  # download single model

  print("Downloading tarball for %s..." % addmodelname)
  url = "https://openkim.org/download/%s.tgz" % addmodelname
  geturl(url,"%s/%s.tgz" % (thisdir,addmodelname))

  print("Unpacking item tarball ...")
  cmd = 'cd "%s"; tar -xzvf %s.tgz' % (thisdir,addmodelname)
  subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)

  print("Building item ...")
  cmd = 'cd "%s/%s"; make; make install' %(thisdir,addmodelname)
  try:
    txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
  except subprocess.CalledProcessError as e:

    # Error: but first, check to see if it needs a driver
    firstRunOutput = e.output.decode("UTF-8")

    cmd = 'cd "%s/%s"; make kim-item-type' % (thisdir,addmodelname)
    txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
    txt = txt.decode("UTF-8")
    if txt == "ParameterizedModel":

      # Get and install driver

      cmd = 'cd "%s/%s"; make model-driver-name' % (thisdir,addmodelname)
      txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
      adddrivername = txt.decode("UTF-8").strip()
      print("First installing model driver: %s..." % adddrivername)
      cmd = 'cd "%s"; python Install.py -n -a %s' % (thisdir,adddrivername)
      try:
        txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
      except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit()

      if verboseflag: print(txt.decode("UTF-8"))

      # now install the model that needed the driver

      print("Now installing model : %s" % addmodelname)
      cmd = 'cd "%s"; python Install.py -n -a %s' % (thisdir,addmodelname)
      try:
        txt = subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
      except subprocess.CalledProcessError as e:
        print(e.output)
        sys.exit()
      print(txt.decode("UTF-8"))
      sys.exit()
    else:
      print(firstRunOutput)
      print("Error, unable to build and install OpenKIM item: %s" \
            % addmodelname)
      sys.exit()

  # success the first time

  if verboseflag: print(txt.decode("UTF-8"))
  print("Removing kim item source and build files ...")
  cmd = 'cd "%s"; rm -rf %s; rm -rf %s.tgz' %(thisdir,addmodelname,addmodelname)
  subprocess.check_output(cmd,stderr=subprocess.STDOUT,shell=True)
