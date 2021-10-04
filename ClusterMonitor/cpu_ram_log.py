import psutil
import math
import argparse
import time
import csv
import os
import datetime
import sys

p = argparse.ArgumentParser()
p.add_argument("-u", "--username", type=str, help="Specify the username for which we record CPU and Memory usage")
p.add_argument("-o", "--output", type=str,
               help="Path to the file where the CPU and Memory usage gets logged (in tsv format)")
p.add_argument("--interval", type=int,
               help="Specify the time (in seconds) over which the CPU and Memory usage gets averaged")
args = p.parse_args()


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5, 'e': 6}
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return (r)


try:
    print("Start data logging")
    while True:
        # record the average over X seconds, becuase cpu usage tends to fluctuate
        memory_avg = []
        cpu_avg = []
        for i in range(args.interval):
            memory = []
            cpu_usage = []
            for proc in psutil.process_iter():
                try:

                    process_info = proc.as_dict(attrs=["pid", "name", "username", "memory_info"])
                    if process_info["name"] == "sleep":
                        continue
                    # if process occupies more than 50 MB it is like not a background process. only look at these.
                    if process_info["username"] == args.username and proc.memory_info()[0] > 10e+2:
                        memory.append(proc.memory_info()[0])
                        cpu_usage.append(proc.cpu_percent(0.2))
                except:
                    pass

            memory_avg.append(sum(memory))
            cpu_avg.append(sum(cpu_usage))
            time.sleep(1)

        final_cpu = round(sum(cpu_avg) / len(cpu_avg), 4)
        final_memory = round(bytesto(sum(memory_avg) / len(memory_avg), "g"), 4)
        header = ['datetime', 'CPU [%]', 'Memory [GB]']
        with open(args.output, "a", newline="", encoding="UTF-8") as csv_file:
            writer = csv.writer(csv_file, delimiter='\t')
            # if file is empty create the header and add the data
            if os.path.getsize(args.output) == 0:
                writer.writerow(header)
                writer.writerow([datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"), final_cpu, final_memory])
            else:
                writer.writerow([datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"), final_cpu, final_memory])

except KeyboardInterrupt:
    print(f"Logging finished and saved to file {args.output}")
