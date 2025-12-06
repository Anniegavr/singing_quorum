# A small project to analyse bills voting data
### For project setup, please refer to INSTRUCTION.md.
### To test the correctness of the fucntionality, please run the tests (refer to section 6 in INSTRUCTION.md).

## Write-up

### 1) Time complexity & tradeoffs
- Dominated by processing n = rows in `vote_results`: group-bys/joins ≈ O(n).

Tradeoffs: simple pandas was used, for clarity, speed and considering the small input
- The script could aggregate-before-join to reduce memory. The count_oposed_and_supported_counts() method merges vote_results→votes before aggregating.
This is correct, but creates a larger intermediate set than necessary. A group‑by first, then join approach reduces peak memory and may be faster on large data.

Why the current way was chosen: pragmatism. We do not encounter a big dataset here. However, in a real-life scenario, reducing the dataset to only-necessarry dimmensions
is always a must, even though it takes more time to deliver. Any waste of time and memory is money. In case of a bigger dataset and processing requirement, Spark or other solution shall replace
Pandas, as this library works in-memory and RAM is always expensive, plus it cannot split tasks in parralel coroutines for time efficiency.

### 2) Future columns account
How would you change your solution to account for future columns that might be
requested, such as “Bill Voted On Date” or“Co-Sponsors”?
Answer:
- *Bill Voted On Date*: Add voted_on to votes; after computing counts, merge to bills.
- *Sponsors*: Add co_sponsors column (bill_id, legislator_id); join to legislators for names, then aggregate per bill (count and/or comma‑separated names).

### 3) If inputs were lists (not CSVs)
- Convert the list into tiny dataframes;
- Filter early through the data (taking into account the tradeoffs of the current solution and fixing them);
- Reuse the same grouping/merging logic; output same schemas.

### 4) Time spent
- ~2 hours for code + test ~and 45 minutes for polishing and write up.

