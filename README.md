`split_bills.py`
a dumb utility script to do proportional split of itemized receipts

input a csv where each line is an item on the receipt, with the first token being the amount, and rest of the line is either:
* `!tip` identifier for the tip amount (which will be split proportionally, just like the tax)
* a list of all participants splitting an item
