# Map Coloring using Backtracking and Consistency Checking

print("===================================")
print("      MAP COLORING - CSP")
print("  Backtracking + Consistency Check")
print("===================================")

# Map of regions and their neighboring regions
map_regions = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}

# Available colors
colors = ["Red", "Green", "Blue"]

# Stores the color assigned to each region
assignment = {}


# Check whether assigning a color is consistent
def is_consistent(region, color):

    for neighbor in map_regions[region]:

        if neighbor in assignment:
            if assignment[neighbor] == color:
                return False

    return True


# Backtracking algorithm
def backtracking():

    # If all regions are colored, solution is found
    if len(assignment) == len(map_regions):
        return True

    # Select an uncolored region
    for region in map_regions:
        if region not in assignment:
            break

    # Try each available color
    for color in colors:

        print("Trying", color, "for region", region)

        # Check consistency before assigning
        if is_consistent(region, color):

            assignment[region] = color

            # Recursively color the remaining regions
            if backtracking():
                return True

            # Backtrack if the assignment leads to failure
            print("Backtracking from", region)
            del assignment[region]

    return False


# Start the algorithm
if backtracking():

    print("\n===================================")
    print("Map Coloring Solution")
    print("===================================")

    for region in assignment:
        print(region, "->", assignment[region])

else:
    print("No solution exists.")