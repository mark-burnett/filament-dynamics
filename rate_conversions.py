def scale_rates( rates, dt ):
    """
    Scales the given rates by dt.
    """
    result = {}
    for instate, out in rates.iteritems():
        if out:
            result[instate] = (out[0] * dt, out[1])
        else:
            result[instate] = None
    return result

def scale_multiple_rates( rates, dt ):
    """
    Scales the given rates by dt.

    Designed to work for situations where there are multiple available
        final states for a given intial state.
    """
    result = {}
    for instate, in_rates in rates.iteritems():
        in_rates_converted = []
        if in_rates:
            ptot = 0
            for p, outstate in in_rates:
                ptot += p * dt
                in_rates_converted.append( (ptot, outstate) )
        result[instate] = in_rates_converted
    return result
