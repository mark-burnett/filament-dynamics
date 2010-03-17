import multiprocessing

def pool_sim(simulation, argument, num_runs=None, num_processes=None):
    """
    Uses multiprocessing to perform multiple simulations at once.
    'argument' is either a single strand used for num_runs simulations
        or it is a sequence of initial strands each used for one simulation.
    'num_runs' is the number of simulations to perform, only use this if
        'argument' is a single strand.
    'num_processes' determines the size of the multiprocessing pool
    """
    pool = None
    if num_processes:
        pool = multiprocessing.Pool(num_processes)
    else:
        pool = multiprocessing.Pool()

    try:
        results = None
        if num_runs:
            results = [pool.apply_async(simulation, (argument,))
                           for i in xrange(num_runs)]
            # Add a crazy long timeout (ms) to work around a python bug.
            # This lets us use CTRL-C to stop the program.
            results = [r.get(999999999999) for r in results]
        else:
            results = pool.map_async(simulation, argument)
            # Add a crazy long timeout (ms) to work around a python bug.
            # This lets us use CTRL-C to stop the program.
            results = results.get(999999999999)

        # Multiprocessing cleanup
        pool.close()
        pool.join()
    except KeyboardInterrupt:
        # Handle CTRL-C
        pool.terminate()
        raise

    return results
