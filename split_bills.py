# returns a tuple summarizing the receipt of the transactions:
# 0: tip            the flat dollar amount of tip added to the bill
# 1: transactions   list of dicts (of price, and participant list)
def parse_transactions(lines):
    tip = 0.0
    transactions = [];

    for line in lines:
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
    
def get_baked_list():
  ret = """7.51,!tip
  14.95,p1
  13.95,p2
  12.95,p3
  3.95,p3
  3.5,p2"""
  return ret.split('\n')

# for each item in the transaction, compute the item_price_per_participant
#  if it was split evenly between all participants
# then for each participant, add together all item_price_per_participant 
#  that they are a part of
def compute_subtotals(transactions):
    subtotals_per_participant = {}
    for transact in transactions:
        num_participants_per_item = len(transact['participants'])
        cost_per_participants = transact['price'] / num_participants_per_item
        for part in transact['participants']:
            subtotals_per_participant[part] = cost_per_participants + subtotals_per_participant.get(part,0.0)
    return subtotals_per_participant

# given a list of subtotals per participant,
# compute a proportional split of the common item's price (tax, tip, etc)
def compute_contribution(subtotals, common):
    total = sum(subtotals.values())
    subcontribs = {part: common*subtotal/total for (part,subtotal) in subtotals.items()}
    return subcontribs

def main():
    transactions, tip_total = parse_transactions(get_baked_list())
    subtotal_pp = compute_subtotals(transactions)

    subtotal = sum(subtotal_pp.values())

    # tax_pp is (subtotal_pp / subtotal_all) * tax_total
    tax_total = subtotal * (8.5/100.0)
    
    print('{:9} = {:04.2f}'.format('subtotal',subtotal))
    print('{:9} = {:04.2f}'.format('tax',     tax_total))
    print('{:9} = {:04.2f}'.format('total',   tax_total+subtotal))
    
    tax_pp = compute_contribution(subtotal_pp, tax_total)
    
    tip_pp = compute_contribution(subtotal_pp, tip_total)

    # for each participant, final amount owed is the 
    #  sum of subtotal, tax, tip (as calculated per participant)
    print()
    print('Result:')
    for participant in subtotal_pp.keys():
        amount = subtotal_pp[participant] + tax_pp[participant] + tip_pp[participant]
        print('{:7} owes {:04.2f}'.format(participant, amount))

if __name__=="__main__": main()
