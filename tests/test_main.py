import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #otherwise, this file cannot find main.py
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from main import count_oposed_and_supported_counts, count_bill_supporters_and_opposers


def test_count_opposed_and_supported_counts():
    legislators = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob']
    })
    votes = pd.DataFrame({
        'id': [10, 20],
        'bill_id': [100, 200]
    })
    vote_results = pd.DataFrame({
        'vote_id': [10, 20, 10],
        'legislator_id': [1, 2, 1],
        'vote_type': [1, 2, 2]  # 1=support, 2=oppose
    })
    print("Input: legislators\n", legislators)
    print("Input: votes\n", votes)
    print("Input: vote_results\n", vote_results)
    expected = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob'],
        'num_supported_bills': [1, 0],
        'num_opposed_bills': [1, 1]
    })
    print("Expected output:\n", expected)
    result = count_oposed_and_supported_counts(legislators, votes, vote_results)
    print("Actual output:\n", result)
    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True))


def test_count_bill_supporters_and_opposers():
    bills = pd.DataFrame({
        'id': [100, 200],
        'title': ['Bill A', 'Bill B'],
        'sponsor_id': [1, 2]
    })
    legislators = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob']
    })
    votes = pd.DataFrame({
        'id': [10, 20],
        'bill_id': [100, 200]
    })
    vote_results = pd.DataFrame({
        'vote_id': [10, 20, 10],
        'legislator_id': [1, 2, 1],
        'vote_type': [1, 2, 2]
    })
    print("Input: bills\n", bills)
    print("Input: legislators\n", legislators)
    print("Input: votes\n", votes)
    print("Input: vote_results\n", vote_results)
    expected = pd.DataFrame({
        'id': [100, 200],
        'title': ['Bill A', 'Bill B'],
        'supporter_count': [1, 0],
        'opposer_count': [1, 1],
        'primary_sponsor': ['Alice', 'Bob']
    })
    print("Expected output:\n", expected)
    result = count_bill_supporters_and_opposers(bills, legislators, votes, vote_results)
    print("Actual output:\n", result)
    #compare relevant columns
    assert_frame_equal(result[['id','title','supporter_count','opposer_count','primary_sponsor']].reset_index(drop=True), expected.reset_index(drop=True))
