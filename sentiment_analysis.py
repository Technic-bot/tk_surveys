import argparse
import pprint
import csv

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

from transformers import pipeline
from sentence_transformers import SentenceTransformer   

import umap

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
    args.add_argument("embeds_dir", help="Output dir for embeddings")
    args.add_argument("sentiment_dir", help="Output dir for sentiment analysys")
    args.add_argument("--skip-sentiment",
            help="Skip sentiment analysis portion",
            action='store_true')
    args.add_argument("--skip-embedding",
            help="Skip embbeding analysis portion",
            action='store_true')
    return args.parse_args()

class SurveySentimentAnalysis():
    def __init__(self, infile, embeds_dir, sentiment_dir, questions):
        self.infile = infile
        self.embeds_dir = embeds_dir
        self.sentiment_dir = sentiment_dir
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
        self.reducer = umap.UMAP()

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
        df['response'].to_markdown(self.sentiment_dir + "sentiment_"+ col_remap[question] + ".md", index=False)
        return df.to_dict(orient="records")

    def embedding_analysis(self):
        for q in self.questions:
            responses = self.survey[q].dropna().to_list()
            print(f"Embedding analysis for {q}")
            embeddings = self.embedder.encode(responses, convert_to_numpy=True)
            print("Running UMAP")
            redu_embeds = self.reducer.fit_transform(embeddings)
            df = pd.DataFrame(responses, columns=['response'])
            df['embeddings'] = list(embeddings)
            df['umapx'] = list(redu_embeds[:,0])
            df['umapy'] = list(redu_embeds[:,1])

            self.embeddings[q] = df
            # self.persist_embeddings(q, analysis)

    def persist_embeddings(self, embed_df):
        filename = self.embed_dir + "embeddings_"+ col_remap[question] + ".parquet"
        df.to_parquet(filename) 
        return

    def graph_embeddings(self):
        for q, df in self.embeddings.items():
            print(f"Graphing embeddings for {q}")
            fig, ax = plt.subplots(
                    figsize=(19, 10)
                    )
        
            ax.scatter(df['umapx'], df['umapy'])
            ax.set_title(f'UMAP reduction of response embeddings for:\n {q}')
            break
            # fig.legend(loc='upper center')
        return fig


if __name__=="__main__":
    opts = proc_opts()
    ssa = SurveySentimentAnalysis(
            opts.file, opts.embeds_dir, opts.sentiment_dir,
            sentiment_cols)
    if not opts.skip_sentiment:
        ssa.sentiment_analysis()
    if not opts.skip_embedding:
        ssa.embedding_analysis()
        ssa.graph_embeddings()
        plt.show()

