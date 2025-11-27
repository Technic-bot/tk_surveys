import argparse
import pprint
import csv

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import umap
#from hdbscan import HDBSCAN
from sklearn.cluster import HDBSCAN
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
    args.add_argument("embeds_dir", help="Output dir for embeddings")
    args.add_argument("sentiment_dir", help="Output dir for sentiment analysys")
    args.add_argument("--skip-sentiment",
            help="Skip sentiment analysis portion",
            action='store_true')
    args.add_argument("--skip-embedding",
            help="Skip embbeding analysis portion",
            action='store_true')
    args.add_argument("--skip-reduce",
            help="Skip UMAP reduction",
            action='store_true')
    return args.parse_args()

class SurveySentimentAnalysis():
    def __init__(self, infile, embeds_dir, sentiment_dir, questions,
            skip_sentiment = False, skip_reduce = False, 
            skip_embeds = False):
        self.infile = infile
        self.embeds_dir = embeds_dir
        self.sentiment_dir = sentiment_dir
        self.survey = pd.read_csv(self.infile)
        self.questions = questions
        self.preprocess()
        self.skip_sentiment = skip_sentiment
        self.skip_reduce = skip_reduce

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
        self.clusterer = HDBSCAN(min_samples=15)

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
        df.to_csv(self.sentiment_dir + "sentiment_"+ col_remap[question] + ".csv", index=False)

        # Emit only responses in order for markdowns
        filename = self.sentiment_dir + "sentiment_"+ col_remap[question] + ".md"
        md = df['response'].to_markdown(index=False)
        with open(filename, 'w') as md_file:
            md_file.write(f"# {question} \n\n") 
            md_file.write(md)
        return df.to_dict(orient="records")

    def embedding_analysis(self):
        for q in self.questions:
            responses = self.survey[q].dropna().to_list()
            print(f"Embedding analysis for {q}")
            print("\tEncoding transformer")
            embeddings = self.embedder.encode(responses, convert_to_numpy=True)
            df = pd.DataFrame(responses, columns=['response'])
            df['embeddings'] = list(embeddings)
             
            print("\tRunning HBDScan")
            self.clusterer.fit(embeddings)
            df['cluster'] = self.clusterer.labels_
            print(f"\tGot {self.clusterer.labels_.max()} clusters")

            if not self.skip_reduce:
                print("\tRunning UMAP")
                redu_embeds = self.reducer.fit_transform(embeddings)
                df['umapx'] = list(redu_embeds[:,0])
                df['umapy'] = list(redu_embeds[:,1])

            self.embeddings[q] = df
            #self.persist_embeddings(q, df)

    def persist_embeddings(self, question, embed_df):
        if not self.embeds_dir:
            return
        filename = self.embeds_dir + "embeddings_"+ col_remap[question] + ".parquet"
        embed_df.to_parquet(filename) 
        return

    def graph_embeddings(self):
        if self.skip_reduce:
            print("No UMAP computed, cannot graph") 
            return 

        for q, df in self.embeddings.items():
            print(f"Graphing embeddings for {q}")
            fig, ax = plt.subplots(
                    figsize=(19, 10)
                    )
        
            ax.scatter(df['umapx'], df['umapy'], c=df['cluster'], cmap='Spectral')
            ax.set_title(f'UMAP reduction of response embeddings for:\n {q}')
            # fig.legend(loc='upper center')
            if self.embeds_dir:
                filename = self.embeds_dir + col_remap[q] + ".png" 
                fig.savefig(filename)
        
        if not self.embeds_dir:
            plt.show()
        return fig


if __name__=="__main__":
    opts = proc_opts()
    ssa = SurveySentimentAnalysis(
            opts.file, opts.embeds_dir, opts.sentiment_dir,
            sentiment_cols, 
            skip_sentiment = opts.skip_sentiment,
            skip_reduce = opts.skip_reduce,
            skip_embeds = opts.skip_embedding)

    if not opts.skip_sentiment:
        ssa.sentiment_analysis()
    if not opts.skip_embedding:
        ssa.embedding_analysis()
        ssa.graph_embeddings()

