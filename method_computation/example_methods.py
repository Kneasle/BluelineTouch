from .method import *
from .constants import *
from .call import *


# DOUBLES
bob_doubles = Method (5, "Plain", "Bob", "5.1.5.1.5,125",
							 calling_positions = "IOMH",
							 calling_position_type = POSITIONS_BY_PLACE_AFTER_CALL)

grandsire_doubles = Method (5, "Grandsire", "Bob", "3,1.5.1.5.1", [
	Call ("B", "3.1", _from = -1), Call ("S", "3.123", _from = -1)
])

grandsire_triples = Method (7, "Grandsire", "Bob", "3,1.7.1.7.1.7.1", [
	Call ("B", "3.1", _from = -1), Call ("S", "3.123", _from = -1)
])

kneasle_doubles = Method (5, "Saturn", "Principle", "3.5.3.1", {"B": "125", "S": "123"})

# MINOR
bob_minor = Method (6, "Plain", "Bob", "X16X16X16,12",
						   calling_positions = "IOMWH",
						   calling_position_type = POSITIONS_BY_PLACE_AFTER_CALL)

cambridge_minor = Method (6, "Cambridge", "Surprise", "x36x14x12x36x14x56,12",
								 {"B": "14", "S": "1234"}, calling_positions = "IBMWH",
								 calling_position_type = POSITIONS_BY_PLACE_AFTER_CALL)

original_minor = Method (6, "Original", "Principle", "X16", {"B": "14", "S": "1234"})

# TRIPLES
bob_triples = Method (7, "Plain", "Bob", "7.1.7.1.7.1.7,127",
							 calling_positions = "IBFWMH",
							 calling_position_type = POSITIONS_BY_PLACE_AFTER_CALL)

stedman_triples = Method (7, "Stedman", "Principle", "3.1.7.3.1.3.1.3.7.1.3.1",
								 [Call ("B", "5", every = 6, _from = -3),
								  Call ("S", "567", every = 6, _from = -3)])

# MAJOR
bob_major = Method (8, "Plain", "Bob", "x18x18x18x18,12",
						   calling_positions = "WVFBIMH")

double_coslany_major = Method (8, "Double Coslany Court", "Bob", "x14.58.36.14.58x18,18",
									  calling_positions = "HMIBFVW")

bristol_maj = Method (8, "Bristol", "Surprise", "x58x14.58x58.36.14x14.58x14x18,18",
							 calling_positions = "HMIBFVW")

# CATERS
stedman_caters = Method (9, "Stedman", "Principle", "3.1.9.3.1.3.1.3.9.1.3.1",
								[Call ("B", "7", every = 6, _from = -3),
								 Call ("S", "789", every = 6, _from = -3)])

# MAX and ABOVE
bristol_max = Method (12, "Bristol", "Surprise",
							 "x5Tx14.5Tx5T.36.14x7T.58.16x9T.70.18x18.9Tx18x1T,1T")

little_bob_twenty_two = Method (22, "Little", "Bob", "x1Lx14,12")
