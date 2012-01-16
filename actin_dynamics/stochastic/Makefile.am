AUTOMAKE_OPTIONS = subdir-objects

INCLUDES = -Iinclude -Itests/include

# --- Libraries ---
lib_LTLIBRARIES      = stochastic.la
stochastic_la_SOURCES = src/filaments/simple_filament.cpp\
						src/transitions/random_hydrolysis.cpp\
						src/simulation_strategy.cpp\
						src/measurements/filament_length.cpp\
						src/measurements/state_count.cpp
stochastic_la_LDFLAGS = -module

# --- Tests ---
check_PROGRAMS   = test
test_SOURCES = tests/test_main.cpp\
			   tests/filaments/test_simple_filament.cpp\
			   tests/transitions/test_random_hydrolysis.cpp\
			   tests/test_concentrations.cpp\
			   tests/test_simulation_strategy.cpp\
			   tests/measurements/test_filament_length.cpp\
			   tests/test_end_conditions.cpp

test_LDADD   = stochastic.la

LIBS = $(GTEST_LIBS)

TESTS = test

# --- Cleanup ---
MAINTAINERCLEANFILES = configure config.log config.status\
					   aclocal.m4 autom4te.cache Makefile.in\
					   config/config.guess config/config.sub config/depcomp\
					   config/install-sh config/ltmain.sh config/missing
