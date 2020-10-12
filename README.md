# Estimating-uplink-and-downlink

Contains script to cluster users in vicinity of cell towers. Only those user locations are contained 
in the cluster centering a cell tower which are at a distance less than 2 mi.

Also, the script also contains snippet to create clusters centering a user to find out which cell towers
are in the range of 2 mi from this user.

This program uses Haversine distance as a metric to compute distances between GPS locations
