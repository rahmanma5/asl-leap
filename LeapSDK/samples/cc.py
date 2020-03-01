def coinChange(coins, amt):
    totalCoins = 0
    for coin in reversed(coins):
        numOfCoins = amt // coin
        totalCoins += numOfCoins
        amt -= coin * numOfCoins
    return totalCoins

coins = [1,3,4,10,25]
amt = 42

print(coinChange(coins,amt))