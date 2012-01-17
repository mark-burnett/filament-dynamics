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

# ---------------------------------------------------------------------
# Basic checks for programs.
# ---------------------------------------------------------------------
AC_PROG_CC
AC_PROG_CXX
AC_LANG_CPLUSPLUS
AM_SANITY_CHECK

# ---------------------------------------------------------------------
# SWIG
# ---------------------------------------------------------------------
AC_PROG_SWIG
SWIG_ENABLE_CXX
SWIG_PYTHON
AC_DISABLE_STATIC # Do I need this?  Will it hinder profiling?

AM_PATH_PYTHON
PYTHON_INCLUDE="-I/usr/include/python2.6"
AC_SUBST(PYTHON_INCLUDE)

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

# SWIG inadequacies require the following warning settings:
# no-missing-field-initializers and -no-strict-aliasing
CXXFLAGS="$CXXFLAGS -W -Wall -Werror -Wno-unused-parameter -Wno-missing-field-initializers -Wno-strict-aliasing" #-pg -DNDEBUG"
AC_SUBST(CXXFLAGS)

# ---------------------------------------------------------------------
# Checks for header files.
# ---------------------------------------------------------------------

# ---------------------------------------------------------------------
# Checks for typedefs, structures, and compiler characteristics.
# ---------------------------------------------------------------------
AC_HEADER_STDBOOL
AC_C_CONST
AC_TYPE_SIZE_T

# ---------------------------------------------------------------------
# Checks for library functions.
# ---------------------------------------------------------------------
# AC_CHECK_FUNCS([abs min max pow sqrt])

# ---------------------------------------------------------------------
# Files configure will be responsible for.
# ---------------------------------------------------------------------
AC_CONFIG_FILES([Makefile])

AC_OUTPUT
