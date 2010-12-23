def get_num_events(simulations=None, parameter_set_number=None):
    ps = simulations.select_child_number(parameter_set_number)
    num_events = 0
    for simulation in ps.simulations:
        for filament in simulation.filaments:
            m = filament.measurements
            num_events += len(m.barbed_pyrene_atp_polymerization)
            num_events += len(m.barbed_pyrene_adppi_polymerization)
            num_events += len(m.barbed_pyrene_adp_polymerization)
            num_events += len(m.barbed_adp_polymerization)

            num_events += len(m.pointed_pyrene_atp_polymerization)
            num_events += len(m.pointed_pyrene_adppi_polymerization)
            num_events += len(m.pointed_pyrene_adp_polymerization)
            num_events += len(m.pointed_adp_polymerization)

            num_events += len(m.barbed_pyrene_atp_depolymerization)
            num_events += len(m.barbed_pyrene_adppi_depolymerization)
            num_events += len(m.barbed_pyrene_adp_depolymerization)
            num_events += len(m.barbed_adp_depolymerization)

            num_events += len(m.pointed_pyrene_atp_depolymerization)
            num_events += len(m.pointed_pyrene_adppi_depolymerization)
            num_events += len(m.pointed_pyrene_adp_depolymerization)
            num_events += len(m.pointed_adp_depolymerization)

            num_events += len(m.cleavage)
            num_events += len(m.release)
    return num_events
