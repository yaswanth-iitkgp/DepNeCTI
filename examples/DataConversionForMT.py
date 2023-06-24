from __future__ import print_function

import re
import pandas as pd
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

import sys
import os
import argparse
from collections import namedtuple


def read_arguments():
    args_ = argparse.ArgumentParser(description='____')
    args_.add_argument('--input_format', choices=['SLP1', 'IAST', 'DEVANAGIRI'], help='input_format_type', required=True)
    args_.add_argument('--label_type', choices=['Finegrain', 'Coarse'], help='Finegrain/Coarse', required=True)
    args = args_.parse_args()
    args_dict = {}
    args_dict['input_format'] = args.input_format
    args_dict['label_type'] = args.label_type
    ARGS = namedtuple('ARGS', args_dict.keys())
    my_args = ARGS(**args_dict)
    return my_args


def raw_to_clean(line):
    line = re.sub('( {1,})',' ',line)
    line = re.sub('-$','',line) #to remove the - in the end
    line = re.sub('<','',line)
    line = re.sub('-',' ',line)
    line = re.sub('(>\w+)','',line)
    line = re.sub(' $','',line) #to remove the space in the end
    line = re.sub('^ ','',line) #to remove the space in the beginning
    line = re.sub('( {1,})',' ',line)
    return line

def transliteration(file,input_scheme,out_file,output_scheme):
    with open(file) as f:
        lines = f.readlines()
    input_scheme = getattr(sanscript,input_scheme)
    output_scheme = getattr(sanscript,output_scheme)
    with open(out_file,'w') as o:
        for line in lines:
            line_new = transliterate(line,input_scheme,output_scheme)
            o.write(line_new)
    return


def data_conversion(file,outfile_path):
    with open(file) as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        tokens = line.strip().split()
        i = 0
        tok_len = len(tokens)
        for token in tokens:
            if '-' not in token:
                i += 1
                new_lines.append(f'{i}\t{token}\tCompNo\t_\t{tok_len+1}\t_\n')
            else:
                tokens_lst = raw_to_clean(token).split()
                length = len(tokens_lst)
                j = 0
                for token in tokens_lst:
                    i += 1
                    if j!=len(tokens_lst)-1:
                        new_lines.append(f'{i}\t{token}\tComp{length}\t_\t{tok_len+1}\t_\n')
                    else:
                        new_lines.append(f'{i}\t{token}\tComp{length}\t_\t{tok_len+1}\tComp_root\n')
                    j+= 1
        new_lines.append(f'{i}\tDUMMY\tCompNo\t_\t{0}\troot\n')
        new_lines.append('\n')
    with open(outfile_path,'w') as o:
        for line in new_lines:
            o.write(line)
    return

def main():
    args = read_arguments()
    script_dir = os.path.dirname(os.path.abspath(__file__))

    infile = os.path.join(script_dir, "..", "data_MT", "input_IAST.txt")
    outfile = os.path.join(script_dir, '..', 'data_MT', 'NeCTIS_input_SLP1.txt')
    transliteration(infile,args.input_format,outfile,"SLP1")

    data_conversion_outfile = os.path.join(script_dir, '..', 'data', 'ud_pos_ner_dp_test_san')
    data_conversion(outfile,data_conversion_outfile)


if __name__ == '__main__':
    main()