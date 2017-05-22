# playing with recursion


def factorial(integer):
    # base case
    if integer == 1:
        return 1
    if integer == 0:
        return 1
    # recursive case
    # print(integer)
    return integer * factorial(integer - 1)


def fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib(n - 1) + fib(n - 2)


# making a dictionary to try to make sense of path in final project

# def path_to_friend(network, user_A, user_B):
#     path = []
#     path_taken = []
#     if user_A not in network:
#         return None
#     find_path(network, user_A, user_B, path, path_taken)
#     if user_B not in path:
        
#     return path


# def find_path(network, origin, target, path, path_taken):
#     import random
#     path.append(origin)
#     if target in network[origin][0]:
#         path.append(target)
#         return path
#     if network[origin][0] == []:
#         path.pop()
#         return None
#     origin = network[origin][0][random.randrange(len(network[origin][0])) - 1]
#     if origin in path_taken:
#         return None
#     path_taken.append(origin)
#     return find_path(network, origin, target, path, path_taken)

# First attempt at path_to_friend
# def path_to_friend(network, user_A, user_B):
#     path = []
#     if user_A not in network:
#         return None
#     find_path(network, user_A, user_B, path)
#     return path


# def find_path(network, origin, target, path):
#     import random
#     path.append(origin)
#     if target in network[origin][0]:
#         path.append(target)
#         return path
#     if network[origin][0] == []:
#         path.pop()
#         return None
#     origin = network[origin][0][random.randrange(len(network[origin][0])) - 1]
#     return find_path(network, origin, target, path)


# testing out to see if I can apply the Urank to my graph of people

def user_rank(network):
    # set everyones rank to one
    ranks = {}
    d = .8
    nfriends = len(network)
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
                                                           
        


    
