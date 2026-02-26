"""
Real-World Use Case
Primary Use Case: Weekly Budget Management for Students
Scenario: A college student receives $100 weekly allowance and needs to track spending on:
Food and drinks
School supplies
Entertainment
Transportation
I
Problem Statement: Without tracking, students often overspend early in the week and run out of money. This program helps them:
Know exactly how much they have left
Check if they can afford items before buying
Calculate discounts to find better deals
See their spending patterns

"""


def showWelcome():
    print('\n WELCOME TO BUDGET TRACKER!!!!')
    print('-' * 40)

def getBudgetStatus(budget,spent):
    remaining = budget - spent
    percentage = (remaining/budget)*100

    print(f"Budget: {budget:.2f}")
    print(f"Spent: {spent:.2f}")
    print(f"Remaining: {remaining:.2f}")
    print(f"Percentage of amount left: {percentage:.1f}% left")

    if(remaining > budget * 0.5):
        print("\nFinancial Status: Green")
    elif(remaining > 0 and remaining <= budget*0.5):
        print("\nFinancial Status: Amber")    
    else:
        print("\nFinancial Status: Red")   

    return remaining


def canBuy(itemPrice,remainingAmt):
    if(itemPrice > 0 and itemPrice >= remainingAmt):
        return False
    else:
        return True

def calculateDiscount(itemPrice,discountPerc):
    discountAmt = itemPrice*(discountPerc/100)

    finalPrice = itemPrice - discountAmt
    print(f"Original Price: {itemPrice}")
    print(f"Discount Percentage: {discountPerc}, Discount Amount: {discountAmt}")
    print(f"Final Price: {finalPrice}")

    return finalPrice

def mainMenu():
    showWelcome()

    budget = float(input("\nEnter your weekly budget: Rs"))
    total_spent = 0
    purchaseCount = 0
    keepGng = True

    while keepGng:
        remaining = getBudgetStatus(budget,total_spent)

        print("=" * 40)
        print("MENU")
        print("1. Add a purchase")
        print("2. Purchase multiple items")
        print("3. Calculate discount Price")
        print("Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            print("-------------ADD A PURCHASE----------------")
            itemName = input("Enter item name: ")
            itemPrice = float(input("Enter item price: "))
            
            if canBuy(itemPrice,remaining):
                Confirm = input(f"Buy {itemName} for {itemPrice:.2f} (yes/no): ")
                if Confirm.lower() == 'yes':
                    total_spent = total_spent + itemPrice
                    purchaseCount += 1
                    print(f"Purchased {itemName}")
                else:
                    print(f"Purchase of {itemName} cancelled by user.")    
            else:
                shortage = itemPrice - remaining
                print(f"Shortage of {shortage}, so cannot afford {itemName}")
            remaining = getBudgetStatus(budget,total_spent)

        elif choice == 2:
            print("\n------------MULTIPLE ITEMS----------")
            print("\nEnter item names (type done to finish!): ")
            item_count = 0
            cartTotal = 0
            while True:
                item = input(f"\nItem {item_count + 1} Name (or done): ")
                if item == 'done':
                    break
                if item == '':
                    print("Itemname is empty, please try again")

                price = float(input("Enter item's price: "))

                if price <= 0:
                    print("Invalid price, please try again")
                    continue

                cartTotal += price
                item_count += 1
                print(f"Added {item}")

            if item_count <= 0:
                print("No items added")
            else:
                print(f"Count of items added:{item_count}, Cart total: {cartTotal} ")

                affordable = cartTotal <= remaining
                resonable = cartTotal <= remaining * 0.7

                if affordable and resonable:
                    print("Safe to buy")
                elif affordable and not resonable:
                    print("Affordable, but budget becomes tight")      
                else:
                    print("Cannot affort it")

                if affordable:
                    Confirm = input(f"Proceed with the purchase (yes/no): ")
                    if Confirm.lower() == 'yes':
                        total_spent += cartTotal
                        purchaseCount += item_count
                        print("Purchase complete!!!")
     
        elif choice == 3:
            print("------------DISCOUNT CALCULATOR-----------")
            originalprice = float(input("Original price of the item: "))
            discountPerc = float(input("Enter discount percentage offered: "))

            finalPrice = calculateDiscount(originalprice, discountPerc)
            
            if canBuy(originalprice,remaining):
                print("You can afford this")
            else:
                print("Sorry, you cannot afford this")    
        elif choice == 4:
            keepGng = False
            print("Exiting application.....")
        else:
            print("Invalid choice")    



mainMenu()
