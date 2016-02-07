from sets import Set

class Rib:

    def __init__(self, rib_fd, up_fd):
        self.rib = {}
        self.rib_fd = rib_fd
        self.up_fd = up_fd
        self.is_flushed = False

    def add_to_rib(self, collector, peer_ip, prefix, ts, as_path, isrib=True):
        print prefix
        as_path = self.list_to_string(as_path)
        if collector not in self.rib:
            self.rib[collector] = {}
        if peer_ip not in self.rib[collector]:
            self.rib[collector][peer_ip] = {}
        if not isrib:
            if self.rib[collector][peer_ip][prefix] != as_path:
                self.up_fd.write(str(collector)+'\t'+str(peer_ip)+'\t'+str(ts)+'\t'+str(prefix)+'\t'+str(self.rib[collector][peer_ip][prefix])+'\t'+str(as_path)+'\n')
        self.rib[collector][peer_ip][prefix] = as_path

    def list_to_string(self, l):
        res_str = ''
        for i in l:
            res_str += str(i)+' '
        return res_str[:-1]

    def flush(self):
        if not self.is_flushed:
            self.is_flushed = True
            self.rib_fd.write(str(self))

    def __str__(self):
        res_string = ''
        for c in self.rib:
            for peer_ip in self.rib[c]:
                for prefix, as_path in self.rib[c][peer_ip].items():
                    res_string += str(c)+'\t'+str(peer_ip)+'\t'+str(prefix)+'\t'+str(as_path)+'\n'

    
