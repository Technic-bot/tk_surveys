import argparse
import pprint
import csv

import pandas as pd
from transformers import pipeline
from sentence_transformers import SentenceTransformer   

from survey_config import survey

col_remap = { s['raw']: s['name'] for s in survey}
sentiment_cols = [ s['raw'] for s in survey if s['type'] == 'sentiment']

def proc_opts():
    args = argparse.ArgumentParser(
        description="Sentiment analysis for TK surveys",
        prog="Survey grapher",
        epilog="Made by Tec bot with ❤️ ",
    )
    args.add_argument("file", help="Input pandas file")
    args.add_argument("output", help="Output dir")
    return args.parse_args()

class SurveySentimentAnalysis():
    def __init__(self, infile, outdir, questions):
        self.infile = infile
        self.outdir = outdir
        self.survey = pd.read_csv(self.infile)
        self.questions = questions
        self.preprocess()

        self.sentiments = {}
        self.embeddings = {}
        # sentiment_pipeline = pipeline('sentiment-analysis', device=0)
        # sentiment_pipeline = pipeline(model="bhadresh-savani/distilbert-base-uncased-emotion", device=0)
        self.sentiment_pipeline = pipeline(
                "text-classification", 
                model="tabularisai/multilingual-sentiment-analysis")
        self.embedder = SentenceTransformer(
                'sentence-transformers/paraphrase-mpnet-base-v2') 

    def preprocess(self ):
        self.survey = self.survey.rename(columns=lambda x: x.strip())
        #df = df.rename(columns=col_remap)
        self.survey = self.survey[sentiment_cols]
        # pprint.pprint(col_remap)
        # df["time"] = pd.to_datetime(df["time"], dayfirst=True)

    def sentiment_analysis(self):
        """ Run sentiment analysis and store results"""
        for q in self.questions:
            print(f"Sentiment analysis for {q}")
            responses = self.survey[q].dropna().to_list()
            sentiment = self.sentiment_pipeline(responses)
            analysis = []
            for r, s in zip(responses, sentiment):
                row = { 'response' : r, 
                      'label' : s['label'],
                      'score' : s['score']
                }
                analysis.append(row)
            
            sort_analysis = self.persist_sentiment(q, analysis)
            self.sentiments[q] = sort_analysis

        return

    def persist_sentiment(self, question, analysis):
        df = pd.DataFrame(analysis)
        df = df.sort_values(by=['label', 'score'], ascending=False)
        df.to_csv(self.outdir + "sentiment_"+ col_remap[question] + ".csv", index=False)
        # Emit only responses in order for markdowns
        df['response'].to_markdown(self.outdir + "sentiment_"+ col_remap[question] + ".md", index=False)
        return df.to_dict(orient="records")

    def embedding_analysis(self):
        for q in self.questions:
            print(f"Embedding analysis for {q}")
            responses = self.survey[q].dropna().to_list()
            embeddings = self.embedder.encode(responses)
            analysis = []
            for r, e in zip(responses, embeddings):
                row = { 'response' : r,
                        'embedding' : e}
                analysis.append(row)

            self.embeddings[q] = analysis
            self.persist_embeddings(q, analysis)

    def persist_embeddings(self, question, analysis):
        filename = self.outdir + "embeddings_"+ col_remap[question] + ".csv"
        with open(filename, 'w') as emb_file:
            headers = ['response', 'embedding']
            writer = csv.DictWriter(emb_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(analysis)
        return
            

if __name__=="__main__":
    opts = proc_opts()
    ssa = SurveySentimentAnalysis(opts.file, opts.output, sentiment_cols)
    ssa.sentiment_analysis()
    ssa.embedding_analysis()

