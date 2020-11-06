
def calculate_gasp(order_book):
    bids = order_book['bids']
    asks = order_book['asks']
    numerator = 0
    denominator = 0
    bid_idx = 0
    ask_idx = 0

    while True:
        try:
            bid_price = bids[bid_idx][0]
            bid_qty = bids[bid_idx][1]

            ask_price = asks[ask_idx][0]
            ask_qty = asks[ask_idx][1]

            if bid_qty < ask_qty:
                numerator = numerator + (bid_qty * bid_price + bid_qty * ask_price)
                # print("{0} * {1} + {2} * {3}".format(bid_qty, bid_price, bid_qty, ask_price))
                bid_idx = bid_idx + 1
                denominator = denominator + 2 *  bid_qty
                asks[ask_idx][1] = ask_qty - bid_qty
            elif ask_qty < bid_qty:
                numerator = numerator + (ask_qty * bid_price + ask_qty * ask_price)
                # print("{0} * {1} + {2} * {3}".format(ask_qty, ask_price, ask_qty, ask_price))
                denominator = denominator + 2 * ask_qty
                ask_idx = ask_idx + 1
                bids[bid_idx][1] = bid_qty - ask_qty
        except IndexError:
            break
    # print("Numerator", numerator)
    # print("Denominator", denominator)
    return numerator / denominator

if __name__ == "__main__":

# 1 [ 321.7 , 165.0 ] [ 321.75 , 5.0  ]
# 2 [ 321.65 , 128.0] [ 321.8 , 100.0 ]
# 3 [ 321.6 , 134.0 ] [ 321.85 , 109.0]
# 4 [ 321.55 , 109.0] [ 321.9 , 110.0 ]
# 5 [ 321.5 , 134.0 ] [ 321.95 , 119.0]
# 시간#{0}, GASP: {1} 150514 111.29314365671642

  order_book = {
    'bids': [
      [ 321.7 , 165.0 ],
      [ 321.65 , 128.0],
      [ 321.6 , 134.0 ],
      [ 321.55 , 109.0],
      [ 321.5 , 134.0 ]
    ],
    'asks': [
      [ 321.75 , 5.0  ],
      [ 321.8 , 100.0 ],
      [ 321.85 , 109.0],
      [ 321.9 , 110.0 ],
      [ 321.95 , 119.0]  
    ]
  }
  gasp = calculate_gasp(order_book)

  print('GASP :', gasp)