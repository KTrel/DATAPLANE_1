from _pybgpstream import BGPStream, BGPRecord, BGPElem


target_prefs = []
with open('/home/motamedi/MEGA/workspace/ipy/Untitled Folder/DATAPLANE_1/atlas/anchor_prefix.txt', 'rb') as br:
    for l in br:
        target_prefs.append(l.strip())

# Create a new bgpstream instance and a reusable bgprecord instance
stream = BGPStream()
rec = BGPRecord()

for pref in target_prefs:
    print pref
    stream.add_filter('prefix', pref)
    # stream.add_filter('prefix','0.0.0.0/0')

    # Consider RIPE RRC 10 only
    stream.add_filter('record-type','updates')
    stream.add_filter('collector','rrc11')

    # Consider this time interval:
    # Sat Aug  1 08:20:11 UTC 2015
    # stream.add_interval_filter(1438417216,1438417216)
    # stream.add_interval_filter(1451606400,1454785264)
    stream.add_interval_filter(1454630400, 1454716800)

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
                print rec.project, rec.collector, rec.type, rec.time, rec.status,
                print elem.type, elem.peer_address, elem.peer_asn, elem.fields, elem.pref
                elem = rec.get_next_elem()

            # if cnt == 100:
            #     break
