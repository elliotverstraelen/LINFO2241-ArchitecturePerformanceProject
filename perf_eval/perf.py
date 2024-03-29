#!/usr/bin/env python
import os
import numpy as np
import subprocess
import time
import re
from datetime import datetime
from pathlib import Path



SERVER_IP = "10.0.1.3"
SERVER_PORT = "2241"
DURATION = 5 # seconds
#PARENT_PATH = Path().parent.absolute()
PARENT_PATH = Path().resolve().parent

def init(FILENAME_THROUGHPUT, FILENAME_RESPONSE_TIME):
    # Create the files in which the results will be stored
    if not os.path.exists('data'):
        os.makedirs('data')

    with open(FILENAME_THROUGHPUT, 'w') as file:
        file.write("fsize,ksize,request_rate,thread,throughput\n")
    
    with open(FILENAME_RESPONSE_TIME, 'w') as file:
        file.write("fsize,ksize,request_rate,thread,response_time\n")
    
    subprocess.run(['make', 'clean'], cwd=PARENT_PATH)
    subprocess.run(['make', 'all'], cwd=PARENT_PATH)


def script_server(thread, fsize):
    process = subprocess.Popen(['ssh', 'server', 'ulimit', '-n', '8192', ';','/root/LINFO2241-ArchitecturePerformanceProject/./server', '-j', str(thread), '-s', str(fsize), '-p', SERVER_PORT], stdout=subprocess.PIPE, cwd=PARENT_PATH)
    return process


def script_client(ksize, request_rate):
    process = subprocess.Popen(['./client', '-k', str(ksize), '-r', str(request_rate), '-t', str(DURATION), SERVER_IP+':'+SERVER_PORT], stdout=subprocess.PIPE, cwd=PARENT_PATH)
    return process

def start_test(fsizes:list, ksizes:list, req_rates:list, threads:list, nb_iteration):
    DAY_TIME = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    FILENAME_THROUGHPUT = "data/"+DAY_TIME+"_throughput.csv"
    FILENAME_RESPONSE_TIME = "data/"+DAY_TIME+"_response_time.csv"
    init(FILENAME_THROUGHPUT,FILENAME_RESPONSE_TIME)

    it = 1

    for fsize in fsizes:
        for ksize in ksizes:
            for request_rate in req_rates:
                for thread in threads:
                    throughput_bytes = np.empty(nb_iteration, dtype=float)
                    throughput_packets = np.empty(nb_iteration, dtype=float)
                    response_time = np.empty(nb_iteration, dtype=float)
                    for i in range(nb_iteration):
                        server_proc = script_server(thread, fsize)
                        time.sleep(4)
                        client_proc = script_client(ksize, request_rate)

                        server_output = server_proc.communicate()[0].decode()
                        client_output = client_proc.communicate()[0].decode()
                        
                        print(it)
                        it += 1

                        
                        throughput_bytes[i] = float(re.search(r"mean\sthroughput\sbytes\s(\d+.?\d*)", client_output).group(1))
                        throughput_packets[i] = float(re.search(r"mean\sthroughput\spackets\s(\d+.?\d*)", client_output).group(1))
                        response_time[i] = float(re.search(r"mean\sresponse\stime\s(\d+.?\d*)", client_output).group(1))


                        # Save results to files
                        with open(FILENAME_THROUGHPUT, 'a') as file:
                            file.write("{0},{1},{2},{3},{4}\n".format(fsize, ksize, request_rate, thread, throughput_packets[i]))
                        with open(FILENAME_RESPONSE_TIME, 'a') as file:
                            file.write("{0},{1},{2},{3},{4}\n".format(fsize, ksize, request_rate, thread, response_time[i]))


if __name__ == "__main__":
    
    
    #2K easy
    #start_test([128,256],[32,64],[350,700],[2,4], 3)

    #2K hard
    #start_test([512,256],[256,128],[600,300],[2,4], 3)

    #Vary thread only
    #start_test([512],[256],[100],[1,2,4,8],3) # OK tested on intel

    #Vary fsize only
    #start_test([64,128,256,512],[32],[100],[1],3) # OK but queuing at 512, bof bof
    #start_test([64,128,256,512],[32],[50],[1],3) # maybe better at 50 but small for 64
    start_test([64,128,256,512],[32],[1000],[1],3)
    #Vary ksize only
    #start_test([256],[8,16,32,64,128],[100],[1],3) # OK
    start_test([256],[8,16,32,64,128],[500],[1],3)

    #Vary requests only
    #start_test([256],[32],[200, 400, 600, 800],[1],3) # OK, +/- doubling response time but at 800 big jump due to queuing

    #Vary fsize-ksize only
    #start_test([64,128,256,512],[16,32],[50],[1],5)

    
                        
                    
    
    
    
                    