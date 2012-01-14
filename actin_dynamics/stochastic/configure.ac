#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

# ---------------------------------------------------------------------
# Basic setup
# ---------------------------------------------------------------------
AC_PREREQ(2.61)

AC_INIT([Stochastic Simulation Using Gillespie Algorithm], [0.1],
        [Mark Burnett <mark.m.burnett@gmail.com>],
        [stochastic])

AC_CONFIG_AUX_DIR([config])

AM_INIT_AUTOMAKE(test, 0.1)

AC_PROG_LIBTOOL

#AC_CONFIG_SRCDIR([code/nuclear/state.cpp])
#AC_CONFIG_HEADER([config.h])

# ---------------------------------------------------------------------
# Basic checks for programs.
# ---------------------------------------------------------------------
AC_PROG_CC
AC_PROG_CXX
AC_LANG_CPLUSPLUS
AM_SANITY_CHECK

# ---------------------------------------------------------------------
# Distrubtion related variables
# ---------------------------------------------------------------------
EXTRA_DIST=bootstrap

# ---------------------------------------------------------------------
# Checks for libraries.
# ---------------------------------------------------------------------
# Google test library.
# FIXME do a version check on gtest (1.2.1 is what I have installed)
GTEST_CFLAGS=`gtest-config --cppflags --cxxflags`
GTEST_LIBS=`gtest-config --ldflags  --libs`

AC_SUBST(GTEST_CFLAGS)
AC_SUBST(GTEST_LIBS)

# Boost program options library
BOOST_PROGRAM_OPTIONS_CFLAGS=""
BOOST_PROGRAM_OPTIONS_LIBS="-lboost_program_options-mt"

AC_SUBST(BOOST_PROGRAM_OPTIONS_CFLAGS)
AC_SUBST(BOOST_PROGRAM_OPTIONS_LIBS)

CXXFLAGS="$CXXFLAGS -W -Wall -Werror" #-pg -DNDEBUG"
AC_SUBST(CXXFLAGS)

# ---------------------------------------------------------------------
# Checks for header files.
# ---------------------------------------------------------------------
# Project header files
#FIXME this should probably be organized without an include dir
PROJECT_INCLUDES=-I`pwd`/include
AC_SUBST(PROJECT_INCLUDES)

# ---------------------------------------------------------------------
# Checks for typedefs, structures, and compiler characteristics.
# ---------------------------------------------------------------------
AC_HEADER_STDBOOL
AC_C_CONST
AC_TYPE_SIZE_T

# ---------------------------------------------------------------------
# Checks for library functions.
# ---------------------------------------------------------------------
AC_CHECK_FUNCS([abs min max pow sqrt])

# ---------------------------------------------------------------------
# Files configure will be responsible for.
# ---------------------------------------------------------------------
AC_CONFIG_FILES([Makefile])

AC_OUTPUT
