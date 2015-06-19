/* -*- c++ -*- ----------------------------------------------------------
   LAMMPS - Large-scale Atomic/Molecular Massively Parallel Simulator
   http://lammps.sandia.gov, Sandia National Laboratories
   Steve Plimpton, sjplimp@sandia.gov

   Copyright (2003) Sandia Corporation.  Under the terms of Contract
   DE-AC04-94AL85000 with Sandia Corporation, the U.S. Government retains
   certain rights in this software.  This software is distributed under
   the GNU General Public License.

   See the README file in the top-level LAMMPS directory.
------------------------------------------------------------------------- */

#ifdef FIX_CLASS

FixStyle(divide,FixDivide)

#else

#ifndef LMP_FIX_DIVIDE_H
#define LMP_FIX_DIVIDE_H

#include "fix.h"

namespace LAMMPS_NS {

class FixDivide : public Fix {
 public:
 
  FixDivide(class LAMMPS *, int, char **);
  ~FixDivide();
  int setmask();
  // void post_constructor();
  void init();
  // void setup_pre_force(int);
  // void pre_force(int);
  void pre_exchange();
  // void end_of_step();
  // void post_run();
  // void setup_pre_force_respa(int,int);
  // void pre_force_respa(int,int,int);
  // void set_arrays(int);

 private:

  double growthFactor;
  int seed;
  // bool preExchangeCalled;
  class RanPark *random;

  int me,nprocs;
  int *recvcounts,*displs;
  tagint maxtag_all,maxmol_all;
  double xlo,xhi,ylo,yhi,zlo,zhi;
  double xc,yc,rc;
  double radius_max;
  double lo_current,hi_current;
  int region_style;
  void find_maxid();
  int overlap(int);
  int outside(int, double, double, double);
  // double getAverageMass();
  int countNewAtoms(double averageMass);

};

}

#endif
#endif

/* ERROR/WARNING messages:

E: Illegal ... command

Self-explanatory.  Check the input script syntax and compare to the
documentation for the command.  You can use -echo screen as a
command-line option when running LAMMPS to see the offending line.

E: Cannot use dynamic group with fix adapt atom

This is not yet supported.

E: Variable name for fix adapt does not exist

Self-explanatory.

E: Variable for fix adapt is invalid style

Only equal-style variables can be used.

E: Fix adapt pair style does not exist

Self-explanatory

E: Fix adapt pair style param not supported

The pair style does not know about the parameter you specified.

E: Fix adapt type pair range is not valid for pair hybrid sub-style

Self-explanatory.

E: Fix adapt kspace style does not exist

Self-explanatory.

E: Fix adapt requires atom attribute diameter

The atom style being used does not specify an atom diameter.

E: Fix adapt requires atom attribute charge

The atom style being used does not specify an atom charge.

E: Could not find fix adapt storage fix ID

This should not happen unless you explicitly deleted
a secondary fix that fix adapt created internally.

*/
