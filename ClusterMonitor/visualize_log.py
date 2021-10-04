import argparse
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.backends.backend_pdf import PdfPages

p = argparse.ArgumentParser()
p.add_argument("-i", "--input", type=str, help="Specify the path to the created log file")
p.add_argument("-o", "--output", type=str,
               help="Specify path to the PDF file which will contain one plot for the CPU and and one plot for the Memory usage")
args = p.parse_args()

df = pd.read_csv(args.input, sep="\t")
df["datetime"] = pd.to_datetime(df["datetime"], format="%H:%M:%S %d/%m/%Y")
print(f"Reading in {len(df)} logged entries")
with PdfPages(args.output) as pdf:
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(df["datetime"], df["CPU [%]"], c="r", lw=0.5)
    ax.fill_between(df["datetime"], df["CPU [%]"], color="r", alpha=0.3)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M %d/%m"))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M %d/%m"))

    plt.xticks(rotation=45)
    plt.title("CPU Usage")
    plt.ylabel("CPU Usage [%]")
    plt.tight_layout()
    pdf.savefig()
    plt.close()

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.plot(df["datetime"], df["Memory [GB]"], c="b", lw=0.5)
    ax.fill_between(df["datetime"], df["Memory [GB]"], color="b", alpha=0.3)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M %d/%m"))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M %d/%m"))

    plt.xticks(rotation=45)
    plt.title("Memory usage")
    plt.ylabel("Memory [GB]")
    plt.tight_layout()
    pdf.savefig()
    plt.close()
