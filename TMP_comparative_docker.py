import argparse
import os

cwd = os.getcwd()

parser = argparse.ArgumentParser(
                    description = 'Runs Docker container')

parser.add_argument('-po', '--pairwise_output', dest="pairwise_output", required=True)
parser.add_argument('-mo', '--multi_output', dest="multi_output", required=True)

parser.add_argument('-r', '--runs_dir', dest="runs_dir", required=True) #The directory that has all the runs

parser.add_argument('-p', '--pairwise_tsv', dest="pairwise_comps", required=False)
parser.add_argument('-m', '--multi_tsv', dest="multi_comps", required=False)
parser.add_argument('-n', '--n_workers', dest="threads", required=False)


args = parser.parse_args()
multi_output=args.multi_output
pairwise_output=args.pairwise_output

runs_dir=args.runs_dir
pairwise_comps=args.pairwise_comps
multi_comps=args.multi_comps
threads=args.threads


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

#Check path to run output
if not os.path.exists(multi_output):
    print("Path to multi output (-mo --multi_output) doesn't exist")
    exit()
else:
    os.chdir(multi_output)
    multi_output = os.getcwd()
    os.chdir(cwd)

#Check path to run output
if not os.path.exists(runs_dir):
    print("Path to run directory (-r --runs_dir) doesn't exist")
    exit()
else:
    os.chdir(runs_dir)
    runs_dir = os.getcwd()
    os.chdir(cwd)



command = f"docker run -i -v " \
          f"{multi_output}:/app/multi_results -v {pairwise_output}:/app/pairwise_results -v {runs_dir}:/mydata/runs " \
          f"{pairwise_tsv_mount} {multi_tsv_mount} " \
          f"tmp TMP_comparative.py -r /mydata/runs/ " \
          f"{multi_tsv_flag} {pairwise_tsv_flag} {thread_flag}"
print(command)
os.system(command)


