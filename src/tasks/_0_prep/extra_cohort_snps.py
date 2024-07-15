import sciluigi as sl
import os
import subprocess

from src.config.Config import Config

class ExtractSNPsConvertBgenToVcfTask(sl.Task):
    """
    A sciluigi task to extract SNPs used in the JTI models for the UKB cohort
    and convert BGEN files to VCF format.
    """
    coho = sl.Parameter()
    basepath = sl.Parameter()
    done = False

    def out_vcf(self):
        """Define the output target for VCF path"""
        return sl.TargetInfo(self, f'{self.basepath}/inputs_{self.coho}/vcf_JTI')

    def run(self):
        coho = self.coho
        #TODO Refactor and try to move to config
        path_jti = os.path.join(Config.DATA_ROOT, 'aux_files/snps_keep.txt')
        path_bgn = os.path.join(Config.DATA_ROOT, f'inputs_{coho}/bgen_JTI')
        path_cohort = os.path.join(Config.DATA_ROOT, f'inputs_{coho}/cohort.txt')
        path_vcf = self.out_vcf().path

        # Ensure output directories exist
        if not os.path.exists(path_bgn):
            os.makedirs(path_bgn)
        if not os.path.exists(path_vcf):
            os.makedirs(path_vcf)

        # Extract SNPs and convert BGEN to VCF
        for CHR in range(22, 0, -1):
            chr_str = str(CHR)
            plink_cmd = [
                "plink2",
                "--bgen", f"{path_bgn}/c{chr_str}.bgen", "ref-first",
                "--sample", Config.SAMPLE,
                "--keep", path_cohort,
                "--extract", path_jti,
                "--export", "bgen-1.2",
                "--snps-only",
                "--out", f"{path_bgn}/c{chr_str}"
            ]

            if CHR in [16, 10, 4, 1]:
                subprocess.run(plink_cmd, check=True)
            else:
                subprocess.Popen(plink_cmd, shell=True)


        for CHR in range(22, 0, -1):
            chr_str = str(CHR)
            bgenix_index_cmd = [
                Config.BGENIX_PATH,
                "-g", f"{path_bgn}/c{chr_str}.bgen",
                "-index"
            ]
            bgenix_vcf_cmd = [
                Config.BGENIX_PATH,
                "-g", f"{path_bgn}/c{chr_str}.bgen",
                "-vcf"
            ]

            subprocess.run(bgenix_index_cmd, check=True)
            with open(f"{path_vcf}/c{chr_str}.vcf", "w") as vcf_file:
                subprocess.run(bgenix_vcf_cmd, stdout=vcf_file, check=True)

        self.done = True

    def complete(self):
        return self.done


if __name__ == '__main__':
    class Workflow(sl.WorkflowTask):
        coho = sl.Parameter()
        basepath = sl.Parameter()

        def workflow(self):
            extract_convert_task = self.new_task('extract_snps_convert_bgen_to_vcf', ExtractSNPsConvertBgenToVcfTask,
                                                 coho=self.coho, basepath=self.basepath)
            return extract_convert_task

    sl.run_local(main_task_cls=Workflow)
