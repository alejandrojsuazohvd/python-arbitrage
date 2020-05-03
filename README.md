# python-arbitrage
### Developed by Alejandro Suazo
This is a python arbitrage application that trades currencies between Zcash, Bitcoin, and Etherium.

We have prices of trade pairs
```
if AB, BC, CA, BA, CB, and AC
     then if the ratio of price between AB is ratio_1, AC is ratio_2, CB is ratio_3
        if ratio_1 > ratio_2 & ratio_3
             then trade A -> C -> B -> A
```
Ex: If the ratios are as follows
```    
2:4 > 1:2 & 2:3
   then A -> C -> B -> A would have a 50% return on investment.
``` 

Then the algorithm continues to do this comparison. BTC is the most truthful orderbook so we will keep our running balance on BTC
2nd problem: trade fees.
So I determined the maximum fees per trade and the GAIN after the trade has COVER the fee costs.
so this now requires the algorithm to determine potential gain on prior to committing a transaction
The condition is as follows
```
if ratio_AB > ratio_AC & ratio_CB
   AND ratio_AC & ratio_CB & ratio_BA > fee %
      then trade A -> C -> B -> A
```

