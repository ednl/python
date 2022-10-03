# Faster sin/cos function by using a lookup table
# Example code for Daniel Shiffman made by Ewoud Dronkert
# https://twitter.com/ednl
# https://github.com/ednl

# Only needed for lookup table generation and validation
from math import sin, cos, tau

# Quadrants and circle below are not in degrees but in "index units" as defined by the step
# If every integer degree is needed, then step = 1 and most of the code can be simplified
# If fractional degrees are also needed, then this code needs to be modified!
step = 3                # step in degrees, must divide 90
quad1 = 90 // step      # first quadrant 90 degrees [integer]
quad2 = 180 // step     # second quadrant 180 degrees [integer]
quad3 = 270 // step     # third quadrant 270 degrees [integer]
circle = 360 // step    # a full circle 360 degrees [integer]

d2r = tau / 360         # degrees to radians factor [float]
i2r = step * d2r        # index to radians factor [float]

# From index to degrees
def index2deg(a):
    return a * step

# From index to radians
def index2rad(a):
    return a * i2r

# Generate the lookup table with index 0..quad1 inclusive (= 0..90 degrees inclusive)
# In real code, this could (should) be a list of literal values
# Use the minimum amount of decimals necessary, choice here: 5
sintable = [round(sin(index2rad(i)), 5) for i in range(quad1 + 1)]
# Another possibility would be to make these values integers by multiplying them
# by the number of decimals needed, while making sure that the maximum value (1 * 10^dec)
# stays within the standard integer range of your platform (e.g. 32767). But then the
# code using these values would have to be modified to take this scaling into account.

# Give sine of argument 'a' given in "index units" by using lookup table
# Argument 'a' is in stepped degrees where in this example the step is 3, so:
#   a = -1 => -3 degrees
#   a =  0 =>  0 degrees
#   a =  1 =>  3 degrees
#   a = 30 => 90 degrees
#   a = 31 => 93 degrees
# Argument 'a' can be any integer but needs to be normalised, so this is slow for very
# big (positive or negative) values. It depends on the CPU and language implementation
# whether "mod" is faster than repeated adding/subtracting. On modern architectures,
# mod is definitely faster, but on the Apple IIe? I have no idea :)
def sinlookup(a):
    # Normalise 'a' to the range 0..circle inclusive
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    # Value of 'a' is now in the range 0..360 degrees inclusive
    # Map each quadrant onto the first quadrant which is in the lookup table
    # Each time, "greater than" is good because the lookup table includes 90 degrees
    if a > quad3:
        return -sintable[circle - a]   # double mirror
    if a > quad2:
        return -sintable[a - quad2]    # shift and mirror
    if a > quad1:
        return sintable[quad2 - a]     # mirror
    return sintable[a]                 # direct value

# Same for cosine
def coslookup(a):
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    if a > quad3:
        return sintable[a - quad3]     # shift
    if a > quad2:
        return -sintable[quad3 - a]    # double mirror
    if a > quad1:
        return -sintable[a - quad1]    # shift and mirror
    return sintable[quad1 - a]         # mirror

# Test for a wide range of "index units"
# and display difference between lookup value and calculation
for i in range(-quad1, circle + quad1 + 1, 10):
    s1 = sinlookup(i)
    s2 = round(sin(index2rad(i)), 5)
    c1 = coslookup(i)
    c2 = round(cos(index2rad(i)), 5)
    print("index", i, "degrees", index2deg(i), "sin-err", s1 - s2, "cos-err", c1 - c2)
