# Robert Kramer
# kramer102@gmail.com
# gamer social network final project
# Sorces used: Udacity Course, google-stack overflow, python documentation


# Helper functions for create_data_structure
def get_next_sentence(remaining_string):
    endpos = remaining_string.find('.') + 1
    next_sentence = remaining_string[0:endpos]
    return next_sentence, endpos


def parse_user(next_sentence):
    user = next_sentence[0:next_sentence.find(' ')]
    return user


def parse_attribute(next_sentence):
    attribute = []
    if "is connected to " in next_sentence:
        con_start = next_sentence.find("is connected to ") + 15
        next_sentence = next_sentence[con_start:]
    else:
        con_start = next_sentence.find("likes to play ") + 13
        next_sentence = next_sentence[con_start:]
    while next_sentence.find(',') != -1:
        con = next_sentence[1:next_sentence.find(',')]
        attribute.append(con)
        next_sentence = next_sentence[next_sentence.find(',') + 1:]
    attribute.append(next_sentence[1:-1])
    return attribute


# My version of create_data_structure.  Will return an empty dictionary if
# input is "".  Data structure in the form {<key>:[[<user>],[<games>]]}
def create_data_structure(string_input):
    network = {}
    while string_input.find('.') != -1:
        next_sentence, endpos = get_next_sentence(string_input)
        string_input = string_input[endpos:]
        user = parse_user(next_sentence)
        connections = parse_attribute(next_sentence)
        next_sentence, endpos = get_next_sentence(string_input)
        games_liked = parse_attribute(next_sentence)
        network[user] = [connections, games_liked]
        string_input = string_input[endpos:]
    return network


# get_connections takes in a formatted network and the user.  It returns
# None if the user is not in network.  If the user has no connections it will
# return []
def get_connections(network, user):
    if user in network:
        return network[user][0]
    return None


# get_games_liked takes in a formatted network.  Same as above except games
def get_games_liked(network, user):
    if user in network:
        return network[user][1]
    return None


# add_connection takes in a network and two users.  It adds user_B to
# the connections of user_A.  If either is not in the network it returns
# False.  If user_B is already connected to user_A the network is returned
# unchanged
def add_connection(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    if user_B in network[user_A][0]:
        return network
    network[user_A][0].append(user_B)
    return network


# add_new_user takes in a network, user, and the games the user likes in the
# form of a list of strings.  Games MUST be passed as a list for the network
# to maintain proper structure and the other functions to perform correctly.
# If there are no games, the empty list [] must be passed.
def add_new_user(network, user, games):
    if user in network:
        return network
    network[user] = [[], games]
    return network


# union is a helper function that mutates the first list into the union
# of both list
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


# get_secondary_connections takes in the network and a user.  It returns the
# connections of connections of the user.  Will return [] if there are none.
def get_secondary_connections(network, user):
    if user not in network:
        return None
    secondary_connections = []
    for connections in network[user][0]:
        a = get_connections(network, connections)
        union(secondary_connections, a)
    return secondary_connections


# connections_in_common return an integer count of the number
# of connections two users have in common
def connections_in_common(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    connect_A = get_connections(network, user_A)
    connect_B = get_connections(network, user_B)
    count = 0
    for con in connect_A:
        if con in connect_B:
            count = count + 1
    return count


# path_to_friend takes in the network and two users.  It returns a path
# as a list of the users it's crawled through.  If it returns
# to the start, the method will trim the beginning of the list.
# The possible paths are stored in the dictionary choices.  As
# find_path crawls through it eliminates choices so that it doesn't
# take the same path twice.
def path_to_friend(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return None
    path = [user_A]
    choices = {}
    add_choices(network, user_A, choices)
    find_path(network, user_B, path, choices)
    if path == []:
        return None
    short_path = []
    while path[-1] != user_A:
        short_path.insert(0, path.pop())
    short_path.insert(0, user_A)
    return short_path


# Helper methods for path_to_friend.
def add_choices(network, user, choices):
    if user not in choices:
        choices[user] = list(range(0, len(network[user][0])))
        return choices


# Takes in a network, a target user, a path list, and dictionary choices
# returns a path as a list to the target.  Uses random to pick from choices
# for the direction so it can find different paths.  If it reaches an empty
# list it backs up.  If it runs out of choices, it backs up.  May return
# redundant paths if it returns to the start after going down a
# fruitless branch
def find_path(network, target, path, choices):
    import random
    if path == []:
        return path
    if target in path:
        return path
    user = path[-1]
    add_choices(network, user, choices)
    if choices[user] == []:
        path.pop()
        return find_path(network, target, path, choices)
    index = random.choice(choices[user])
    choices[user].remove(index)
    next_path = network[user][0][index]
    path.append(next_path)
    return find_path(network, target, path, choices)


# Need for later methods.  Takes in a network, two users, and the number
# of loops you would like it to run for.  Uses the randomness of the find
# path method to attempt to find the shortest path.
def approx_shortest_path_to_friend(network, user_A, user_B, loops):
    path_base = path_to_friend(network, user_A, user_B)
    for t in range(loops):
        path = path_to_friend(network, user_A, user_B)
        if len(path) < len(path_base):
            path_base = path
    return path_base


# MYOP -- I'm going to say that the influence
# of one person over another is proportional to their rank and the
# number of games they have in common and inversely proportional
# to the square of the distance of the shortest path from one to
# the other.  Other methods in the procedure use this information
# to attempt to indicate which users have the greatest influence.
# A method for a list of Rankings based on rank and influence are provided.
# In the example set the two Rankings give similar, but not identical results.
# There are damping factors included which may allow the model to be adjusted.


# games_in_common is a helper method
def games_in_common(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    games_A = get_games_liked(network, user_A)
    games_B = get_games_liked(network, user_B)
    count = 0
    for e in games_A:
        if e in games_B:
            count = count + 1
    return count


# individual_influence takes in a network and two users.  It attempts
# to output a numerical influence measure.  If loops for shortest path
# are large the method can take a while.  The model is a guess.  Use
# com_imp_f to vary the importance of games in common to the model
def individual_influence(network, user_A, user_B):
    ranks = user_ranks(network)
    rank = ranks[user_A]
    loops = 10
    common_ground = 0.0  # forcing double
    path = (approx_shortest_path_to_friend(network,
                                           user_A, user_B, loops))
    if path is None:
        path_length = 1000      # effectively making the influence 0
    else:
        path_length = len(path)
    games_user_A = list(get_games_liked(network, user_A)) # copies
    games_user_B = list(get_games_liked(network, user_B))
    union(games_user_A, games_user_B)
    total_games = games_user_A
    if total_games is None:
        total_games = list(range(1000))
    com_imp_f = 2               # common ground importance fudge factor
    common_ground = com_imp_f * (games_in_common(network, user_A,
                                                 user_B)) / len(total_games)
    influence = (rank * common_ground) / path_length ** 2
    return influence


# This method takes in a network and user.  It returns a score of the
# sum of the influence of that members to each member in the network
def overall_influence(network, user):
    score = 0.0
    for people in network:
        score = score + individual_influence(network, user, people)
    return score


# Takes in a network and returns a list of rankings from most influential
# to least.
def influence_rankings(network):
    rankings = []            # used a list because I wanted to sort the result
    for users in network:
        score = overall_influence(network, users)
        rankings.append([score, users])
    rankings.sort()
    rankings.reverse()
    # normalizing the results
    sumof = 0
    for elements in rankings:
        sumof = elements[0] + sumof
    for e in rankings:
        e[0] = e[0] / sumof
    return rankings


# Essentially the U_rank method from the course.  Takes in a network and
# returns a dictionary mapping each user to their rank associated with how
# many incoming connections they have.  First included to check if measuring
# influence by distance from one user to another gave meaningful results.
# later integrated into the influence model.
def user_ranks(network):
    # set everyones rank to one
    ranks = {}
    d = .8
    if network:
        nfriends = len(network) # trying to handle empty network
    times_to_run = 10
    for people in network:
        ranks[people] = 1.0 / nfriends
    for t in range(times_to_run):
        newranks = {}
        for people in network:
            newrank = (1.0 - d) / nfriends
            for node in network:
                if people in network[node][0]:
                    newrank = newrank + ranks[node] * d / len(network[node][0])
            newranks[people] = newrank
        ranks = newranks
    return ranks


# Takes in a network and returns and ordered list of their rankings.
# Interesting to use to compare with influence
def user_ranks_rankings(network):
    ranks = user_ranks(network)
    rankings = []
    for users in ranks:
        rankings.append([ranks[users], users])
    rankings.sort()
    rankings.reverse()
    return rankings
