class Simulation(object):
    def __init__(self, poly, depoly, hydro, record, end):
        self.poly   = poly
        self.depoly = depoly
        self.hydro  = hydro
        self.record = record
        self.end    = end

    def run(self, nucleus_size):
        # Initialize strand
        strand = self.hydro.create_strand(nucleus_size)

        # Initialize data storage dictionary
#        data = dict( (key, []) for key in self.record.keys() )

        poly_count   = 0
        depoly_count = 0
        hydro_stats  = None

        [e.reset() for e in self.end]
#        while not any(e(**locals()) for e in self.end):
        while not any(e(None) for e in self.end):
            print strand
            poly_count += self.poly(strand)
            try:
                depoly_count += self.depoly(strand)
            except IndexError:
                break
            hydro_stats = self.hydro(strand, hydro_stats)

            # Collect and store data
#            for key, f in self.record.items():
#                result = f(**locals())
#                if result is not None:
#                    data[key].append(result)
#
#        return data
