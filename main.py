import os
import pandas as pd
from pandas import DataFrame

DATA_DIR = "data"
OUTPUT_DIR = "output"
LEGISLATORS_FILE = os.path.join(DATA_DIR, "legislators.csv")
BILLS_FILE = os.path.join(DATA_DIR, "bills.csv")
VOTES_FILE = os.path.join(DATA_DIR, "votes.csv")
VOTE_RESULTS_FILE = os.path.join(DATA_DIR, "vote_results.csv")
LEGISLATORS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "legislators-support-oppose-count.csv")
BILLS_OUTPUT_FILE = os.path.join(OUTPUT_DIR, "bills.csv")

def load_input_data() -> tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    legislators_df = pd.read_csv(LEGISLATORS_FILE)
    bills_df = pd.read_csv(BILLS_FILE)
    votes_df = pd.read_csv(VOTES_FILE)
    vote_results_df = pd.read_csv(VOTE_RESULTS_FILE)
    return legislators_df, bills_df, votes_df, vote_results_df

"""
1. For every legislator in the dataset, how many bills did the legislator support (voted for the
bill)? How many bills did the legislator oppose?
2. For every bill in the dataset, how many legislators supported the bill? How many legislators
opposed the bill? Who was the primary sponsor of the bill?
"""

def count_oposed_and_supported_counts(
    legislators: pd.DataFrame,
    votes: pd.DataFrame,
    vote_results: pd.DataFrame
) -> pd.DataFrame:

    #merge vote_results with votes to get bill_id
    vote_details = vote_results.merge(votes, left_on="vote_id", right_on="id", suffixes=('_vr', '_vote'))

    #supports and oppositions per legislator
    legislator_stats = (
        vote_details
        .groupby(['legislator_id', 'vote_type'])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    legislator_stats = legislator_stats.rename(columns={
        1: 'num_supported_bills',
        2: 'num_opposed_bills'
    })

    legislator_summary = (legislators.merge(
        legislator_stats,
        how='left',
        left_on='id',
        right_on='legislator_id'
    )
                          .fillna({'num_supported_bills': 0, 'num_opposed_bills': 0})
                          .astype({'num_supported_bills': int, 'num_opposed_bills': int}))

    #return required columns
    legislator_summary = legislator_summary[[
        'id', 'name', 'num_supported_bills', 'num_opposed_bills'
    ]]

    return legislator_summary

def count_bill_supporters_and_opposers(
    bills_df: pd.DataFrame,
    legislators_df: pd.DataFrame,
    votes_df: pd.DataFrame,
    vote_results_df: pd.DataFrame
) -> pd.DataFrame:
    #get bill_id from vote results (vr) and vote id
    vr_with_bills = vote_results_df.merge(
        votes_df,
        left_on="vote_id",
        right_on="id",
        suffixes=('_vr', '_vote')
    )

    #supporters and opposers for each bill
    bill_votes = (
        vr_with_bills
        .groupby(['bill_id', 'vote_type'])
        .size()
        .unstack(fill_value=0)
    )
    bill_votes = bill_votes.rename(columns={
        1: 'supporter_count',
        2: 'opposer_count'
    })

    bills_with_counts = bills_df.merge(
        bill_votes,
        left_on="id",
        right_index=True,
        how="left",
    )
    bills_with_counts[["supporter_count", "opposer_count"]] = (
        bills_with_counts[["supporter_count", "opposer_count"]]
        .fillna(0)  #bills with no votes get 0
        .astype(int)
    )

    #get primary sponsor and return their name
    bills_with_counts = bills_with_counts.merge(
        legislators_df[['id', 'name']],
        left_on='sponsor_id',
        right_on='id',
        how='left',
        suffixes=('', '_sponsor')
    )
    bills_with_counts['primary_sponsor'] = bills_with_counts['name'].fillna('Unknown')
    result = bills_with_counts[[
        'id', 'title', 'supporter_count', 'opposer_count', 'primary_sponsor'
    ]]
    return result

#entrypoint
def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    legislators_df, bills_df, votes_df, vote_results_df = load_input_data()

    legislator_summary = count_oposed_and_supported_counts(
        legislators_df,
        votes_df,
        vote_results_df
    )
    legislator_summary.to_csv(LEGISLATORS_OUTPUT_FILE, index=False)

    bill_summary = count_bill_supporters_and_opposers(
        bills_df,
        legislators_df,
        votes_df,
        vote_results_df
    )
    bill_summary.to_csv(BILLS_OUTPUT_FILE, index=False)
    print("Done. Check the results in the **Output** folder.")

if __name__ == "__main__":
    main()

