/*    Copyright (C) 2012 Mark Burnett
 *
 *    This program is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

%module stochastic
%include <std_shared_ptr.i>

%{
#include "simulation_strategy.h"

#include "state.h"
#include "random_seed.h"

#include "filaments/filament.h"
#include "filaments/default_filament.h"
#include "filaments/simple_filament.h"
#include "filaments/cached_filament.h"
#include "filaments/segmented_filament.h"

#include "concentrations/concentration.h"
#include "concentrations/fixed_concentration.h"
#include "concentrations/fixed_reagent.h"

#include "end_conditions/end_condition.h"
#include "end_conditions/duration.h"
#include "end_conditions/event_count.h"

#include "measurements/measurement.h"
#include "measurements/filament_length.h"
#include "measurements/state_count.h"

#include "transitions/transition.h"
#include "transitions/depolymerization.h"
#include "transitions/polymerization.h"
#include "transitions/cooperative_hydrolysis.h"
#include "transitions/random_hydrolysis.h"
#include "transitions/vectorial_hydrolysis.h"
%}

/*
%template(transition_ptr_t) boost::shared_ptr<Transition>;
%template(be_polymerization_ptr_t) boost::shared_ptr<BarbedEndPolymerization>;
%template(random_hydrolysis_ptr_t) boost::shared_ptr<RandomHydrolysis>;

%template(concentration_ptr_t) boost::shared_ptr<Concentration>;
%template(fixed_concentration_ptr_t) boost::shared_ptr<FixedConcentration>;
*/

%include "simulation_strategy.h"

%include "state.h"
%include "random_seed.h"

%include "filaments/filament.h"
%include "filaments/default_filament.h"
%include "filaments/simple_filament.h"
%include "filaments/cached_filament.h"
%include "filaments/segmented_filament.h"

%include "concentrations/concentration.h"
%include "concentrations/fixed_concentration.h"
%include "concentrations/fixed_reagent.h"

%include "end_conditions/end_condition.h"
%include "end_conditions/duration.h"
%include "end_conditions/event_count.h"

%include "measurements/measurement.h"
%include "measurements/filament_length.h"
%include "measurements/state_count.h"

%include "transitions/transition.h"
%include "transitions/depolymerization.h"
%include "transitions/polymerization.h"
%include "transitions/cooperative_hydrolysis.h"
%include "transitions/random_hydrolysis.h"
%include "transitions/vectorial_hydrolysis.h"

/*
SWIG_SHARED_PTR(Concentration, Concentration)
SWIG_SHARED_PTR_DERIVED(FixedConcentration, Concentration, FixedConcentration)

SWIG_SHARED_PTR(Transition, Transition)
SWIG_SHARED_PTR_DERIVED(BarbedEndPolymerization, Transition, BarbedEndPolymerization)
SWIG_SHARED_PTR_DERIVED(RandomHydrolysis, Transition, RandomHydrolysis)
*/
