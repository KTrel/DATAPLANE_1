import radix
import editdistance
import networkx as nx
import matplotlib.pyplot as plt


class StateMatcher(object):
    def __init__(self):
        self.trace_bgp_math_graph = nx.DiGraph()
        self.prefix_radix = radix.Radix()
        ifp = '../../atlas/anchor_prefix.txt'
        br = open(ifp, 'rb')
        for l in br:
            self.prefix_radix.add(l.strip())

        self.trace_state = {}
        path = '../../aspath-traceroutes'
        br = open(path, 'rb')
        for l in br:
            tokens = l.split()
            pref = self.prefix_radix.search_best(tokens[0])
            try:
                pref = pref.prefix
            except AttributeError:
                print l
                raw_input('???')
            asn = tokens[1]
            as_path = ' '.join(tokens[2:])
            if pref not in self.trace_state:
                self.trace_state[pref] = {}
            self.trace_state[pref][asn] = as_path

        self.bgp_state = {}
        path = '../../aspath-traceroutes'
        br = open(path, 'rb')
        for l in br:
            tokens = l.split()
            pref = self.prefix_radix.search_best(tokens[0])
            pref = pref.prefix
            asn = tokens[1]
            as_path = ' '.join(tokens[2:])
            if pref not in self.bgp_state:
                self.bgp_state[pref] = {}
            self.bgp_state[pref][asn] = as_path

        # print self.trace_state
        # print self.bgp_state

    def match_states(self):
        for pref_d, vp_aspth_dict_d in self.trace_state.iteritems():
            print pref_d
            best_match_val = 0
            best_match_lst = []
            # raw_input('...')
            for vp_d, aspath_d in vp_aspth_dict_d.iteritems():
                # print vp_d, ':', aspath_d

                vp_aspth_dict_c = self.bgp_state[pref_d]
                for vp_c, aspath_c in vp_aspth_dict_c.iteritems():
                    dist = editdistance.eval(aspath_c.split(), aspath_d.split())
                    if dist>best_match_val:
                        best_match_val = dist
                        best_match_lst = [vp_c]
                    elif dist == best_match_val:
                        best_match_lst.append(vp_c)
                    # print vp_d, '%', vp_c, '=>', editdistance.eval(aspath_c.split(), aspath_d.split())
                # print vp_d, '%', best_match_val, '=>', best_match_lst
                for vp_c in best_match_lst:
                    self.trace_bgp_math_graph.add_edge('d_{0}_{1}'.format(vp_d, pref_d), 'd_{0}_{1}'.format(vp_c, pref_d))

    def show_graph(self):
        print len(self.trace_bgp_math_graph.nodes())
        print len(self.trace_bgp_math_graph.edges())
        nx.draw_spectral(self.trace_bgp_math_graph, node_size=10, alpha=0.5, with_labels=False)
        plt.savefig('matching_graph', bbox_inches='tight', format='jpg', dpi=320)
        # plt.show()

if __name__ == '__main__':
    sm = StateMatcher()
    sm.match_states()
    sm.show_graph()
