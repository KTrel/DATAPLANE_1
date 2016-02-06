import requests
import arparse
import json
from sets import Set
import time
import datetime


class Probe:

    def __init__ (self, probe_id, asn, country_code, lat, lgt, ipv4='unknown', \
    nat="unknown", system="unknown", status="unknown", public="unknown", ipv6_works='no',
    rfc1918 = 'unknown', tagged='unknown', home='unknown', core='unknown', isp='unknown', \
    academic='unknown', start_time='unknown'):
        self.probe_id = probe_id
        self.asn = asn
        self.lat = lat
        self.lgt = lgt
        self.country_code = country_code
        self.ipv4 = ipv4
        self.nat = nat
        self.system = system
        self.status = status
        self.public = public
        self.ipv6_works = ipv6_works
        self.rfc1918 = rfc1918
        self.tagged = tagged
        self.home = home
        self.core = core
        self.isp = isp
        self.academic = academic
        self.start_time = start_time

        Probe.total_probes += 1
        if self.ipv4 is not None:
            Probe.total_ipv4 += 1
        if self.ipv6_works == "yes":
            Probe.total_ipv6 += 1
        if self.nat == "nat":
            Probe.total_nat += 1
        if self.nat == "no-nat":
            Probe.total_no_nat += 1
        if self.public:
            Probe.total_public += 1
        if self.system == "system-v1":
            Probe.total_v1 += 1
        if self.system == "system-v2":
            Probe.total_v2 += 1
        if self.system == "system-v3":
            Probe.total_v3 += 1
        if country_code not in Probe.total_countries:
            Probe.total_countries[country_code] = 1
        else:
            Probe.total_countries[country_code] += 1

    def __hash__(self):    
        return hash(self.probe_id)

    def __repr__(self):
        return str(self.probe_id)+'\t'+str(self.asn)+'\t'+str(self.country_code)+'\t' \
            +str(self.lat)+'\t'+str(self.lgt)+'\t'+str(self.ipv4)+"\t"+self.nat+"\t" \
            +self.system+'\t'+str(self.status)+'\t'+str(self.public)+'\t'+str(self.ipv6_works)+'\t' \
            +str(self.rfc1918)+'\t'+str(self.tagged)+'\t'+str(self.home)+'\t' \
            +str(self.core)+'\t'+str(self.isp)+'\t'+str(self.academic)
    
    @staticmethod
    def header ():
        return '#ID\tASN\tCOUNTRY\tLAT\t\tLGT\tIPV4\t\tNAT\tSYSTEM\t\tSTATUS\tPUBLIC\tIVP6\tRFC1918\tTAGGED\tHOME\tCORE\tISP\tACADEMIC'



def get_probes():
    r = requests.get('https://atlas.ripe.net/api/v1/probe-archive/')

    print r.status_code
    print r.headers

    probes_list = {}

    data = json.loads(r.text)

    for p in data["objects"]:
        nat = "unknown"
        system = "unknown"

        # Check if behind a NAT
        if "nat" in p["tags"]:
            nat = "nat"
        elif "no-nat" in p["tags"]:
            nat = "no-nat"

        # Check the system
        if "system-v1" in p["tags"]:
            system = "system-v1"
        elif "system-v2" in p["tags"]:
            system = "system-v2"
        elif "system-v3" in p["tags"]:
            system = "system-v3"
        elif "system-v4" in p["tags"]:
            system = "system-v4"

        # rfc1918
        if "system-ipv4-rfc1918" in p["tags"]:
            rfc1918 = True
        else:
            rfc1918 = False

        # Tagged by user
        tagged_by_users = False
        for t in p["tags"]:                
            if "system" not in t and t != 'nat' and t != 'no-nat':
                tagged_by_users = True
                break

        if tagged_by_users == False:
            fd = open('tmp', 'a+')
            fd.write(nat+' ')
            for i in p["tags"]:
                fd.write(str(i)+' ')

            fd.write('\n')
            fd.close()

        # Probe location
        home = False
        if "home" in p["tags"]:
            home = True
        core = False
        if "core" in p["tags"]:
            core = True
        isp = False
        if "isp" in p["tags"]:
            isp = True
        academic = False
        if "academic" in p["tags"]:
            academic = True
                

        ipv6_works = "no"
        if "system-ipv6-works" in p["tags"]:
            ipv6_works = "yes"

        if p["status"] == 1:
            probe = Probe(int(p["id"]), p['asn_v4'], \
            p['country_code'], p['latitude'], p['longitude'], \
            p['address_v4'], nat, system, p["status"], p['is_public'], ipv6_works, \
            rfc1918, tagged_by_users, home, core, isp, academic)
            probes_list[int(p["id"])] = probe

    return probes_list


if __name__ == '__main__':

    parser = argparse.ArgumentParser("Given a list of ASes or countries, this scripts \
    collects all the probes that are in this set of ASes/countries.")
    parser.add_argument("infile", type=str, help="File with a list of ASes")
    parser.add_argument("outfile", type=str, help="Outfile")
    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile

    fd_res = open(outfile, 'w', 1)
    fd_res.write(Probe.header()+'\n')

    fd = open(infile, 'r')
    for line in fd.readlines():

        v = line.split()
        country = v[0]

        #asn = line.rstrip()
        probes_list = get_country_probes (country)
    
        for probe in probes_list:
            fd_res.write(str(probe)+'\n')

    fd.close()
    fd_res.close()
