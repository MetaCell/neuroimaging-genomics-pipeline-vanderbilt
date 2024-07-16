import sciluigi as sl
import subprocess
import os
from multiprocessing import Pool
import numpy as np

from src.config.Config import Config
from src.utils.filesystem import create_path_if_not_exists


class ConvertGenotypeProbabilitiesTask(sl.Task):
    """
    A sciluigi task to convert genotype probabilities to dosages.
    """

    group = sl.Parameter()
    model = sl.Parameter()
    basepath = sl.Parameter()
    done = False

    def out_dosage(self):
        # Define the output target
        return sl.TargetInfo(self, f'{self.basepath}/inputs_{self.group}/dosage_{self.model}')

    @staticmethod
    def convert2dosage(data):

        vcf_path = data['vcf_path']
        dos_path = data['dos_path']
        group = data['group']

        chrom = data['chrom']
        start = data['start']
        end = data['end']
        version = data['version']

        # Group-specific format differences
        header = {'HCP': 0, 'UKB': 5}

        # Chromosome, rsid, position, reference allele, alternate allele, MAF=0, dosage
        new_lines = []

        # Read VCF
        i = -1
        vcf_file = f'{vcf_path}/c{chrom}.vcf'
        with open(vcf_file, 'r') as f:
            for line in f:
                i += 1
                if i < header[group.split('/')[0]]:
                    continue

                # Versioning
                if i < start:
                    continue
                if i == end:
                    break

                # Variant description
                info = line.strip().split('\t')
                rsid = info[2].split(';')[0]
                posn = info[1]
                refa = info[3]
                alta = info[4]
                maf0 = '9'

                desc = '\t'.join([chrom, rsid, posn, refa, alta, maf0])

                # Dosages
                prob = info[9:]
                if group == 'HCP':
                    dosg = [np.array(p.split(','), dtype=float).argmax() for p in prob]
                elif group.split('/')[0] == 'UKB':
                    dosg = [np.array(p.split(':')[1].split(','), dtype=float).argmax() for p in prob]

                dosg = np.array(dosg, dtype=str)
                vals = '\t'.join(dosg)

                # Combine description and values
                new_line = desc + '\t' + vals + '\n'
                new_lines.append(new_line)

        # Write to file
        if len(new_lines) == 0:
            return

        dos_file = f'{dos_path}/c{chrom}_v{version}.dosage.txt'
        with open(dos_file, 'w') as f:
            f.writelines(new_lines)

        print(f'done converting chr {chrom}.{version}')

    def run(self):
        vcf_path = Config.VCF_PATH.replace('GROUP_NAME', self.group).replace('MODEL_NAME', self.model)
        dos_path = str(self.out_dosage().path)
        group = str(self.group)

        print(os.getcwd())

        create_path_if_not_exists(dos_path)
        
        ## Function to read VCF file and convert to dosage

        # Prepare data for multiprocessing
        chr_ver = []
        amax = 100000
        itrs = 5000
        for i, s in enumerate(np.arange(0, amax, itrs)):
            for c in np.arange(22, 0, -1):
                chr_ver.append({
                    'chrom': str(c),
                    'start': s,
                    'end': s + itrs,
                    'version': str(i),
                    'vcf_path': vcf_path,
                    'dos_path': dos_path,
                    'group': group
                })


        # Convert VCF files to dosages using multiprocessing
        pool = Pool(processes=20)
        pool.map(ConvertGenotypeProbabilitiesTask.convert2dosage, chr_ver)

        # Concatenate file versions
        for c in np.arange(22, 0, -1):
            dosage_files = [f for f in os.listdir(dos_path) if f.startswith(f'c{c}_v')]
            with open(os.path.join(dos_path, f'c{c}.dosage.txt'), 'w') as outfile:
                for fname in sorted(dosage_files):
                    with open(os.path.join(dos_path, fname)) as infile:
                        outfile.write(infile.read())
        self.done = True

    def complete(self):
        if self.done:
            return True
        else:
            return False


if __name__ == '__main__':
    class Workflow(sl.WorkflowTask):
        group = sl.Parameter()
        model = sl.Parameter()
        basepath = sl.Parameter()

        def workflow(self):
            convert_task = self.new_task('convert_genotype_probabilities', ConvertGenotypeProbabilitiesTask,
                                         group=self.group, model=self.model, basepath=self.basepath)
            return convert_task

    sl.run_local(main_task_cls=Workflow)