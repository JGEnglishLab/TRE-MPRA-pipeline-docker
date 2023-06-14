import argparse
import os

cwd = os.getcwd()

parser = argparse.ArgumentParser(
                    description = 'Runs Docker container')

parser.add_argument('-ro', '--run_output', dest="run_output", required=True)


parser.add_argument('-f', '--path_to_fq', dest="fastq_path", required=True)
parser.add_argument('-t', '--path_to_treatment_tsv', dest="treatment_tsv_path", required=True)
parser.add_argument('-r', '--run_name', dest="dir_name", required=False)
parser.add_argument('-dt', '--path_to_dna_tsv', dest="dna_tsv_path", required=False)
parser.add_argument('-s', '--path_to_spikein_file', dest="spike_path", required=False)
parser.add_argument('-sr', '--sample_number_regex', dest="pattern", required=False)
parser.add_argument('-d', '--path_to_DNA_fastq', dest="dna_path", required=False)
parser.add_argument('-n', '--n_workers', dest="threads", required=False)
parser.add_argument('--sudo', action='store_true')




args = parser.parse_args()
run_output=args.run_output
dir_name=args.dir_name
fastq_path=args.fastq_path
treatment_tsv_path=args.treatment_tsv_path
dna_tsv_path=args.dna_tsv_path
pattern=args.pattern
dna_path=args.dna_path
spike_path=args.spike_path
threads=args.threads

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


#Checks if they added a dir name
if dir_name:
    dir_name = f"-r {dir_name}"
else:
    dir_name = ""

#Check path to fastq files
if not os.path.exists(fastq_path):
    print("path to fastq_path (-f --path_to_fq) doesn't exist")
    exit()
else:
    os.chdir(fastq_path)
    fastq_path = os.getcwd()
    os.chdir(cwd)

#Check path to run output
if not os.path.exists(run_output):
    print("path to run output (-ro --run_output) doesn't exist")
    exit()
else:
    os.chdir(run_output)
    emp_output = os.getcwd()
    os.chdir(cwd)

#Check path to treatement TSV
if not os.path.exists(treatment_tsv_path):
    print("path to treatment tsv (-t --path_to_treatment_tsv) doesn't exist")
    exit()
else:
    treatment_tsv_path = os.path.abspath(treatment_tsv_path)

#Check optional flags

#Check path to dna fastq files
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



#Check dna tsv path
if dna_tsv_path:
    if not os.path.exists(dna_tsv_path):
        print("path to DNA tsv map (-dt --path_to_dna_tsv) doesn't exist")
        exit()
    else:
        dna_tsv_path=os.path.abspath(dna_tsv_path)
        dna_tsv_mount = f"-v {dna_tsv_path}:/mydata/dna_map.tsv"
        dna_tsv_flag = "-dt /mydata/dna_map.tsv"
else:
    dna_tsv_mount = ""
    dna_tsv_flag = ""

#Check spike in path
if spike_path:
    if not os.path.exists(spike_path):
        print("path to spike in file (-s --path_to_spikein_file) doesn't exist")
        exit()
    else:
        spike_path=os.path.abspath(spike_path)
        spike_mount = f"-v {spike_path}:/mydata/spike.txt"
        spike_flag = "-s /mydata/spike.txt"
else:
    spike_mount = ""
    spike_flag = ""

if pattern:
    pattern_flag = f"-sr {pattern}"
else:
    pattern_flag = ""



command = f"{sudo_option} docker run -i -v " \
          f"{emp_output}:/app/runs -v {fastq_path}:/mydata/fq_files -v {treatment_tsv_path}:/mydata/treatements.tsv " \
          f"{dna_tsv_mount} {spike_mount} {dna_fq_mount} " \
          f"samhimes92/tmp TMP_empirical.py -f /mydata/fq_files -t /mydata/treatements.tsv " \
          f"{dna_tsv_flag} {spike_flag} {dna_fq_flag} {pattern_flag} {dir_name} {thread_flag}"
print(command)
os.system(command)


