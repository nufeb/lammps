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

#ifndef LMP_NEIGH_REQUEST_H
#define LMP_NEIGH_REQUEST_H

#include "pointers.h"

namespace LAMMPS_NS {

class NeighRequest : protected Pointers {
 public:
  int index;                // index of which neigh request this is
  void *requestor;          // class that made request
  int requestor_instance;   // instance of that class (only Fix, Compute, Pair)
  int id;                   // ID of request as stored by requestor
                            // used to track multiple requests from one class

  // which class style requests the list, one flag is 1, others are 0

  int pair;              // set by default
  int fix;
  int compute;
  int command;

  // kind of list requested, one flag is 1, others are 0
  // NOTE: should make only the first 3 settings be unique,
  //         allow others as add-on flags
  //       this will require changed flags in pair requestors
  //       this will lead to simpler logic in Neighbor::choose_build()

  int half;              // 1 if half neigh list (set by default)
  int full;              // 1 if full neigh list
  int half_from_full;    // 1 if half list computed from previous full list
  int gran;              // 1 if granular list
  int granhistory;       // 1 if history info for granular contact pairs
  int respainner;        // 1 if a rRESPA inner list
  int respamiddle;       // 1 if a rRESPA middle list
  int respaouter;        // 1 if a rRESPA outer list

  // command_style only set if command = 1
  // allows print_pair_info() to access command name

  const char *command_style;

  // -----------------
  // optional settings, set by caller, all are 0 by default
  // -----------------

  // 0 if needed every reneighboring during run
  // 1 if occasionally needed by a fix, compute, etc

  int occasional;

  // 0 if use force::newton_pair setting
  // 1 if override with pair newton on
  // 2 if override with pair newton off

  int newton;

  // 1 if one-sided granular list for sphere/surf interactions (gran = 1)

  int granonesided;

  // number of auxiliary floating point values to store, 0 if none set

  int dnum;

  // 1 if also need neighbors of ghosts

  int ghost;

  // 1 if using multi-threaded neighbor list build for USER-OMP or USER-INTEL

  int omp;
  int intel;

  // 1 if using Kokkos neighbor build

  int kokkos_host;
  int kokkos_device;

  // 1 if using Shardlow Splitting Algorithm (SSA) neighbor list build
  
  int ssa;

  // -----------------
  // end of optional settings
  // -----------------
  
  // set by pair_hybrid and neighbor after all requests are made
  // these settings do not change kind value or optional settings

  int copy;              // 1 if this list copied from another list

  int skip;              // 1 if this list skips atom types from another list
  int *iskip;            // iskip[i] if atoms of type I are not in list
  int **ijskip;          // ijskip[i][j] if pairs of type I,J are not in list
  int off2on;            // 1 if this is newton on list, but skips from off list

  int otherlist;         // index of other list to copy or skip from

  // original params by requestor
  // stored to compare against in identical() in case Neighbor changes them

  int half_original;
  int half_from_full_original;
  int copy_original;
  int otherlist_original;

  // pointer to FSH class, set by caller

  class FixShearHistory *fix_history;  // fix that stores history info

  // methods

  NeighRequest(class LAMMPS *);
  ~NeighRequest();
  void archive();
  int identical(NeighRequest *);
  int same_kind(NeighRequest *);
  int same_skip(NeighRequest *);
  void copy_request(NeighRequest *);
};

}

#endif
