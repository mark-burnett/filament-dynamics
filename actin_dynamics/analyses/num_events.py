def get_num_events(simulations=None, parameter_set_number=None):
    ps = simulations.select_child_number(parameter_set_number)
    num_events = 0
    for simulation in ps.simulations:
        for filament in simulation.filaments:
            m = filament.measurements
            num_events += len(m.barbed_pyrene_atp_polymerization) - 1
            num_events += len(m.barbed_pyrene_adppi_polymerization) - 1
            num_events += len(m.barbed_pyrene_adp_polymerization) - 1
            num_events += len(m.barbed_adp_polymerization) - 1

            num_events += len(m.pointed_pyrene_atp_polymerization) - 1
            num_events += len(m.pointed_pyrene_adppi_polymerization) - 1
            num_events += len(m.pointed_pyrene_adp_polymerization) - 1
            num_events += len(m.pointed_adp_polymerization) - 1

            num_events += len(m.barbed_pyrene_atp_depolymerization) - 1
            num_events += len(m.barbed_pyrene_adppi_depolymerization) - 1
            num_events += len(m.barbed_pyrene_adp_depolymerization) - 1
            num_events += len(m.barbed_adp_depolymerization) - 1

            num_events += len(m.pointed_pyrene_atp_depolymerization) - 1
            num_events += len(m.pointed_pyrene_adppi_depolymerization) - 1
            num_events += len(m.pointed_pyrene_adp_depolymerization) - 1
            num_events += len(m.pointed_adp_depolymerization) - 1

            num_events += len(m.cleavage) - 1
            num_events += len(m.release) - 1
    return num_events
