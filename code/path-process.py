import pprint as pp

stats_two = 0
stats_four = 0
stats_six = 0

with open("tor_paths.csv", 'r') as path_file:
    with open("propaths.txt", 'w') as proc_file:
        path_dict = dict()

        for line in path_file:
            path = " "
            if not(line.startswith("GId,GName")):
                proc_line = line.strip().split(",")
                if len(proc_line) == 2:
                    stats_two += 1
                elif len(proc_line) == 4:
                    stats_four += 1
                else:
                    stats_six += 1
                    
                    gid = proc_line[0:1]
                    eid = proc_line[4:5]
                    path = gid + eid
                    str_path = '||'.join(path)
                    
                    path_dict[str_path] = path_dict.get(str_path, 0) + 1

            path = ""
        proc_file.write("Circuits of length two=%s, four=%s, and six=%s" % (stats_two, stats_four, stats_six))
        for key, value in path_dict.items():
            proc_file.write('%s:%s\n' % (key, value))
