import radix
import editdistance


class StateMatcher(object):
    def __init__(self):
        self.prefix_radix = radix.Radix()
        ifp = '../DATAPLANE_1/atlas/anchor_prefix.txt'
        br = open(ifp, 'rb')
        for l in br:
            self.prefix_radix.add(l.strip())

        self.trace_state = {}
        path = '../DATAPLANE_1/aspath-traceroutes'
        br = open(path, 'rb')
        for l in br:
            tokens = l.split()
            pref = self.prefix_radix.search_best(tokens[0])
            asn = tokens[1]
            as_path = ' '.join(tokens[2:])
            if pref not in self.trace_state:
                self.trace_state[pref] = {}
            self.trace_state[pref][asn] = as_path

    def match_states(self):
        pass


if __name__ == '__main__':
    sm = StateMatcher()
    sm.match_states()
