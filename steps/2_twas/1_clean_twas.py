'''
Clean up TWAS output files. 

- Nhung, Feb 2024
'''

import sys 
import os 
import logging

cohort = sys.argv[1] ## UKB/twas_JTI/vol_mean
# main_path = '/data1/rubinov_lab/brain_genomics/metacell/outputs'
main_path = '../../data/outputs'
coho_path = f'{main_path}_{cohort}'

tfiles = os.listdir(coho_path)
logging.basicConfig(filename=f'{coho_path}/clean_twas.log', level=logging.INFO)
for t, tpath in enumerate(tfiles): 
    logging.info(f'Processing {tpath}')
    tfile = f'{coho_path}/{tpath}'

    ############ EDIT BY @d-gopalkrishna ############
    if os.path.isdir(tfile): continue

    with open(tfile, 'r') as f: 
        lines = f.readlines()
        logging.info(f'Reading {tfile}, lines: {lines[1]}')

    if lines[1][0] != 'b': continue 

    new_lines = [lines[0]]
    for line in lines[1:]: 

        if '"' in line: 
            continue 

        if 'pheno' in line: 
            continue 

        if line[0] == 'b': 
            new_line = line.replace('b', '').replace("'", "")
            new_lines.append(new_line)

    with open(tfile, 'w') as f: 
        logging.info(f'Writing to {tfile}')
        f.writelines(new_lines)

    if (t%100) == 0: 
        print('{} / {}'.format(t, len(tfiles)))

        
    

