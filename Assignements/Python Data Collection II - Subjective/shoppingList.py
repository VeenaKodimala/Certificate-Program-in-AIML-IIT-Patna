'''You have a shopping list with items and their prices:

shopping_list = [
    {"item": "Milk", "price": 50},
    {"item": "Bread", "price": 30},
    {"item": "Eggs", "price": 60},
    {"item": "Rice", "price": 120}
]
Complete the following tasks:

Task 1: Add and Remove Items (30 points)
Add a new item {"item": "Butter", "price": 80} to the shopping list
Remove the first item from the list using .pop(0)
Print how many items are in the list now
Task 2: Calculate Total Cost (35 points)
Calculate the total cost of all items in the shopping list
Find the most expensive item and print its name and price
Print the total cost
Task 3: Create Summary Dictionary (35 points)
Create a dictionary called summary with:
"total_items": Number of items in the list
"total_cost": Total price of all items
"average_price": Average price per item (round to 2 decimals)
Print the summary dictionary
'''

shopping_list = [
    {"item": "Milk", "price": 50},
    {"item": "Bread", "price": 30},
    {"item": "Eggs", "price": 60},
    {"item": "Rice", "price": 120}
]

shopping_list.append({"item": "Butter", "price": 80})
shopping_list.pop(0)
print(f"No.of items in list: {len(shopping_list)}")

totalCost = 0
maxCost = 0
maxItem=''
for i in range(len(shopping_list)):
    element = shopping_list[i]
    totalCost = totalCost + element.get("price")
    if maxCost < element.get("price"):
        maxCost = element.get("price")
        maxItem = element.get("item")

print(f"Total cost: {totalCost}")
print(f"Expensive item: {maxItem}, cost : {maxCost}") 

summary = {'No.of Items':len(shopping_list),'Total Cost': totalCost, 
           "Average Cost":round(totalCost/len(shopping_list),2)}

print(f"Summary: {summary}")
