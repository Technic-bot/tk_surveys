import argparse
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from textwrap import fill

from renames import (
    cols,
    col_remap,
    raw_cols,
    gender_renames,
    orig_renames,
    char_renames,
)
from graph_list import pie_graphs,bar_graphs, histograms,bar_order_keys

import pprint


def proc_opts():
    parser = argparse.ArgumentParser(
        prog="Survey grapher",
        description="Graph the TK surveys",
        epilog="Made by Tec bot with ❤️ ",
    )
    parser.add_argument("file", help="Input CSV")
    parser.add_argument("--outdir", help="Output dir")
    parser.add_argument("--dry-run",'-n', help="Dry run",action='store_true')
    return parser.parse_args()


def graph_time(df):
    grp = pd.Grouper(key="time", freq="D")
    time_df = df.groupby(grp).count()
    print(time_df["age"].sum())

    fig, axs = plt.subplots()
    axs.plot(time_df.index, time_df["age"])

    axs.set_title("Submissions")
    fig.autofmt_xdate()
    axs.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    return fig


def graph_age_hist(df):
    min_age = df["age"].min()
    max_age = df["age"].max()
    print("Max age: {}".format(max_age))
    print("Min age: {}".format(min_age))
    bins = np.arange(15, 70,5)

    fig, ax = plt.subplots()
    ax.hist(df["age"], bins=bins, rwidth=0.5, align="mid", color="#72CDFE")
    ax.set_xticks(bins)
    ax.set_title("Age distribution")
    ax.set_xlabel("Age [years]")
    ax.set_ylabel("Count")

    return fig


def graph_hist(df, col, title, label):
    min_col = df[col].min()
    max_col = df[col].max()
    bins = np.arange(min_col, max_col)
    print(min_col, max_col)

    fig, ax = plt.subplots()
    n = ax.hist(df[col], bins=bins, rwidth=0.8, align="mid", color="#72CDFE")
    print(bins,n[0])
    ax.set_xticks(bins)
    ax.set_title(title)
    ax.set_xlabel(label)
    ax.set_ylabel("Count")

    return fig


def graph_bar(df, col, title, other_n=1, crop=0):

    if other_n:
        others = df[col].value_counts()[df[col].value_counts() < other_n]
        df.loc[df[col].isin(others.index), col] = "Other"

    g_df = df.groupby(col).count()
    if crop:
        g_df = g_df[g_df["time"] > crop]
    g_df.sort_values(by="time", inplace=True, axis=0, ascending=False)

    fig, ax = plt.subplots(figsize=(6.4, 5.2))
    x = np.arange(len(g_df.index))
    labs = g_df.index.str.wrap(12)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, rotation=25)
    ax.bar(labs, g_df["time"], color="#72CDFE")
    ax.set_title(title)
    ax.set_ylabel("Count")

    return fig


def graph_bar_order_key(df, col, title, crop=1):

    g_df = df.groupby(col).count()
    if crop:
        g_df = g_df[g_df["time"] > crop]
      
    g_df.sort_index(inplace=True)


    fig, ax = plt.subplots()
    ax.bar(g_df.index, g_df["time"], color="#F7941D")
    ax.set_title(title)
    ax.set_ylabel("Count")

    return fig


def graph_pie(df, col, title, other_n=2):

    # othering
    others = df[col].value_counts()[df[col].value_counts() < other_n]
    df.loc[df[col].isin(others.index), col] = "other"

    g_df = df.groupby(col).count()
    fig, ax = plt.subplots()
    labs = g_df.index.str.wrap(24)
    ax.pie(g_df["time"], labels=labs, autopct="%1.1f%%")
    ax.set_title(title)

    return fig


def preprocess(df):
    # whitespace i hate you!
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df.rename(columns=col_remap, inplace=True)
    df["time"] = pd.to_datetime(sur_df["time"])
    df["gender"].replace(gender_renames, inplace=True)
    df["origin"].replace(orig_renames, inplace=True)
    df["fav_char"] = df["fav_char"].str.strip()
    df["fav_char"].replace(char_renames, inplace=True)
    df["unfav_char"] = df["unfav_char"].str.strip()
    df["unfav_char"].replace(char_renames, inplace=True)
    df["fav_race"] = df["fav_race"].str.replace(r" \(.*\)", "", regex=True)
    df["patreon"] = df["patreon"].str.replace(r" \(.*\)", "", regex=True)

def proc_merch(df):
  # Merch question requires extra processing
  # Can be tuned into generic multi response plotter
  merch = df['merch'].str.split(',')
  merch = merch.explode()
  merch = merch.str.strip()
  g_df = merch.groupby(merch).count()
  g_df.sort_values(inplace=True, axis=0, ascending=False)

  fig, ax = plt.subplots(figsize=(6.4,5.2))
  x = np.arange(len(g_df.index))
  labs = g_df.index.str.wrap(12)
  ax.set_xticks(x)
  ax.set_xticklabels(labs, rotation=25)
  ax.tick_params(axis='both', which='major', labelsize=8)
  ax.bar(labs,g_df.values,color="#F7941D")
  ax.set_title("Do you own any Tk merchandise?")

  return fig

if __name__ == "__main__":
    args = proc_opts()
    plt.style.use("seaborn-darkgrid")
    sur_df = pd.read_csv(args.file)
    preprocess(sur_df)

    #f = graph_bar(sur_df,'edu','Education')
    #plt.show()
    #sys.exit(1)
    
    print("Plotting merch graph")
    f = proc_merch(sur_df)
    if args.outdir and not args.dry_run:
      f.savefig(args.outdir +"_merch_pie.png")
      plt.close(f)

    print("Plotting age graph")
    f = graph_age_hist(sur_df)
    if args.outdir and not args.dry_run:
      f.savefig(args.outdir +"_age_hist.png")
      plt.close(f)

    print("Plotting pie graphs")
    for col,title in pie_graphs:
      print("Plotting {} with title {}".format(col,title))
      f = graph_pie(sur_df,col,title)
      if args.outdir and not args.dry_run:
        f.savefig(args.outdir + col + "_pie.png")
        plt.close(f)

    print("Plotting bar graphs")
    for col,title in bar_graphs:
      print("Plotting {} with title {}".format(col,title))
      f = graph_bar(sur_df,col,title)
      if args.outdir and not args.dry_run:
        f.savefig(args.outdir + col + "_bar.png")
        plt.close(f)

    print("Plotting histograms")
    for col,title,label in histograms:
      print("Plotting {} with title {}".format(col,title))
      f = graph_hist(sur_df,col,title,label)
      if args.outdir and not args.dry_run:
        f.savefig(args.outdir + col + "_hist.png")
        plt.close(f)

    print("Plotting bar graphs ordered")
    for col,title in bar_order_keys:
      print("Plotting {} with title {}".format(col,title))
      f = graph_bar_order_key(sur_df,col,title)
      if args.outdir and not args.dry_run:
        f.savefig(args.outdir + col + "_ord.png")
        plt.close(f)

    if not args.outdir:
      plt.show()
