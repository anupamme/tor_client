with open("consensus.txt", 'r') as cons_file:
    with open("proced_cons.txt", 'w') as proc_file:
        Proc_router = ""
        Total_BW = 0

        for line in cons_file:
            in_line = line

            if in_line.startswith('r '):
                nick, key = in_line.split(" ")[1:3]
                
                Proc_router = nick + "," + key

            if in_line.startswith('s '):
                if "Guard" in in_line:
                    if "Exit" in in_line:
                        flag = "B"
                    else:
                        flag = "G"
                
                elif "Exit" in in_line:
                    flag = "E"
                
                Proc_router = Proc_router + "," + flag

            if in_line.startswith('w Bandwidth='):
                BW_line = in_line.split(" ")
                BW=''.join(BW_line[1:2])
                bandwidth_line = BW.split("=")
                bandwidth = ''.join(bandwidth_line[1:2])
                
                Proc_router = Proc_router + "," + bandwidth.strip() 
                Total_BW = Total_BW + int(bandwidth)
        
            if in_line.startswith('p '):
                proc_file.write(Proc_router + "\n")
                Proc_router = ""

        proc_file.write("Total BW=" + str(Total_BW) + "\n")

