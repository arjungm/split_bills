import argparse

def read_transaction_file(fhandle):
    tip = 0
    transactions = [];

    for line in fhandle:
        elems = line.strip().split(',')
        # the first elem is the price of the item in the transaction
        price = float(elems[0])
        # the rest of the elems is a participant
        participants = [str(e) for e in elems if e!=elems[0]]
        
        if( (len(participants)==1) and (participants[0] == "!tip") ):
            tip = price
        else:
            transactions.append( {'price': price, 'participants': participants} )
    return (transactions, tip)

def compute_subtotals(transactions):
    subtotals = {}
    for transact in transactions:
        num_parts = len(transact['participants'])
        cost_per_part = transact['price'] / num_parts
        for part in transact['participants']:
            subtotals[part] = cost_per_part + subtotals.get(part,0.0)
    return subtotals

def compute_contribution(subtotals, common):
    total = sum(subtotals.values())
    subcontribs = {part: common*subtotal/total for (part,subtotal) in subtotals.items()}
    return subcontribs

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('fhandle', type=argparse.FileType('r'))
    args = parser.parse_args()
    fhandle = args.fhandle

    transactions, tip_total = read_transaction_file(fhandle)
    subtotal_pp = compute_subtotals(transactions)

    subtotal = sum(subtotal_pp.values())

    # tax_pp is (subtotal_pp / subtotal_all) * tax_total
    tax_total = subtotal * (8.75/100.0)
    tax_pp = compute_contribution(subtotal_pp, tax_total)
    
    tip_pp = compute_contribution(subtotal_pp, tip_total)

    # for each participant, final amount owed is the sum of subtotal, tax, tip
    for part in subtotal_pp.keys():
        amount = subtotal_pp[part] + tax_pp[part] + tip_pp[part]
        print '{0} owes {1}'.format(part, amount)

if __name__=="__main__":
    main()
