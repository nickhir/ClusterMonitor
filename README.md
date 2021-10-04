# ClusterMonitor
A very simple python script which monitors and records the CPU and RAM consumption of submitted cluster jobs.

## Usage
To start recording use the `cpu_ram_log.py` script. This script requires 3 arguments:
- `-u` which corresponds to your username.
- `-o` which specifies the output file (in tsv format)
- `--interval` which specifies the time (in seconds) over which the CPU and RAM usage gets averaged

Example:
```python
python cpu_ram_log.py -u nickhir -o cpu_ram.log --interval 5
```
The script can simply be included in your cluster job submittion like this:
```bash
#!/bin/bash
#SBATCH --job-name=Example_run

sambamba sort -t 20 some_bam.bam &
MainScript=$!
python cpu_ram_log.py -u nickhir -o cpu_ram.log --interval 5 &
wait $MainScript
pkill -P $$
```


Afterwards the resulting log file can be plotted (for that `matplotlib` is needed).
For that use the `visualize_log.py` script which needs 2 arguments: 
- `-i` which specifies the path to the log file which was created with `cpu_ram_log.py`
- `-o` which specifies the path to the resulting PDF which contains a plot for the CPU and RAM usage.


Example:
```python
python visualize_log.py -i cpu_ram.log -o cpu_ram_visualization.pdf
```

The resulting plots will look somewhat like this:
![exampleImage](ClusterMonitor/example/example_image.png)
