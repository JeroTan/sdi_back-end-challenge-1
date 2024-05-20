#import dependencies
import json;

#Load Table
with open("tableData.json", "r") as file:
    carTable = json.load(file)

#insert the data
carTable = carTable["carRentalTable"]

#makeThe number integers
for car in carTable:
    car["seat"] = int(car["seat"])
    car["cost"] = int(car["cost"])

#sort the cost
carTable = sorted(carTable, key=lambda e: e['cost'])

seats = False
while seats == False:
    seats = input("Please input number of (seats)? ")

    if (not seats.isnumeric()) or int(seats) == 0:
        print("Invalid input please try again")
        seats = False
    else:
        seats = int(seats)


#define the algorithm
def lookForLowestCost(remainingSeats):
    #print("%d " % (remainingSeats), end="")
    preferredCar = False #Initiate Preferred car

    #Select the Highest Seat Car since it is the least expensive. With this we will know the threshold of the data so that we can recurse again to calculate the data
    currentHighestSeat = 0
    for car in carTable:
        if car["seat"] > currentHighestSeat:
            currentHighestSeat = car["seat"]
            preferredCar = car

    #This one will be used to check whether the remaining seats is still applicable to the ratio of given car data seats
    currentLowestSeat = 999999999999
    lowestCarSeat = preferredCar
    for car in carTable:
        if car["seat"] < currentLowestSeat:
            currentLowestSeat = car["seat"]
            lowestCarSeat = car


    for car in carTable:
        if car["seat"] >= remainingSeats and preferredCar["seat"] >= remainingSeats :
            preferredCar = car
            break

    #Since we finally narrow down the preferred car we need to cut down the remainingSeats
    remainingSeats = remainingSeats - preferredCar["seat"]

    #This will be the result to return
    result = {
        preferredCar["size"]: {"cost":preferredCar["cost"], "total":1, "seat":preferredCar["seat"]}
    }

    # The first case to return a recursive function
    if remainingSeats <= 0:
        return result
    
    #recursion to check other stuff
    otherResult = lookForLowestCost(remainingSeats)

    
    for props in otherResult:
        if props in result:
            result[props]["total"] = result[props]["total"] + otherResult[props]["total"]
        else:
            result[props] = {"cost":otherResult[props]["cost"], "total":otherResult[props]["total"], "seat":otherResult[props]["seat"]}

    return result


#run the algorithm

print("processing", end="")
result = lookForLowestCost(seats)
print("")
print("Here is the result:")
print(result)

print("For your '%d' seat(s), you may avail the following: " %(seats))
cost = 0
i = 0
totalCapacity = 0
for props in result:
    if i != 0:
        print(" + ")
    data = result[props]
    print("%s x %d" %(props, data["total"]), end="")
    i = i + 1
    #compute the total cost along the way
    cost = cost + data["cost"]*data["total"]
    #... and also the total capacity of seats 
    totalCapacity = totalCapacity + data["total"]*data["seat"]
print("")
print("Which cost Php %d" %(cost), end="")
if totalCapacity > seats:
    print(", with additional %d seat(s) allowance" %(totalCapacity-seats))
