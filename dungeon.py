# give players the choice to set the size of the maze
# give players the choice to set the  number of monsters
# option to have moving or static monsters

import random
import os
import sys


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def retry():
    retry_inp = input("Want to play again? Y/n ")
    if retry_inp.lower() != "n":
        game()
    else:
        print("Goodbye")
        sys.exit()


def generate_maze(width, height, monsters):
    # generate maze
    maze = []
    floor = 0
    while floor < height:
        room = 0
        while room < width:
            maze.append([floor, room])
            room += 1
        floor += 1

    # Put player, monsters and door in maze and check they are not in the same position
    while True:
        player_pos = random.choice(maze)
        door_pos = random.choice(maze)

        if monsters > 1:
            m_count = 0
            monster_pos = []
            while m_count < monsters:
                monster_pos.append(random.choice(maze))
                m_count += 1
            if player_pos != door_pos and player_pos not in monster_pos and door_pos not in monster_pos:
                break
        else:
            monster_pos = random.choice(maze)
            if player_pos != monster_pos and player_pos != door_pos and monster_pos != door_pos:
                break
    return maze, player_pos, monster_pos, door_pos


def draw_dungeon(dungeon, player, monster, door, history, width):
    # Draw a visual map of the maze
    clear()
    for floor, room in dungeon:
        if [floor, room] == player:
            print('[ P ]', end=' ')
        elif [floor, room] in monster:
            print('[ M ]', end=' ')
        #elif [floor, room] == door:
        #    print('[ D ]', end=' ')
        elif [floor, room] in history:
            print('[ . ]', end=' ')
        else:
            print('[   ]', end=' ')
        if room == (width-1):
            print('\n')

    # print('You are in {}\n'
    #      'The monster are/is in: {}\n'
    #      'The door is in {}\n'
    #      .format(player, monster, door))


def encounter(player, door, monster, history):
    # when player encounter door he wins
    if player == door:
        print('Congratulations! It took you {} turns to escape the dungeon'.format(len(history)))
        retry()
    # when monster catches player he loses
    elif player in monster:
        print('The monster swallows you whole... You survived {} turns in the dungeon'.format(len(history)))
        retry()


def player_move(current, width, height):
    # player can move within the dungeon
    # player cannot fall off the grid
    while True:
        direction = input(
            "You currently are in room {}, in which direction would you like to move? U/D/R/L ".format(current))
        floor = current[0]
        room = current[1]
        if direction.upper() == 'D':
            floor += 1
        elif direction.upper() == 'U':
            floor -= 1
        elif direction.upper() == 'R':
            room += 1
        elif direction.upper() == 'L':
            room -= 1
        else:
            print('{} is not a valid command'.format(current))

        if room < 0 or room > width - 1 or floor < 0 or floor > height - 1:
            continue
        else:
            return [floor, room]


def monster_move(current, height, width):
    # monster moves randomly in the dungeon
    # monster cannot fall off the grid
    for idx, monsters in enumerate(current):
        while True:
            direction = random.randint(1, 4)
            floor = monsters[0]
            room = monsters[1]

            if direction == 1:
                floor += 1
            elif direction == 2:
                floor -=  1
            elif direction == 3:
                room += 1
            elif direction == 2:
                room -= 1

            if room < 0 or room > width -1 or floor < 0 or floor > height - 1:
                continue
            else:
                current[idx] = [floor, room]
                break
    return current


def settings ():
    height = 8
    width = 8
    monsters = 5
    return height, width, monsters


def game():

    maze_height, maze_width, num_monsters = settings()

    # Generate maze with grid
    our_maze, player_pos, monster_pos, door_pos = generate_maze(maze_height, maze_width, num_monsters)

    player_history = []

    while True:
        # player breadcrumbs
        player_history.append(player_pos)
        draw_dungeon(our_maze, player_pos, monster_pos, door_pos, player_history, maze_width)

        # player movement
        player_pos = player_move(player_pos, maze_width, maze_height)
        encounter(player_pos, door_pos, monster_pos, player_history)
        draw_dungeon(our_maze, player_pos, monster_pos, door_pos, player_history, maze_width)

        # monster movement
        monster_pos = monster_move(monster_pos, maze_height, maze_width)
        encounter(player_pos, door_pos, monster_pos, player_history)
        draw_dungeon(our_maze, player_pos, monster_pos, door_pos, player_history, maze_width)


game()
