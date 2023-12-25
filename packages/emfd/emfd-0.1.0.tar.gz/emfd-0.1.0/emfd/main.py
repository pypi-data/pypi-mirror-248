import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import argparse
from emfd.scoring import score_docs, pat_docs

parser = argparse.ArgumentParser(description='Extract moral informtion from textual documents with emfd.')

parser.add_argument('input_csv', metavar='infile', nargs='+',
                    help='Path to the CSV containing the input text. Each row in the CSV must correspond to one document text')

parser.add_argument('dict_type', metavar='dict_version', nargs='+', type=str, default='emfd',
                    help='Dictionary for scoring. Possible values are: emfd, mfd, mfd2')
                    
parser.add_argument('prob_map', metavar='prob_map', nargs='+', type=str, default='all',
                    help='eMFD only. Assigns either five moral probabilities (all) or only the highest probability (single) to each word. Possible values are: all, single')

parser.add_argument('score_method', metavar='scoring_method', nargs='+', type=str, default='bow',
                    help='Text scoring method. Possible values are: bow, wordlist, gdelt.ngrams, pat')
                    
parser.add_argument('output_metrics', metavar='output_metrics', nargs='+', type=str, default='sentiment',
                    help='eMFD only. Either returns an average sentiment score for each foundation (sentiment) or splits each foundation into a vice/virtue category (vice-virtue).
                    Possible values are: sentiment, vice-virtue')

parser.add_argument('output_csv', metavar='outfile', nargs='+', type=str,
                    help='The path/name for the scored output CSV.')

args = vars(parser.parse_args())
IN_CSV_PATH = args['input_csv'][0]
DICT_TYPE = args['dict_type'][0]
PROB_MAP = args['prob_map'][0]
SCORE_METHOD = args['score_method'][0]
OUT_METRICS = args['output_metrics'][0]
OUT_CSV_PATH = args['output_csv'][0]

infile_type = IN_CSV_PATH.split('.')[-1]

if infile_type == 'csv':
    csv = pd.read_csv(IN_CSV_PATH, header=None)
    num_docs = len(csv)

elif infile_type == 'txt':
    ngrams =  open(IN_CSV_PATH).readlines()
    df = pd.DataFrame()
    df['word'] = [x.split('\t')[3] for x in ngrams]
    df['freq'] = [ int(x.split('\t')[4].strip()) for x in ngrams]
    num_docs = len(df)
else:
    print('Input file type not recognized! Must either be CSV for scoring method bow, wordlist, and pat, or TXT for gdelt.ngram')

print("Running emfd")
print("Total number of input texts to be scored:", num_docs)

if SCORE_METHOD == 'bow':
    df = score_docs(csv,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

if SCORE_METHOD == 'wordlist':
    df = score_docs(csv,DICT_TYPE,SCORE_METHOD,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

if SCORE_METHOD == 'gdelt.ngrams':
    df = score_docs(df,DICT_TYPE,SCORE_METHOD,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

if SCORE_METHOD == 'pat':
    df = pat_docs(csv,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

print('Scoring completed.')
