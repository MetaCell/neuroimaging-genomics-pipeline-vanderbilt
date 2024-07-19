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
        return sl.TargetInfo(self, f'{self.basepath}/{Config.OUTPUT_VCF_JTI}'.replace('COHO', self.coho))

    def run(self):
        coho = self.coho
        path_bgn = Config.PATH_BGEN.replace('GROUP_NAME', coho)
        path_jti = Config.PATH_JTI
        path_cohort = Config.PATH_COHORT.replace('GROUP_NAME', coho)
        prep_sample = Config.PREP_SAMPLE.replace('GROUP_NAME', coho)
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
                Config.PLINK_PATH,
                "--bgen", f"{path_bgn}/c{chr_str}.bgen", "ref-first",
                "--sample", prep_sample,
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
                "-index",
                "-clobber"
                # TODO: -clobber: Specify that bgenix should overwrite existing index file if it exists.
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
