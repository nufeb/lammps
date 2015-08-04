# This directory contains moltemplate files for the "Pyramids of Giza" example.
# (Note: the ground lattice work that appears in some images was not generated
#        by moltemplate. Moltemplate can not currently create bonded periodic
#        structures as of 2013-4-04.  Those were generated by topotools.)
#
# To run moltemplate, use:

moltemplate.sh system.lt

# This will generate:system.data, system.in, system.in.init, system.in.settings
# 
# The output_ttree/ directory will contain files like "Data Atoms", "Data Bonds"
# which contain the corresponding structures of the system.data file.
# (This might make it slightly easier to combine them with atom data and 
#  bond data generated by other programs, such as topotools, for example.)
