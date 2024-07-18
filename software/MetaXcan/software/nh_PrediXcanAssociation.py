#! /usr/bin/env python
import os
import logging

from timeit import default_timer as timer

import metax
from metax import Logging
from metax import Exceptions
from metax import Utilities

from metax.predixcan import PrediXcanAssociation as PA
from metax.predixcan import nh_Utilities as PrediXcanUtilities

import numpy as np 
import h5py

def run(args, prediction_results = None):

    ###################################################################################################

    ## subsampling 
    [tag, ds, itr] = args.sample_iter.split('.') ## e.g., poly_train_idxs.HCP/nonTwin.0 
    ipath = f'/data1/rubinov_lab/brain_genomics/paper_twas/'
    ipath += f'inputs_{ds}/{tag}.hdf5'

    with h5py.File(ipath, 'r') as f: sidx = f[itr][()]
    


    #[ds, itr] = args.sample_iter.split('_')

    ### diff models
    #mpath = '/data1/rubinov_lab/brain_genomics/proj_grex/inputs_UKB'
    #ipath = f'{mpath}/idx_{ds}.hdf5' 
    #with h5py.File(ipath, 'r') as f: 
    #    sidx = f[itr][()]

    #mpath = '/data1/rubinov_lab/brain_genomics/paper_twas'
    #if ds == 'HCP':
    #    ## HCP sampling 
    #    sfile = f'{mpath}/inputs_HCP/allEuro/twas_disc_samples.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        sidx = f['772c'][()][itr]

    #elif ds == 'HCPntc': 
    #    ## HCP nonTwin replication sampling 
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_HCPnonTwin.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        sidx = f['repl_idx'][()][itr]

    #elif ds == 'HCPnt': 
    #    ## HCP nonTwin discovery sampling 
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_HCPnonTwin.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        cidx = f['repl_idx'][()][itr]
    #    sidx = np.setdiff1d(np.arange(39565), cidx)

    #elif ds == 'HCPeuc': 
    #    ## HCP allEuro replication sampling 
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_HCPallEuro.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        sidx = f['repl_idx'][()][itr]

    #elif ds == 'HCPeu': 
    #    ## HCP allEuro discovery sampling 
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_HCPallEuro.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        cidx = f['repl_idx'][()][itr]
    #    sidx = np.setdiff1d(np.arange(39565), cidx)

    #elif ds in ['2000', '5500', '15000']: 
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_UKB{ds}.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        cidx = f['repl_idx'][()][itr]
    #    sidx = np.setdiff1d(np.arange(39565), cidx)
    #
    #elif ds in ['2000c', '5500c', '15000c']: 
    #    ff = ds[:-1]
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples_UKB{ff}.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        sidx = f['repl_idx'][()][itr]

    #else:
    #    ## UKB sampling
    #    sfile = f'{mpath}/inputs_UKB/twas_repl_samples.hdf5'
    #    with h5py.File(sfile, 'r') as f: 
    #        cidx = f[ds][()][itr]
    #    sidx = np.setdiff1d(np.arange(39565), cidx)

    ###################################################################################################

    start = timer()
    if os.path.exists(args.output):
        logging.info("%s already exists, you have to move it or delete it if you want it done again", args.output)
        return

    if prediction_results is None and \
            ((args.hdf5_expression_file and args.expression_file) or (not args.hdf5_expression_file and not args.expression_file)):
        logging.info("Provide either hdf5 expression file or plain text expression file")
        return

    with PrediXcanUtilities.p_context_from_args(args, sidx, prediction_results) as context:
        genes = context.get_genes()
        n_genes = len(genes)
        reporter = Utilities.PercentReporter(logging.INFO, n_genes)
        reporter.update(0, "%d %% of model's genes processed so far", force=True)
        results = []
        for i,gene in enumerate(genes):
            logging.log(7, "Processing gene %s", gene)
            r = PA.predixcan_association(gene, context)
            results.append(r)
            reporter.update(i, "%d %% of model's genes processed so far")
        reporter.update(i, "%d %% of model's genes processed so far")
        results = PA.dataframe_from_results(results)
        results = results.sort_values(by="pvalue")
        results = results.fillna("NA")

        Utilities.save_dataframe(results, args.output)

    end = timer()
    logging.info("Successfully ran predixcan associations in %s seconds" % (str(end - start)))


def add_arguments(parser):
    parser.add_argument("--hdf5_expression_file", help="HDF5 File with predicted gene expressions.")
    parser.add_argument("--expression_file",
                        help="Text file (or gzip-compressed) with predicted gene expressions. Alternative to HDF5 file.")
    parser.add_argument("--input_phenos_file",
                        help="Text file (or gzip-compressed) where one column will be used as phenotype")
    parser.add_argument('--covariates', type=str, nargs='+', help='Names of covariates in the file', default=[])
    parser.add_argument('--covariates_file',
                        help="Text file (or gzip-compressed) with covariate data. If provided, will force OLS regression")
    parser.add_argument("--input_phenos_column", help="Name of column from input file to be used as phenotype")
    parser.add_argument("--input_phenos_na_values", help="scalar value to be interpreted as 'NA' in the phenotype", nargs="+")
    parser.add_argument("--output", help="File where stuff will be saved.")
    parser.add_argument("--mode", help="Type of regression. Can be: {}".format(PA.PMode.K_MODES), default=PA.PMode.K_LINEAR)
    parser.add_argument("--sample_iter", help="Random sample iteration.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='PrediXcanAssociation.py %s: Single-Tissue PrediXcan association' % (metax.__version__))

    add_arguments(parser)

    parser.add_argument("--verbosity", help="Log verbosity level. 1 is everything being logged. 10 is only high level messages, above 10 will hardly log anything", default = 10)
    parser.add_argument("--throw", action="store_true", help="Throw exception on error", default=False)

    args = parser.parse_args()

    Logging.configureLogging(int(args.verbosity))

    if args.throw:
        run(args)
    else:
        try:
            run(args)
            print("Done")
        except Exceptions.ReportableException as e:
            logging.error(e.msg)
        except Exception as e:
            logging.info("Unexpected error: %s" % str(e))
