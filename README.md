# Delivery-Route-Optimization
 
This program was made to determine an optimized delivery route for packages while being limited to 3 available trucks and 2 available drivers. 
Within the code includes time and space complexity details for each function.

To load each truck, a greedy algorithm approach was used. The packages first were loaded by the earliest delivery time and special notes. Then by matching zip codes to the already loaded packages.
The delivery of the packages was handled by a Nearest-Neighbor algorithm. This takes the distance between the current address and every potential destination address, then chooses the destination with the closest distance. 
