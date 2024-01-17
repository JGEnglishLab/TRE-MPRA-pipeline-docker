#!/usr/bin/python3
import argparse
from argparse import RawTextHelpFormatter
import os
import help_txt as ht

cwd = os.getcwd()

CONTAINER_ID = "samhimes92/tmp"

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter, description="Runs Docker container"
)

parser.add_argument("-ro", required=True, help=ht.ro())
parser.add_argument("-f", required=True, help=ht.f())
parser.add_argument("-t", required=True, help=ht.t())
parser.add_argument("-r", required=False, help=ht.r_empirical())
parser.add_argument("-dt", required=False, help=ht.dt())
parser.add_argument("-s", required=False, help=ht.s())
parser.add_argument("-sr", required=False, help=ht.sr())
parser.add_argument("-d", required=False, help=ht.d())
parser.add_argument("-i", required=False, help=ht.i())
parser.add_argument("-n", required=False, help=ht.n())
parser.add_argument("--sudo", action="store_true", help=ht.sudo())


args = parser.parse_args()
run_output = vars(args)["ro"]
dir_name = vars(args)["r"]
fastq_path = vars(args)["f"]
treatment_tsv_path = vars(args)["t"]
dna_tsv_path = vars(args)["dt"]
pattern = vars(args)["sr"]
dna_path = vars(args)["d"]
ignore_path = vars(args)["i"]
spike_path = vars(args)["s"]
threads = vars(args)["n"]

if args.sudo:
    sudo_option = "sudo"
else:
    sudo_option = ""

if threads:
    if not threads.isnumeric():
        print("Number of threads (-n --n_workers) must be numeric")
        exit()
    else:
        thread_flag = f"-n {threads}"
else:
    thread_flag = ""


# Checks if they added a dir name
if dir_name:
    dir_name = f"-r {dir_name}"
else:
    dir_name = ""

# Check path to fastq files
if not os.path.exists(fastq_path):
    print("path to fastq_path (-f --path_to_fq) doesn't exist")
    exit()
else:
    os.chdir(fastq_path)
    fastq_path = os.getcwd()
    os.chdir(cwd)

# Check path to run output
if not os.path.exists(run_output):
    print("path to run output (-ro --run_output) doesn't exist")
    exit()
else:
    os.chdir(run_output)
    emp_output = os.getcwd()
    os.chdir(cwd)

# Check path to treatement TSV
if not os.path.exists(treatment_tsv_path):
    print("path to treatment tsv (-t --path_to_treatment_tsv) doesn't exist")
    exit()
else:
    treatment_tsv_path = os.path.abspath(treatment_tsv_path)

# Check optional flags

# Check path to dna fastq files
if dna_path:
    if not os.path.exists(dna_path):
        print("path to dna fastqs (-d --path_to_DNA_fastq) doesn't exist")
        exit()
    else:
        os.chdir(dna_path)
        dna_path = os.getcwd()
        os.chdir(cwd)
        dna_fq_mount = f"-v {dna_path}:/mydata/dna_fq_files"
        dna_fq_flag = "-d /mydata/dna_fq_files"

else:
    dna_fq_mount = ""
    dna_fq_flag = ""


# Check dna tsv path
if dna_tsv_path:
    if not os.path.exists(dna_tsv_path):
        print("path to DNA tsv map (-dt --path_to_dna_tsv) doesn't exist")
        exit()
    else:
        dna_tsv_path = os.path.abspath(dna_tsv_path)
        dna_tsv_mount = f"-v {dna_tsv_path}:/mydata/dna_map.tsv"
        dna_tsv_flag = "-dt /mydata/dna_map.tsv"
else:
    dna_tsv_mount = ""
    dna_tsv_flag = ""

# Check spike in path
if spike_path:
    if not os.path.exists(spike_path):
        print("path to spike in file (-s --path_to_spikein_file) doesn't exist")
        exit()
    else:
        spike_path = os.path.abspath(spike_path)
        spike_mount = f"-v {spike_path}:/mydata/spike.txt"
        spike_flag = "-s /mydata/spike.txt"
else:
    spike_mount = ""
    spike_flag = ""

# Check ignore_file path
if ignore_path:
    if not os.path.exists(ignore_path):
        print("path to ignore file (-i) doesn't exist")
        exit()
    else:
        ignore_path = os.path.abspath(ignore_path)
        ignore_mount = f"-v {ignore_path}:/mydata/ignore.txt"
        ignore_flag = "-i /mydata/ignore.txt"
else:
    ignore_mount = ""
    ignore_flag = ""

if pattern:
    pattern_flag = f"-sr {pattern}"
else:
    pattern_flag = ""

command = (
    f"{sudo_option} docker run -i -v "
    f"{emp_output}:/app/runs -v {fastq_path}:/mydata/fq_files -v {treatment_tsv_path}:/mydata/treatements.tsv "
    f"{dna_tsv_mount} {spike_mount} {ignore_mount} {dna_fq_mount} "
    f"{CONTAINER_ID} TMP_empirical.py -f /mydata/fq_files -t /mydata/treatements.tsv "
    f"{dna_tsv_flag} {spike_flag} {ignore_flag} {dna_fq_flag} {pattern_flag} {dir_name} {thread_flag}"
)
print(command)
os.system(command)

print("Finished")
print("Removing Docker Image")
remove_command = f'docker rm $(docker stop $(docker ps -a -q --filter ancestor={CONTAINER_ID} --format="{{{{.ID}}}}")) '
os.system(remove_command)

