# Faster sin/cos function by using a lookup table
# Example code for Daniel Shiffman made by Ewoud Dronkert
# https://twitter.com/ednl
# https://github.com/ednl

# Only needed for lookup table generation and validation
from math import sin, cos, radians

quad1  =  90    # first quadrant 90 degrees [integer]
quad2  = 180    # second quadrant 180 degrees [integer]
quad3  = 270    # third quadrant 270 degrees [integer]
circle = 360    # full circle 360 degrees [integer]

# Generate the lookup table with index 0..quad1 inclusive (= 0..90 degrees inclusive)
# In real code, this should probably be a list of literal values
# Use the minimum amount of decimals necessary (arbitrary choice here: 5),
# especially if your language has both float and double types
sintable = [round(sin(radians(a)), 5) for a in range(quad1 + 1)]

# Give sine of angle in whole degrees by using lookup table
# Argument can be any integer but needs to be normalised, so this is slow for very
# big (positive or negative) values. It depends on the CPU and language implementation
# whether "mod" is faster than repeated adding/subtracting. On modern architectures,
# mod is definitely faster, but on the Apple II+? I have no idea :)
def sinlookup(a):
    # Normalise to the range 0..circle inclusive
    # If angle is often very large and mod operator is hardware accelerated, then use that
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    # Value is now in the range 0..360 degrees inclusive
    # Map each quadrant onto the first quadrant which is in the lookup table
    # Each time, "greater than" is good because the lookup table includes 90 degrees
    if a > quad3:
        return -sintable[circle - a]    # x-y-mirror
    if a > quad2:
        return -sintable[a - quad2]     # x-shift and y-mirror
    if a > quad1:
        return sintable[quad2 - a]      # x-mirror
    return sintable[a]                  # direct value

# Same for cosine
def coslookup(a):
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    if a > quad3:
        return sintable[a - quad3]     # x-shift
    if a > quad2:
        return -sintable[quad3 - a]    # x-y-mirror
    if a > quad1:
        return -sintable[a - quad1]    # x-shift and y-mirror
    return sintable[quad1 - a]         # x-mirror

# Test for a wide range of "index units"
# and display difference between lookup value and calculation
for a in range(-quad1, circle + quad1 + 1, 30):
    s1 = sinlookup(a)
    s2 = round(sin(radians(a)), 5)
    c1 = coslookup(a)
    c2 = round(cos(radians(a)), 5)
    print("degrees", a, "sin-err", s1 - s2, "cos-err", c1 - c2)
