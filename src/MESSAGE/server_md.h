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

#ifndef LMP_SERVER_MD_H
#define LMP_SERVER_MD_H

#include "pointers.h"

namespace LAMMPS_NS {

class ServerMD : protected Pointers {
 public:
  ServerMD(class LAMMPS *);
  void loop();

 private:
  void box_change(double *, double *, double *);
  void send_fev(int);
};

}

#endif
