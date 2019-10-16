#!/usr/bin/python3
import requests

# the "seperator" just a line of = to make the output easier to read
erottimet = ""
for x in range(30): 
    erottimet += "="

# a global attribute used to determine either to print currenct currency or converted currency
IsChanged = True

# a list of global currencies that are taken form the european banks api
valuutat = requests.get('https://api.exchangeratesapi.io/latest').text

# a list of options for the user to pick their currency from
option = valuutat.split(',')
options = option[:-1]

# The function called to print the list of options for the user to pick their currency form
#TO DO: make list look better in output (Currently hard to read)
def userPickOption(options):
    while True:
        print("please choose a number from 1-33")
        for idx, element in enumerate(options):
                if element.startswith('{'):
                    element = element.replace('{"rates":{','')
                if element.startswith('"MYR"'):
                    element = element.replace('}','') 
                print("{}) {}".format(idx+1,element.replace('"',"")))
        i = input("Enter Number: ")
        print(erottimet)
        try: 
            if 0 < int(i) <=len(options):
                return int(i)
                break
        except (TypeError, ValueError) as e:
            print(e)

# the function called to ask the user to pick their currency 
def selectCurrency(options):
    global IsChanged
    if IsChanged == True:
        print("Select your currency")
    else:
        print("Select the currency you want to convert to")
    indexnum = userPickOption(options)-1
    IsChanged = False
    if indexnum == 0:
        currency = "CAD"

    elif indexnum == 32:
        currency = "EUR"
    else:
        currency = options[indexnum].split('"')[1]
    return currency

# gets the current value from the european banks api
def getValue(currency):
    global valuutat
    if (currency == "EUR" or currency =="eur"):
        return 1.00
    value = valuutat.find(currency.upper())
    valueEND = value + 10
    value1 = valuutat[value:valueEND]
    value2 = value1.split(":")[1]
    return float(value2)

# c = a x b
# a = your money
# b = exchange rate
# the formula used to convert the currencies 
def calculateCurrency(value, value1, amount):
    awnser = float(amount) / value
    awnser1 = awnser*value1
    return awnser1

# the currency you currently have
currency = selectCurrency(options)

print("Please enter your amount of currency")

# asks the user for the amount of currency they want to convert. If the input is not a number than it asks for input again
while True:
    try:
        amount = input()
        test = float(amount)
        if test < 0:
            raise ValueError
        break
    except ValueError:
        print("Not a number!")

# the currency you want to convert to 
currency1 = selectCurrency(options)

# the values that are used
value = getValue(currency)
value1 = getValue(currency1)

print("Your currency was: " + currency.upper() + " " + str(amount) + "\n" + "you wanted to convert to: " + currency1.upper() + "\n" + amount + " " + currency.upper() + " in " + currency1.upper() +" is: " + str(float("{0:.2f}".format(calculateCurrency(value, value1, amount)))) + "\n" + erottimet)
