#!/usr/bin/python3
import argparse
from argparse import RawTextHelpFormatter
import os
import help_txt as ht

cwd = os.getcwd()

parser = argparse.ArgumentParser(
    formatter_class=RawTextHelpFormatter, description="Runs Docker container"
)

parser.add_argument("-po", required=False, default = "./", help=ht.po())
parser.add_argument("-mo", required=False, default = "./", help=ht.mo())
parser.add_argument("-r", required=True, help=ht.r_comparative_docker())  # The directory that has all the runs
parser.add_argument("-p", required=False, help=ht.p())
parser.add_argument("-m", required=False, help=ht.m())
parser.add_argument("-n", required=False, help=ht.n())
parser.add_argument("--sudo", action="store_true", help=ht.sudo())


args = parser.parse_args()
multi_output = vars(args)["mo"]
pairwise_output = vars(args)["po"]
runs_dir = vars(args)["r"]
pairwise_comps = vars(args)["p"]
multi_comps = vars(args)["m"]
threads = vars(args)["n"]

def check_output_dir(dir, type):
    if not os.path.exists(dir):
        if type == "pairwise":
            print("Path to pairwise output (-po --pairwise_output) doesn't exist")
        elif type == "multi":
            print("Path to multi output (-mo --multi_output) doesn't exist")
        exit()
    else:
        os.chdir(dir)
        abs_dir_path = os.getcwd()
        os.chdir(cwd)
        return abs_dir_path


if args.sudo:
    sudo_option = "sudo"
else:
    sudo_option = ""


if pairwise_comps:
    if not os.path.exists(pairwise_comps):
        print("Path to pairwise comparisons TSV (-p --pairwise_tsv) doesn't exist")
        exit()
    else:
        pairwise_comps = os.path.abspath(pairwise_comps)
        pairwise_tsv_mount = f"-v {pairwise_comps}:/mydata/pairwise_comps.tsv"
        pairwise_tsv_flag = "-p /mydata/pairwise_comps.tsv"
else:
    pairwise_tsv_mount = ""
    pairwise_tsv_flag = ""


if multi_comps:
    if not os.path.exists(multi_comps):
        print("Path to multivariate comparisons TSV (-m --multi_tsv) doesn't exist")
        exit()
    else:
        multi_comps = os.path.abspath(multi_comps)
        multi_tsv_mount = f"-v {multi_comps}:/mydata/multi_comps.tsv"
        multi_tsv_flag = "-m /mydata/multi_comps.tsv"
else:
    multi_tsv_mount = ""
    multi_tsv_flag = ""

if threads:
    if not threads.isnumeric():
        print("Number of threads (-n --n_workers) must be numeric")
        exit()
    else:
        thread_flag = f"-n {threads}"
else:
    thread_flag = ""

#Check path to run output
if not os.path.exists(pairwise_output):
    print("Path to pairwise output (-po --pairwise_output) doesn't exist")
    exit()
else:
    os.chdir(pairwise_output)
    pairwise_output = os.getcwd()
    os.chdir(cwd)

# Check path to run output
if not os.path.exists(multi_output):
    print("Path to multi output (-mo --multi_output) doesn't exist")
    exit()
else:
    os.chdir(multi_output)
    multi_output = os.getcwd()
    os.chdir(cwd)

# Check path to run output
if not os.path.exists(runs_dir):
    print("Path to run directory (-r --runs_dir) doesn't exist")
    exit()
else:
    os.chdir(runs_dir)
    runs_dir = os.getcwd()
    os.chdir(cwd)


command = (
    f"{sudo_option} docker run -i -v "
    f"{multi_output}:/app/multi_results -v {pairwise_output}:/app/pairwise_results -v {runs_dir}:/mydata/runs "
    f"{pairwise_tsv_mount} {multi_tsv_mount} "
    f"samhimes92/tmp TMP_comparative.py -r /mydata/runs/ "
    f"{multi_tsv_flag} {pairwise_tsv_flag} {thread_flag}"
)
print(command)
os.system(command)
