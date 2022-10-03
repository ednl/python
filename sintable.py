# Faster sin/cos function by lookup table
# Example code for Daniel Shiffman made by Ewoud Dronkert
# https://twitter.com/ednl
# https://github.com/ednl

from math import sin, cos, tau

# Quadrants and circle below are not in degrees but in "index units" defined by the step
step = 3                # steps taken in degrees, must divide 90
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

# Make the lookup table indexed 0..quad1 inclusive (0..90 degrees inclusive)
# In real code, this should be a list of literal values
# Use the minimum amount of decimals necessary, here: 5
sintable = [round(sin(index2rad(i)), 5) for i in range(quad1 + 1)]

# Give sine of argument in "index units" from lookup table
# Argument 'a' is in stepped degrees where in this example the step is 3, so:
#   a = -1 => -3 degrees
#   a =  0 =>  0 degrees
#   a =  1 =>  3 degrees
#   a = 30 => 90 degrees
#   a = 31 => 93 degrees
def sinlookup(a):
    # Normalise a to the range 0..circle inclusive
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    # Value of a is now in the range 0..360 degrees inclusive
    # Map each quadrant onto the first quadrant which is in the lookup table
    # Each time, "greater than" is good because the lookup table includes 90 degrees
    if a > quad3:
        return -sintable[circle - a]
    if a > quad2:
        return -sintable[a - quad2]
    if a > quad1:
        return sintable[quad2 - a]
    return sintable[a]

# Same but for cosine
def coslookup(a):
    while a < 0:
        a += circle
    while a > circle:
        a -= circle
    if a > quad3:
        return sintable[a - quad3]
    if a > quad2:
        return -sintable[quad3 - a]
    if a > quad1:
        return -sintable[a - quad1]
    return sintable[quad1 - a]

# Test for a wide range of "index units"
# Display difference between lookup value and calculation
for i in range(-quad1, circle + quad1 + 1, 10):
    s1 = sinlookup(i)
    s2 = round(sin(index2rad(i)), 5)
    c1 = coslookup(i)
    c2 = round(cos(index2rad(i)), 5)
    print("index", i, "degrees", index2deg(i), "sin-err", s1 - s2, "cos-err", c1 - c2)