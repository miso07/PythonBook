import matplotlib.pyplot as plt
import FinanceDataReader as fdr


df   = fdr.DataReader('BTC/USD', '2021')
df_1 = fdr.DataReader('ETH/USD', '2021')
df_2 = fdr.DataReader('SOL/USD', '2021')

print(df)

my_crypto = df_1
plt.figure(figsize=(10, 8))
for c in my_crypto.columns.values:
    plt.plot(my_crypto[c], alpha=0.7, lw = 2)
plt.title("Cryptocurrencies Graph")
plt.xlabel('Months')
plt.ylabel('Crypto Price USD($)')
plt.legend(my_crypto.columns.values, loc = 'upper left')
plt.show()

