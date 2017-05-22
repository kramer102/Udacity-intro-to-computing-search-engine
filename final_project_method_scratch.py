example_input = "John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

input_empty = ''


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


def get_connections(network, user):
    try:
        return network[user][0]
    except:
        return None


def get_games_liked(network, user):
    if user in network:
        return network[user][1]
    return None


def add_connection(network, user_A, user_B):
    if user_A not in network or user_B not in network:
        return False
    if user_B in network[user_A][0]:
        return network
    network[user_A][0].append(user_B)
    return network


def add_new_user(network, user, games):
    if user in network:
        return network
    network[user] = [[], games]
    return network


def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)


def get_secondary_connections(network, user):
    if user not in network:
        return None
    secondary_connections = []
    for connections in network[user][0]:
        a = get_connections(network, connections)
        union(secondary_connections, a)
    return secondary_connections


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


def build_test_network():
    network = {}
    add_new_user(network, 'A', [])
    add_new_user(network, 'B', [])
    add_new_user(network, 'C', [])
    add_new_user(network, 'D', [])
    add_new_user(network, 'E', [])
    add_new_user(network, 'F', [])
    network['A'][0] = ['B', 'C', 'D']
    network['B'][0] = ['C']
    network['C'][0] = ['B']
    network['D'][0] = ['E', 'A']
    network['E'][0] = ['B', 'F']
    network['F'][0] = []
    return network


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


def add_choices(network, user, choices):
    if user not in choices:
        choices[user] = list(range(0, len(network[user][0])))
        return choices
    

def find_path(network, target, path, choices):
    import random
    if path == []:
        return path
    if target in path:
        return path
    user = path[-1]
    # print(path)
    # print(choices)
    add_choices(network, user, choices)
    if choices[user] == []:
        path.pop()
        return find_path(network, target, path, choices)
    # next_path = network[user][0][choices[user].pop()]
    index = random.choice(choices[user])
    choices[user].remove(index)
    next_path = network[user][0][index]
    path.append(next_path)
    return find_path(network, target, path, choices)


def approx_shortest_path_to_friend(network, user_A, user_B, time_step):
    path_base = path_to_friend(network, user_A, user_B)
    for t in range(time_step):
        path = path_to_friend(network, user_A, user_B)
        if len(path) < len(path_base):
            path_base = path
    return path_base

# MYOP -- I'm interested in which members of the network have the
# most influence.  I think it would be related to how closely connected they
# are and how much they have in common with the people they are
# connected to.


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

# I'm going to think of the amount of influence one user has
# over another as the number of games they have in common divided
# by the length of the path from one to another as determined
# by the find path algorith (not perfect should be shortest) maybe I'll try
# and find something more elegant later.


# def individual_influence(network, user_A, user_B):
#     games = games_in_common(network, user_A, user_B) / \
#         len(get_games_liked(network, user_A))
#     time_step = 30
#     path = approx_shortest_path_to_friend(network, user_A, user_B, time_step)
#     # print(path)
#     if path is None:
#         return 0.0
#     length_of_path = len(path)
#     if length_of_path == 0:
#         return 0.0
#     # the score is computer by adding a connecting factor and games factor
#     return (0.0 + games) / length_of_path + 1.0 / length_of_path

# new individual influence try.  I'm going to say that the influence
# of one person over another is proportional to their rank and the
# number of games they have in common and inversely proportional
# to the square of the distance of the shortest path from one to
# the other

def individual_influence(network, user_A, user_B):
    ranks = user_ranks(network)
    rank = ranks[user_A]
    loops = 10
    common_ground = 0.0 # forcing double
    path = (approx_shortest_path_to_friend(network,
                                           user_A, user_B, loops))
    if path is None:
        path_length = 1000      # effectively making the influence 0
    else:
        path_length = len(path)
    games_user_A = get_games_liked(network, user_A)
    games_user_B = get_games_liked(network, user_B)
    for game in games_user_A:
        if game not in games_user_B:
            games_user_B.append(game)
    total_games = games_user_B
    if total_games is None:
        total_games = list(range(1000))
    com_imp_f = 2               # common ground importance fudge factor
    common_ground = com_imp_f * (games_in_common(network, user_A,
                                                 user_B)) / len(total_games)
    influence = (rank * common_ground) / path_length ** 2
    return influence


def overall_influence(network, user):
    score = 0.0
    for people in network:
        score = score + individual_influence(network, user, people)
    return score


def influence_rankings(network):
    rankings = []
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


def user_ranks_rankings(network):
    ranks = user_ranks(network)
    rankings = []
    for users in ranks:
        rankings.append([ranks[users], users])
    rankings.sort()
    rankings.reverse()
    return rankings
