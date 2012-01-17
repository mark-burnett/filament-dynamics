AUTOMAKE_OPTIONS = subdir-objects

INCLUDES = -Iinclude -Itests/include

# --- Libraries ---
lib_LTLIBRARIES = stochastic.la
stochastic_la_SOURCES = src/filaments/simple_filament.cpp\
						src/transitions/random_hydrolysis.cpp\
						src/transitions/vectorial_hydrolysis.cpp\
						src/transitions/depolymerization.cpp\
						src/transitions/polymerization.cpp\
						src/simulation_strategy.cpp\
						src/measurements/filament_length.cpp\
						src/measurements/state_count.cpp\
						src/random_seed.cpp\
						src/filaments/cached_filament.cpp\
						src/filaments/segmented_filament.cpp

stochastic_la_LDFLAGS = -module

# --- Tests ---
check_PROGRAMS = runtests
runtests_SOURCES = tests/test_main.cpp\
			   tests/filaments/test_simple_filament.cpp\
			   tests/filaments/test_cached_filament.cpp\
			   tests/filaments/test_segmented_filament.cpp\
			   tests/transitions/test_random_hydrolysis.cpp\
			   tests/transitions/test_vectorial_hydrolysis.cpp\
			   tests/transitions/test_depolymerization.cpp\
			   tests/transitions/test_polymerization.cpp\
			   tests/test_concentrations.cpp\
			   tests/test_simulation_strategy.cpp\
			   tests/measurements/test_filament_length.cpp\
			   tests/measurements/test_state_count.cpp\
			   tests/test_end_conditions.cpp\
			   tests/test_old_integration.cpp

runtests_LDADD   = stochastic.la

LIBS = $(GTEST_LIBS)

TESTS = runtests

# --- Cleanup ---
MAINTAINERCLEANFILES = configure config.log config.status\
					   aclocal.m4 autom4te.cache Makefile.in\
					   config/config.guess config/config.sub config/depcomp\
					   config/install-sh config/ltmain.sh config/missing
