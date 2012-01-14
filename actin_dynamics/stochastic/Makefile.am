AUTOMAKE_OPTIONS = subdir-objects

INCLUDES = -Iinclude -Itests/include

# --- Libraries ---
lib_LTLIBRARIES      = stochastic.la
stochastic_la_SOURCES = src/state/simple_filament.cpp\
						src/transitions/random_hydrolysis.cpp
stochastic_la_LDFLAGS = -module

# --- Tests ---
check_PROGRAMS   = test
test_SOURCES = tests/test_main.cpp\
			   tests/state/test_simple_filament.cpp\
			   tests/transitions/test_random_hydrolysis.cpp

test_LDADD   = stochastic.la

LIBS = $(GTEST_LIBS)

TESTS = test

# --- Cleanup ---
MAINTAINERCLEANFILES = configure config.log config.status\
					   aclocal.m4 autom4te.cache Makefile.in\
					   config/config.guess config/config.sub config/depcomp\
					   config/install-sh config/ltmain.sh config/missing
