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

from datetime import datetime

import pprint

FIG_SIZE = (12,8)

from survey_config import survey

col_remap = { s['raw']: s['name'] for s in survey}
pie_graphs = [entry for entry in survey if entry['type'] == 'pie']
bar_cat = [entry for entry in survey if entry['type'] == 'bar_cat']
bar_num = [entry for entry in survey if entry['type'] == 'bar_num']
histograms = [entry for entry in survey if entry['type'] == 'histogram']
bar_order_keys = [entry for entry in survey if entry['type'] == 'bar_order_keys']

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
    #print(time_df["age"].sum())

    fig, axs = plt.subplots(figsize=FIG_SIZE)
    axs.plot(time_df.index, time_df["age"])

    axs.set_title("Submissions")
    fig.autofmt_xdate()
    axs.fmt_xdata = mdates.DateFormatter("%Y-%m-%d")
    return fig

def add_footer(ax):
    date = datetime.today().strftime('%Y-%m-%d')
    msg = f"Made by Tec poll up to {date}"
    ax.annotate(msg,
            xy = (1.0, 1.1),
            xycoords='axes fraction',
            ha='right',
            va="center",
            fontsize=10)
    return

def graph_age_hist(df):
    min_age = df["age"].min()
    max_age = df["age"].max()
    print("Max age: {}".format(max_age))
    print("Min age: {}".format(min_age))
    bins = np.arange(12, 80,2)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.hist(df["age"], bins=bins, rwidth=0.75, align="mid", color="#72CDFE")
    ax.set_xticks(bins)
    ax.set_xticklabels(bins, rotation=25)
    ax.set_title("Age distribution")
    ax.set_xlabel("Age [years]")
    ax.set_ylabel("Count")
    add_footer(ax)
    return fig


def graph_hist(df, col, title, label):
    min_col = df[col].min()
    max_col = df[col].max()
    bins = np.arange(min_col, max_col+1)
    #print(min_col, max_col+1)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    n = ax.hist(df[col], bins=bins, rwidth=0.8, align="mid", color="#72CDFE")
    #print(df.groupby(col).count()['time'])
    ax.set_xticks(bins)
    ax.set_xticklabels(bins.astype(int), rotation=25)
    ax.set_xticks(bins)
    ax.set_title(title)
    ax.set_xlabel(label)
    ax.set_ylabel("Count")
    add_footer(ax)

    return fig

def prune(df, col, title, other_n, crop):
    if other_n:
        # Find and replace all instances with count < other_n
        # with 'Other'
        vc = df[col].value_counts() 
        others = vc[vc < other_n]
        df.loc[df[col].isin(others.index), col] = "Other"

    g_df = df.groupby(col).count()
    if crop:
        # count instance per group crop anything with at least "crop" times
        g_df = g_df[g_df["time"] > crop]
    return g_df

def graph_bar_categorical(df, col, title, other_n=2, crop=0):
    g_df = prune(df, col, title, other_n, crop)
    g_df.sort_values(by="time", inplace=True, axis=0, ascending=False)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    x = np.arange(len(g_df.index))
    labs = g_df.index.str.wrap(12)
    ax.set_xticks(x)
    ax.set_xticklabels(labs, rotation=25)
    ax.bar(labs, g_df["time"], color="#72CDFE")
    ax.set_title(title)
    ax.set_ylabel("Count")
    add_footer(ax)

    return fig

def graph_bar_numerical(df, col, title, other_n=0, crop=0, label=None):
    g_df = prune(df, col, title, other_n, crop)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    x = np.arange(max(g_df.index)+1)
    ax.set_xticks(x)
    ax.bar(g_df.index, g_df["time"], color="#72CDFE")
    ax.set_title(title)
    ax.set_ylabel("Count")
    if label:
        ax.set_xlabel(label)
    add_footer(ax)
    return fig

def graph_bar_order_key(df, col, title, crop=0):

    g_df = df.groupby(col).count()
    if crop:
        g_df = g_df[g_df["time"] > crop]
      
    g_df.sort_index(inplace=True)

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.bar(g_df.index, g_df["time"], color="#F7941D")
    ax.set_title(title)
    ax.set_ylabel("Count")
    add_footer(ax)

    return fig


def graph_pie(df, col, title, other_n=2):
    # othering
    if other_n:
        # Find and replace all instances with count < other_n
        # with 'Other'
        vc = df[col].value_counts() 
        others = vc[vc < other_n]
        df.loc[df[col].isin(others.index), col] = "Other"

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    g_df = df.groupby(col).count()
    labs = g_df.index.str.wrap(24)
    ax.pie(g_df["time"], labels=labs, autopct="%1.1f%%")
    ax.set_title(title)
    add_footer(ax)

    return fig

def proc_merch(df):
  # Merch question requires extra processing
  # Can be tuned into generic multi response plotter
  # separator string may change next year
  # it did
  merch = df['merch'].str.split(',')
  merch = merch.explode()
  merch = merch.str.strip()
  g_df = merch.groupby(merch).count()
  g_df.sort_values(inplace=True, axis=0, ascending=False)

  fig, ax = plt.subplots(figsize=FIG_SIZE)
  x = np.arange(len(g_df.index))
  labs = g_df.index.str.wrap(12)
  ax.set_xticks(x)
  ax.set_xticklabels(labs, rotation=25)
  ax.tick_params(axis='both', which='major', labelsize=8)
  ax.bar(labs,g_df.values,color="#F7941D")
  ax.set_title("Do you own any Tk merchandise?")

  return fig

def save_graph(figure, filename, dry_run=False ):
    if dry_run:
        return
    figure.savefig(filename)
    plt.close(figure)
    return

def preprocess(df):
    # whitespace i hate you!
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df.rename(columns=col_remap, inplace=True)
    # pprint.pprint(col_remap)
    df["time"] = pd.to_datetime(sur_df["time"], dayfirst=True)
    df["gender"] = df["gender"].replace(gender_renames)
    df["origin"] = df["origin"].replace(orig_renames)
    df["fav_char"] = df["fav_char"].str.strip()
    df["fav_char"] = df["fav_char"].replace(char_renames)
    df["unfav_char"] = df["unfav_char"].str.strip()
    df["unfav_char"] = df["unfav_char"].replace(char_renames)
    df["fav_race"] = df["fav_race"].str.replace(r" \(.*\)", "", regex=True)
    df["patreon"] = df["patreon"].str.replace(r" \(.*\)", "", regex=True)
    df["intro"] = df["intro"].str.replace(r" \(.*\)", "", regex=True)
    return

if __name__ == "__main__":
    args = proc_opts()
    plt.style.use("seaborn-v0_8-darkgrid")
    sur_df = pd.read_csv(args.file)
    preprocess(sur_df)
    print(f"Got {len(sur_df)} entries")

    print("Plotting age graph")
    f = graph_age_hist(sur_df)
    if args.outdir:
      name = args.outdir +"_age_dist_condensed.png"
      print(name)
      save_graph(f,name, args.dry_run)

    print("Plotting merch graph")
    f = proc_merch(sur_df)
    if args.outdir: 
      save_graph(f,args.outdir +"_merch.png", args.dry_run)

    print("Plotting What got you into Twokinds?")
    f = graph_bar_categorical(
        sur_df, 'intro', "What got you into Twokinds?",2)
    if args.outdir: 
      save_graph(f,args.outdir +"_intro.png", args.dry_run)

    print("Plotting bar graphs numerical")
    for graph in bar_num:
      col = graph['name']
      title = graph['title']
      label = graph['label']
      tp = graph['type']
      print(f"\tPlotting {col} with title {title} as {tp}")
      f = graph_bar_numerical(sur_df, col, title ,0, label=label)
      if args.outdir: 
        name = "_".join([args.outdir, col, "numbar.png"])
        save_graph(f, name, args.dry_run)
    
    print("Plotting bar graphs categorical")
    for graph in bar_cat:
      col = graph['name']
      title = graph['title']
      print(f"\tPlotting {col} with title {title}")
      f = graph_bar_categorical(sur_df, col, title ,1)
      if args.outdir: 
        name = "_".join([args.outdir, col, "catbar.png"])
        save_graph(f, name, args.dry_run)
    
    print("Plotting histograms")
    for graph in histograms:
      col = graph['name']
      title = graph['title']
      label = graph['label']
      print(f"\tPlotting {col} with title {title}")
      f = graph_hist(sur_df, col, title, label )
      if args.outdir:
        name = "_".join([args.outdir, col, "hist.png"])
        save_graph(f, name, args.dry_run)

    print("Plotting pie graphs")
    for graph in pie_graphs:
      col = graph['name']
      title = graph['title']
      print(f"\tPlotting {col} with title {title}")
      f = graph_pie(sur_df,col,title)
      if args.outdir:
        save_graph(f, "_".join([args.outdir, col, "pie.png"]), args.dry_run)

    print("Plotting ordered bar graphs")
    for graph in bar_order_keys:
      col = graph['name']
      title = graph['title']
      print("\tPlotting {} with title {}".format(col,title))
      f = graph_bar_order_key(sur_df,col,title)
      if args.outdir:
        name = "_".join([args.outdir, col, "ord.png"])
        save_graph(f, name, args.dry_run)

    if not args.outdir and not args.dry_run:
      plt.show()
    sys.exit(1)
