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

#ifdef PAIR_CLASS

PairStyle(dpd/fdt/energy,PairDPDfdtEnergy)

#else

#ifndef LMP_PAIR_DPD_FDT_ENERGY_H
#define LMP_PAIR_DPD_FDT_ENERGY_H

#include "pair.h"

namespace LAMMPS_NS {

class PairDPDfdtEnergy : public Pair {
 public:
  PairDPDfdtEnergy(class LAMMPS *);
  virtual ~PairDPDfdtEnergy();
  virtual void compute(int, int);
  virtual void settings(int, char **);
  virtual void coeff(int, char **);
  virtual void init_style();
  virtual double init_one(int, int);
  void write_restart(FILE *);
  void read_restart(FILE *);
  virtual void write_restart_settings(FILE *);
  virtual void read_restart_settings(FILE *);
  double single(int, int, int, int, double, double, double, double &);
  int pack_reverse_comm(int, int, double *);
  void unpack_reverse_comm(int, int *, double *);

  double **cut;
  double **a0;
  double **sigma,**kappa;
  double *duCond,*duMech;

  class RanMars *random;

 protected:
  double cut_global;
  int seed;
  bool splitFDT_flag;

  virtual void allocate();

};

}

#endif
#endif

/* ERROR/WARNING messages:

E: Illegal ... command

Self-explanatory.  Check the input script syntax and compare to the
documentation for the command.  You can use -echo screen as a
command-line option when running LAMMPS to see the offending line.

E: Incorrect args for pair coefficients

Self-explanatory.  Check the input script or data file.

E: Pair dpd/fdt/energy requires ghost atoms store velocity

Use the communicate vel yes command to enable this.

E: Pair dpd/fdt/energy requires newton pair on

Self-explanatory.

E: All pair coeffs are not set

All pair coefficients must be set in the data file or by the
pair_coeff command before running a simulation.

*/
