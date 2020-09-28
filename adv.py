from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

rev_directions = {"n": "s", "s": "n", "e": "w", "w": "e"}

class Queue():
    def __init__(self):
        self.queue = []
    
    def enqueue(self, value):
        self.queue.append(value)

    def deque(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
        
    def size(self):
        return len(self.queue)

def bfs(starting_room, visited= set()):
    path = []
    for direction in player.current_room.get_exits():
        player.travel(direction)
        if player.current_room in visited:
            player.travel(rev_directions[direction])
        else:
            visited.add(player.current_room)
            path.append(direction)
            path = path + bfs(player.current_room, visited)
            player.travel(rev_directions[direction])
            path.append(rev_directions[direction])
    return path

traversal_path = bfs(player.current_room)

#TESTS PASSED: 1000 moves, 500 rooms visited

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
