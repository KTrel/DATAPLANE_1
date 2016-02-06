from optparse import OptionParser
from _pybgpstream import BGPStream, BGPRecord, BGPElem


def getopts():
    parser = OptionParser()
    parser.add_option('-i', dest='in_folder', type=str,
                      default='', help='use raw counts')
    parser.add_option('-o', dest='out_file', type=str,
                      default="error.txt", help='use raw counts')
    parser.add_option('-s', dest='start_time', type=int,
                      default=1454630400, help='start time')
    parser.add_option('-e', dest='end_time', type=int,
                      default=1454716800, help='end time')

    # parser.add_option('--file', dest='fileName', type=str,
    #   default="profiles_10k.txt", help='use expected counts')
    return parser.parse_args()


def main():
    (options, args) = getopts()
    start = options.start_time
    end = options.end_time

    target_prefs = []
    with open('./../../atlas/anchor_prefix.txt', 'rb') as br:
        for l in br:
            target_prefs.append(l.strip())

    # Create a new bgpstream instance and a reusable bgprecord instance
    stream = BGPStream()
    rec = BGPRecord()

    with open('./data/stream_{0}'.format(start), 'wb') as bw:
        for pref in target_prefs:
            print pref
            stream.add_filter('prefix', pref)
            # stream.add_filter('prefix','0.0.0.0/0')

            # Consider RIPE RRC 10 only
            stream.add_filter('record-type', 'updates')
            stream.add_filter('collector', 'rrc00')

            # Consider this time interval:
            # Sat Aug  1 08:20:11 UTC 2015
            # stream.add_interval_filter(1438417216,1438417216)
            # stream.add_interval_filter(1451606400,1454785264
            stream.add_interval_filter(start, end)

            # Start the stream
            stream.start()

            # Get next record
            cnt = 0

            while stream.get_next_record(rec):
                # Print the record information only if it is not a valid record
                if rec.status != "valid":
                    pass
                    # print '*', rec.project, rec.collector, rec.type, rec.time, rec.status
                else:
                    cnt += 1
                    elem = rec.get_next_elem()
                    while elem:
                        if elem.type == 'S':
                            continue
                        # Print record and elem information
                        # print rec.project, rec.collector, rec.type, rec.time, rec.status,
                        # print elem.type, elem.peer_address, elem.peer_asn, elem.fields, elem.pref
                        bw.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}\t{8}\t{9}\n'.format(
                            rec.project, rec.collector, rec.type, rec.time, rec.status,
                            elem.type, elem.fields['prefix'], elem.peer_address, elem.peer_asn, elem.fields))
                        bw.flush()
                        elem = rec.get_next_elem()

                    # if cnt == 100:
                    #     break
    print 'Successful termination; Start time: {0}'.format(start)

if __name__ == '__main__':
    main()

