import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd 
import argparse
from scoring import score_docs, pat_docs

parser = argparse.ArgumentParser(description='Extract moral informtion from textual documents with AMorE.')

parser.add_argument('input_csv', metavar='infile', nargs='+',
                    help='Path to the CSV containing the input text. Each row in the CSV must correspond to one document text')

parser.add_argument('dict_type', metavar='dict_version', nargs='+', type=str, default='emfd',
                    help='Dictionary for scoring. Possible values are: emfd, mfd, mfd2')

parser.add_argument('score_method', metavar='scoring_method', nargs='+', type=str, default='bow',
                    help='Dictionary for scoring. Possible values are: bow, pat')

parser.add_argument('output_csv', metavar='outfile', nargs='+', type=str,
                    help='The path/name for the scored output CSV.')

args = vars(parser.parse_args())
IN_CSV_PATH = args['input_csv'][0]
OUT_CSV_PATH = args['output_csv'][0]
DICT_TYPE = args['dict_type'][0]
SCORE_METHOD = args['score_method'][0]

csv = pd.read_csv(IN_CSV_PATH, header=None)
num_docs = len(csv)

print("❤ Running AMorE ❤")
print("Total number of input texts to be scored:", num_docs)

if SCORE_METHOD == 'bow':
    df = score_docs(csv,DICT_TYPE,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)
    
if SCORE_METHOD == 'pat':
    df = pat_docs(csv,DICT_TYPE,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

print('Scoring completed.')