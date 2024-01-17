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

parser.add_argument("-po", required=False, default = "./", help=ht.po())
parser.add_argument("-r", required=True, help=ht.r_comparative_docker())  # The directory that has all the runs
parser.add_argument("-p", required=False, help=ht.p())
parser.add_argument("-n", required=False, help=ht.n())
parser.add_argument("--sudo", action="store_true", help=ht.sudo())


args = parser.parse_args()
pairwise_output = vars(args)["po"]
runs_dir = vars(args)["r"]
pairwise_comps = vars(args)["p"]
threads = vars(args)["n"]


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
if not os.path.exists(runs_dir):
    print("Path to run directory (-r --runs_dir) doesn't exist")
    exit()
else:
    os.chdir(runs_dir)
    runs_dir = os.getcwd()
    os.chdir(cwd)


command = (
    f"{sudo_option} docker run -i "
    f"-v {pairwise_output}:/app/pairwise_results -v {runs_dir}:/mydata/runs "
    f"{pairwise_tsv_mount} "
    f"{CONTAINER_ID} TMP_comparative.py -r /mydata/runs/ "
    f"{pairwise_tsv_flag} {thread_flag}"
)


print(command)
os.system(command)

print("Finished")
print("Removing Docker Image")
remove_command = f'docker rm $(docker stop $(docker ps -a -q --filter ancestor={CONTAINER_ID} --format="{{{{.ID}}}}")) '
os.system(remove_command)