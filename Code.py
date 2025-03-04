#import Libraries

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns


#Loading dataset file

df = pd.read_csv('housePrice.csv')
print(df.shape)
print(df.head())

# remove Nan and outlier with IQR
df = df.dropna()

Q1 = df['Price(USD)'].quantile(0.25)
Q3 = df['Price(USD)'].quantile(0.75)
IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

df = df[(df['Price(USD)'] >= lower_bound) & (df['Price(USD)'] <= upper_bound)]
df.index = range(1, len(df) + 1)

print(df.shape)
print(df)

# Remove extra character and converting data

df['Price(USD)'] = pd.to_numeric(df['Price(USD)'])
df['Area'] = pd.to_numeric(df['Area'], errors='coerce')


df['Price(USD)'] = df['Price(USD)'].astype(str).str.replace(' ', '').str.replace(',', '').astype(float)
df['Area'] = df['Area'].astype(str).str.replace(' ', '').str.replace(',', '').astype(float)


# 1. What is the average price of houses in different areas?
mean_prices = df.groupby('Address')['Price(USD)'].mean().reset_index(name='Mean Price(USD)')
mean_prices.index = range(1, len(mean_prices) + 1)

print(mean_prices[['Address', 'Mean Price(USD)']])

#2. How many houses are there in each area?
home_count = df.groupby('Address')['Area'].count().reset_index(name='Home Count')
home_count.index = range(1, len(home_count) + 1)

print(home_count[['Address', 'Home Count']])

#3. What is the relationship between the area of a house and its price?
plt.figure(figsize=(12, 6))
sns.lineplot(x=df['Area'], y=df['Price(USD)'], color='blue')
plt.title('Relationship between Area and Price')
plt.xlabel('Area(m2)')
plt.ylabel('Price(USD)')
plt.grid(True)

area_per_price_figure = plt.gcf()

plt.show()

#4. Does the number of rooms (Room Column) affect the price of a house?
plt.figure(figsize=(12, 6))
sns.lineplot(x=df['Room'], y=df['Price(USD)'], color='blue')
plt.title('Relationship between Room num and Price')
plt.xlabel('Room(num)')
plt.ylabel('Price(USD)')
plt.grid(True)

room_per_price_figure = plt.gcf()

plt.show()

#5. Which area has the most expensive houses, and which area has the cheapest houses?
most_expensive_area = df[df['Price(USD)'] == df['Price(USD)'].max()]['Address']
cheap_expensive_area = df[df['Price(USD)'] == df['Price(USD)'].min()]['Address']

print("most expensive houses area: ",most_expensive_area)
print("cheapest expensive houses area: ",cheap_expensive_area)


#6. Which area has the highest number of houses with parking?
houses_with_parking = df[df['Parking'] == True]

parking_count_by_address = houses_with_parking.groupby('Address').size()

highest_num_house_parking = parking_count_by_address.idxmax()
max_count = parking_count_by_address.max()

area_most_parking_house_num = (df['Area'] == highest_num_house_parking).count()

print(f"Area with highest number of houses with parking: {highest_num_house_parking} (Total Parking: {max_count} , Total House: {area_most_parking_house_num} , Parking per house: {max_count / area_most_parking_house_num }) ")

#7. Can you buy a two-room house or a house with parking for $250,000?
can_buy_2room = df[(df['Room'] == 2) & (df['Price(USD)'] <= 250000)]
can_buy_parking = df[(df['Parking'] == True) & (df['Price(USD)'] <= 250000)]

can_buy = pd.concat([can_buy_2room, can_buy_parking])

can_buy = can_buy.drop_duplicates()

can_buy = can_buy.sort_values(by='Price(USD)')

can_buy = can_buy.reset_index(drop=True)
can_buy.index = range(1, len(can_buy) + 1)

print(f"Num of Houses with 2-Room: {can_buy_2room.shape[0]} , Num of Houses with Parking: {can_buy_parking.shape[0]} , Total: {can_buy.shape[0]}" ) 
print(can_buy)

#8. Find the 10 most expensive areas and the 10 cheapest areas.
ten_expensive = df.sort_values('Price(USD)', ascending=False)['Address'].reset_index(drop=True).head(10)
ten_expensive.index = range(1, 11)  

ten_cheapest = df.sort_values('Price(USD)')['Address'].reset_index(drop=True).head(10)
ten_cheapest.index = range(1, 11) 

print('10 Expensive House:')
print(ten_expensive)

print()

print('10 Cheapest House:')
print(ten_cheapest)



#Save Result
area_per_price_figure.savefig('area_vs_price.png', dpi=300, bbox_inches='tight')
room_per_price_figure.savefig('room_vs_price.png', dpi=300, bbox_inches='tight')

df.to_csv('df.csv', index=False)
mean_prices.to_csv('mean_prices_area.csv', index=False)
home_count.to_csv('home_count_area.csv', index=False)
houses_with_parking.to_csv('houses_with_parking.csv', index=False)
can_buy_2room.to_csv('house_250k_2room.csv', index=False)
can_buy_parking.to_csv('house_250k_parking.csv', index=False)
can_buy.to_csv('house_parking_2room_250k.csv', index=False)
ten_cheapest.to_csv('ten_cheapest_area.csv', index=True)
ten_expensive.to_csv('ten_expensive_area.csv', index=True)

#Github.com/RezaGooner
