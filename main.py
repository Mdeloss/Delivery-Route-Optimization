# Mariano De Los Santos, Student ID 001523416

import csv
from datetime import timedelta

# HashTable class using chaining.
from Hash import ChainingHashTable


# Truck class that will be defined later
class Truck:
    pass


# Package class that will be defined later
# String value format added
class Package:
    def __repr__(self):
        return "{}".format(self.ID)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}".format(self.ID, self.Address, self.City, self.State,
                                                                   self.Zip,
                                                                   self.DeliveryTime, self.Weight, self.Notes,
                                                                   self.Status,
                                                                   self.StatusDelTime, self.TruckNumber)

    pass


# Hash table instance saved into hashTablePackages
hashTablePackages = ChainingHashTable()


# O(n^2) time and O(n) space
# Load packages by ID onto trucks using greedy algorithm
# Create package object from CSV directory
# Load packages into hash table
# Includes package 9 address correction
def loadPackageData(fileName, thisHashTable):
    with open(fileName) as packageData:

        packageFileData = csv.DictReader(packageData)
        # Temporary lists for package organization
        tempList = []
        tempList2 = []
        # Iterate through packageFileData
        for row in packageFileData:

            # Package object
            p = Package()
            p.ID = int(row['ID'])
            p.Address = row['Address']
            p.City = row['City']
            p.State = row['State']
            p.Zip = row['Zip']
            p.DeliveryTime = row['DeliveryTime']
            p.Weight = int(row['Weight'])
            p.Notes = row['Notes']
            p.Status = 'Hub'
            p.StatusDelTime = timedelta(hours=0, minutes=0, seconds=0)
            p.TruckNumber = int(0)

            # insert into the hash table
            thisHashTable.insert(p.ID, p)

            # First round of loading
            # Load trucks stopping at 16 packages
            # Filter by earliest delivery time and special notes
            # Truck 1
            if len(truck1.loadedPackages) < 16:
                if p.DeliveryTime == '10:30 AM' or p.DeliveryTime == '9:00 AM':
                    if p.Notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
                        truck2.loadedPackages.append(p.ID)
                        p.TruckNumber = 2
                        continue
                    truck1.loadedPackages.append(p.ID)
                    p.TruckNumber = 1
                    continue
                if p.ID == 19 or p.ID == 4 or p.ID == 39 or p.ID == 27:
                    truck1.loadedPackages.append(p.ID)
                    p.TruckNumber = 1
                    continue
            # Truck 2
            if len(truck2.loadedPackages) < 16:
                if p.Notes == 'Can only be on truck 2':
                    truck2.loadedPackages.append(p.ID)
                    p.TruckNumber = 2
                    continue
                if p.Notes == 'Delayed on flight---will not arrive to depot until 9:05 am':
                    truck2.loadedPackages.append(p.ID)
                    p.TruckNumber = 2
                    continue
            # Truck 3
            if len(truck3.loadedPackages) < 16:
                if p.Notes == 'Wrong address listed':
                    truck3.loadedPackages.append(p.ID)
                    p.TruckNumber = 3
                    continue

            # If not loaded, add to temp list
            tempList.append(p.ID)
            continue

    # Second round of loading
    # O(n^2) time complexity
    # Filter by matching zip codes
    # Search for matching Zip between tempList and truck 2
    # Add matches to trucks 2
    for i in tempList:
        f = hashTablePackages.search(i)
        if len(truck2.loadedPackages) < 16:
            for j in truck2.loadedPackages:
                k = hashTablePackages.search(j)
                if f.Zip == k.Zip:
                    truck2.loadedPackages.append(i)
                    f.TruckNumber = 2
                    break  # break to check next item in tempList

    # Function to load the rest of packages
    # consolidate trucks 1, 2, and 3
    for i in truck1.loadedPackages:
        tempList2.append(i)
    for i in truck2.loadedPackages:
        tempList2.append(i)
    for i in truck3.loadedPackages:
        tempList2.append(i)

    # Find intersection between tempList2 and tempList
    t = set(tempList).intersection(tempList2)
    for i in t:
        tempList.remove(i)  # Remove found packages from tempList

    #  Add tempList to trucks 1, 2, and 3
    for i in tempList:

        if len(truck1.loadedPackages) < 16:
            truck1.loadedPackages.append(i)
            p = hashTablePackages.search(i)
            p.TruckNumber = 1
            continue
        if len(truck2.loadedPackages) < 16:
            truck2.loadedPackages.append(i)
            p = hashTablePackages.search(i)
            p.TruckNumber = 2
            continue
        if len(truck3.loadedPackages) < 16:
            truck3.loadedPackages.append(i)
            p = hashTablePackages.search(i)
            p.TruckNumber = 3

    # Update Hash Table with package 9 new address
    new = hashTablePackages.search(9)
    new.Address = '410 S State St'
    new.City = 'Salt Lake City'
    new.State = 'UT'
    new.Zip = '84111'
    new.Notes = 'Address corrected'


# O(n) time and space
# Definition that returns distance using addresses.csv
# Called within truck delivery definitions
def getDistance(fileName, curAddress, destAddress):
    with open(fileName) as address:
        addressData = csv.reader(address)

        # index used to look up reverse address
        # if distance value is empty
        a1 = ''
        a2 = ''
        index = 0
        index1 = 0
        index2 = 0

        # Search for address distance in addresses csv file by row number
        for row in addressData:
            index = index + 1  # Row number

            # Find first address and assign row to a1
            # Assign row number to index1
            if row[0] == curAddress:
                a1 = row
                index1 = index
            # Find second address and assign row to a2
            # Assign row number to index2
            if row[0] == destAddress:
                a2 = row
                index2 = index

        # If row at "second address row number" is empty, check the inverse index for same distance
        # Return distance value
        if a1[index2] == '':
            return a2[index1]
        else:
            return a1[index2]


# Truck 1 object
truck1 = Truck()
truck1.loadedPackages = []
truck1.hub = "4001 S 700 E"
truck1.location = truck1.hub
truck1.departureTime = timedelta(hours=8)
truck1.currentTime = truck1.departureTime
truck1.mileage = 0


# O(n^2) time and O(n) space
# Truck1 delivery using nearest-neighbor algorithm
def truck1_delivery():
    # While truck1 is not empty
    while len(truck1.loadedPackages) >= 1:
        tempDistance = 1000  # Reset shortest distance

        # Iterate through truck1 list
        for package in truck1.loadedPackages:

            # Grab package from Hash Table and store in p
            p = hashTablePackages.search(package)

            # Compare distance of current and next address
            distance = getDistance('CSV/addresses.csv', truck1.location, p.Address)

            # Deliver 9 AM package first
            if p.DeliveryTime == '9:00 AM':
                time = timedelta(hours=float(distance) / 18)
                tempDistance = newDistance = distance
                newAddress = p.Address
                closestPackage = package
                break

            # If current distance is shorter than previous distance
            # update distance and time details, then continue iteration
            if float(distance) < float(tempDistance):
                tempDistance = newDistance = distance
                newAddress = p.Address
                closestPackage = package
                time = timedelta(hours=float(distance) / 18)
                continue

        # Once shortest package is found then deliver package
        # Delivery and removal of package from truck1
        truck1.location = newAddress
        truck1.mileage += float(newDistance)
        truck1.currentTime += time
        p = hashTablePackages.search(closestPackage)  # Set hash table object to current package
        p.Status = 'Delivered'
        p.StatusDelTime = truck1.currentTime
        truck1.loadedPackages.remove(closestPackage)

    # Assign final distance and time details to truck1
    # Find distance between current location and Hub
    return_to_hub = getDistance('CSV/addresses.csv', truck1.location, '4001 S 700 E')
    truck1.mileage += float(return_to_hub)
    truck1.currentTime += timedelta(hours=float(return_to_hub) / 18)
    truck1.location = '4001 S 700 E'


# Truck 2 object
truck2 = Truck()
truck2.loadedPackages = []
truck2.hub = "4001 S 700 E"
truck2.location = truck2.hub
truck2.departureTime = timedelta(hours=9, minutes=5)
truck2.currentTime = truck2.departureTime
truck2.mileage = 0


# O(n^2) time and O(n) space
# Truck2 delivery using nearest-neighbor algorithm
def truck2_delivery():
    # While truck2 is not empty
    while len(truck2.loadedPackages) >= 1:
        tempDistance = 1000  # Reset shortest distance

        # Iterate through truck2 list
        for package in truck2.loadedPackages:

            # Grab package from Hash Table and store in p
            p = hashTablePackages.search(package)

            # Compare distance of current and next address
            distance = getDistance('CSV/addresses.csv', truck2.location, p.Address)

            # Deliver 10:30 AM package first
            if p.DeliveryTime == '10:30 AM':
                time = timedelta(hours=float(distance) / 18)
                tempDistance = newDistance = distance
                newAddress = p.Address
                closestPackage = package
                break

            # If current distance is shorter than previous distance
            # update distance and time details, then continue iteration
            if float(distance) < float(tempDistance):
                tempDistance = newDistance = distance
                newAddress = p.Address
                closestPackage = package
                time = timedelta(hours=float(distance) / 18)
                continue

        # Once shortest package is found then deliver package
        # Delivery and removal of package from truck2
        truck2.location = newAddress
        truck2.mileage += float(newDistance)
        truck2.currentTime += time
        p = hashTablePackages.search(closestPackage)  # Set hash tabel to current package
        p.Status = 'Delivered'
        p.StatusDelTime = truck2.currentTime
        truck2.loadedPackages.remove(closestPackage)

    # Assign final distance and time details to truck2
    # Find distance between current location and Hub
    return_to_hub = getDistance('CSV/addresses.csv', truck2.location, '4001 S 700 E')
    truck2.mileage += float(return_to_hub)
    truck2.currentTime += timedelta(hours=float(return_to_hub) / 18)
    truck2.location = '4001 S 700 E'


# Truck 3 object
truck3 = Truck()
truck3.loadedPackages = []
truck3.undelivered = []
truck3.hub = "4001 S 700 E"
truck3.location = truck3.hub
truck3.departureTime = timedelta(hours=10, minutes=20)
truck3.currentTime = truck3.departureTime
truck3.mileage = 0


# O(n^2) time and O(n) space
# Truck3 delivery using nearest-neighbor algorithm.
def truck3_delivery():
    # While truck3 is not empty
    while len(truck3.loadedPackages) >= 1:
        tempDistance = 1000  # Reset shortest distance

        # Iterate through truck3 list
        for package in truck3.loadedPackages:

            # Grab package from Hash Table and store in pAddress
            p = hashTablePackages.search(package)

            # Compare distance of current and next address
            distance = getDistance('CSV/addresses.csv', truck3.location, p.Address)

            # If current distance is shorter than previous distance
            # update distance and time details, then continue iteration
            if float(distance) < float(tempDistance):
                tempDistance = newDistance = distance
                newAddress = p.Address
                closestPackage = package
                time = timedelta(hours=float(distance) / 18)
                continue

        # Once shortest package is found then deliver package
        # Delivery and removal of package from truck3
        truck3.location = newAddress
        truck3.mileage += float(newDistance)
        truck3.currentTime += time
        p = hashTablePackages.search(closestPackage)  # Set hash tabel to current package
        p.Status = 'Delivered'
        p.StatusDelTime = truck3.currentTime
        truck3.loadedPackages.remove(closestPackage)

    # Assign final distance and time details to truck3
    # Find distance between current location and Hub
    return_to_hub = getDistance('CSV/addresses.csv', truck3.location, '4001 S 700 E')
    truck3.mileage += float(return_to_hub)
    truck3.currentTime += timedelta(hours=float(return_to_hub) / 18)
    truck3.location = '4001 S 700 E'


# Begin loading packages using packages.csv
loadPackageData('CSV/packages.csv', hashTablePackages)


# O(n) time and space
# Trucks are now loaded and can be simulated
class Main:
    # User Interface
    # Program Title
    print("Western Governors University Parcel Service (WGUPS)")
    print()

    # Run Truck 1 delivery and print details
    print("Truck 1 Details:")
    print("Delivered {} packages:".format(len(truck1.loadedPackages)), truck1.loadedPackages)
    truck1_delivery()
    print("Departed at: {},".format(truck1.departureTime), "Returned at: {}".format(truck1.currentTime))
    print("The mileage for the route is:", truck1.mileage)
    print()

    # Run Truck 2 delivery and print details
    print("Truck 2 Details:")
    print("Delivered {} packages:".format(len(truck2.loadedPackages)), truck2.loadedPackages)
    truck2_delivery()
    print("Departed at: {},".format(truck2.departureTime), "Returned at: {}".format(truck2.currentTime))
    print("The mileage for the route is:", truck2.mileage)
    print()

    # Run Truck 3 delivery and print details
    print("Truck 3 Details:")
    print("Delivered {} packages:".format(len(truck3.loadedPackages)), truck3.loadedPackages)
    truck3_delivery()
    print("Departed at: {},".format(truck3.departureTime), "Returned at: {}".format(truck3.currentTime))
    print("The mileage for the route is:", truck3.mileage)
    print()

    # Print total mileage for all trucks
    print("Total mileage is: {}".format(truck1.mileage + truck2.mileage + truck3.mileage))
    print()

    # The user will be asked to enter a specific time
    timeInput = input("Please enter a time for more details. (Use the following 24HR format, HH:MM:SS): ")
    try:
        # Assign time to timeInputConvert
        (h, m, s) = timeInput.split(":")
        timeInputConvert = timedelta(hours=int(h), minutes=int(m), seconds=int(s))

        # Update all packages for time entered
        # Iterate through all packages
        for p in range(1, 41):
            package = hashTablePackages.search(p)

            # If input time is earlier than delivery time, check for truck departure time
            if timeInputConvert < package.StatusDelTime:
                # Check truck1 departure time and update package status
                if package.TruckNumber == 1:
                    if truck1.departureTime < timeInputConvert:
                        package.Status = 'En Route'
                        package.StatusDelTime = ''
                    else:
                        package.Status = 'Hub'
                        package.StatusDelTime = ''
                # Check truck2 departure time and update package status
                if package.TruckNumber == 2:
                    if truck2.departureTime < timeInputConvert:
                        package.Status = 'En Route'
                        package.StatusDelTime = ''
                    else:
                        package.Status = 'Hub'
                        package.StatusDelTime = ''
                # Check truck3 departure time and update package status
                if package.TruckNumber == 3:
                    if truck3.departureTime < timeInputConvert:
                        package.Status = 'En Route'
                        package.StatusDelTime = ''
                    else:
                        package.Status = 'Hub'
                        package.StatusDelTime = ''

            # Reflect package 9 details before 10:20 AM
            if timeInputConvert < timedelta(hours=10, minutes=20):
                if package.ID == 9:
                    package.Address = '300 State St'
                    package.City = 'Salt Lake City'
                    package.State = 'UT'
                    package.Zip = '84103'
                    package.Notes = "Wrong address listed"

        # The user will be asked if they want to view packages
        # by truck number, package ID, or all
        viewModeInput = input("View by: Single, Truck, or All? ")
        # View all packages
        if viewModeInput == 'All' or viewModeInput == 'all':
            for p in range(1, 41):
                package = hashTablePackages.search(p)
                print(str(package))
        # View single package
        if viewModeInput == 'Single' or viewModeInput == 'single':
            try:
                # The user will be asked to input a package ID.
                input = input("Enter the package ID: ")
                package = hashTablePackages.search(int(input))
                print(package)

            except ValueError:
                print("Entry invalid. Closing program.")
                exit()
        # View packages by truck number
        if viewModeInput == 'Truck' or viewModeInput == 'truck':
            try:
                # The user will be asked to input a package ID.
                input = input("Enter the Truck ID: ")
                for p in range(1, 41):
                    package = hashTablePackages.search(p)
                    if package.TruckNumber == int(input):
                        print(str(package))

            except ValueError:
                print("Entry invalid. Closing program.")
                exit()
    except ValueError:
        print("Entry invalid. Closing program.")
        exit()

