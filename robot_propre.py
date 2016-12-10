import random

WALL = 'X'
ROBOT_START = 'S'
ENEMY_START = 'E'
PLAYER = 'R'
ENEMY = 'M'
EXIT = 'O'

TRACKED = (WALL, ROBOT_START, ENEMY_START, EXIT)
ERASED = (ROBOT_START, ENEMY_START, )

class Robot(object):
    deltas = {
        'Z': (0, -1),
        'S': (0, 1),
        'Q': (-1, 0),
        'D': (1, 0)
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def pos(self):
        return self.x, self.y

    def lecteur(self, direction):
        direction = direction.upper()
        numbers = "123456789"
        rapide = []
        multiple = ""
        nouvelle_direction = ""
        for element in direction:
            rapide.append(element)
            for item in rapide:
                if item in numbers:
                    multiple = item
                else:
                    nouvelle_direction = item
        return nouvelle_direction, multiple


    def next(self, direction, multiple):
        if multiple == "":
            dx, dy = self.deltas.get(direction, (0, 0))
            return self.x + dx, self.y + dy
        else:
            if direction == "Z" or direction == "S":
                dx, dy = self.deltas.get(direction, (0, 0))
                dy *= int(multiple)
            elif direction == "Q" or direction == "D":
                dx, dy = self.deltas.get(direction, (0, 0))
                dx *= int(multiple)
        return self.x + dx, self.y + dy

    def move(self, x, y):
        self.x = x
        self.y = y

class Enemy(Robot):

    def suivant(self, direction):
        dx, dy = direction
        return self.x + dx, self.y + dy

    def inverse(self, direction):
        dx, dy = direction
        return self.x - dx, self.y - dy

    def intelligence(self, player, enemy, obstacle):
        goal = player.pos
        position = enemy.pos
        choix = []
        if goal != position:
            if goal[0] != position[0]:
                choix = []
                if goal[0] <= position[0]:
                    choix.append((-1, 0))
                elif goal[0] >= position[0]:
                    choix.append((1, 0))

            elif goal[1] != position[1]:
                choix = []
                if goal[1] <= position[1]:
                    choix.append((0, -1))
                elif goal[1] >= position[1]:
                    choix.append((0, 1))
        if choix == []:
            return self.x, self.y
        else:
            direction = random.choice(choix)
            if enemy.suivant(direction) in obstacle:
                return enemy.inverse(direction)
            else:
                return enemy.suivant(direction)

class GameMap(object):

    def __init__(self):
        self.grid = []
        self.coordinates = {}
        self.objects = {}
        self.obstacles = []
        self.sorties = []

    def load(self, path):
        with open(path, 'r') as f:
            for y, line in enumerate(f):
                line = line.strip()
                temp_line = []
                for x, symbol in enumerate(line):
                    # load background
                    if symbol in TRACKED:
                        self.coordinates[(x, y)] = symbol
                    if symbol in ERASED:
                        temp_line.append(' ')
                    else:
                        temp_line.append(symbol)

                self.grid.append(temp_line)

        self.init()

    @property
    def player(self):
        return self.objects['robot']

    @property
    def enemy(self):
        return self.objects['enemy']

    def show(self):
        for y, line in enumerate(self.grid):
            temp_line = []
            for x, symbol in enumerate(line):
                if (x, y) == self.player.pos:
                    temp_line.append(PLAYER)
                elif (x, y) == self.enemy.pos:
                    temp_line.append(ENEMY)
                else:
                    temp_line.append(symbol)
            print(''.join(temp_line))

    def init(self):
        for (x, y), symbol in self.coordinates.items():
            if symbol == ROBOT_START:
                self.objects['robot'] = Robot(x, y)
            elif symbol == ENEMY_START:
                self.objects['enemy'] = Enemy(x, y)
            elif symbol == WALL:
                self.obstacles.append((x, y))
            elif symbol == EXIT:
                self.sorties.append((x, y))

    def is_obstacle(self, x, y):
        return (x, y) in self.obstacles

    def is_sortie(self, x, y):
        return (x, y) in self.sorties

    def logic(self):
        dest = input("Destination ? ({})".format('/'.join(Robot.deltas)))
        robot = self.player
        enemy = self.enemy
        reader = robot.lecteur(dest)
        next_position = robot.next(*reader)
        if self.is_obstacle(*next_position):
            print("Pas par la !")
            enemy.move(*enemy.intelligence(robot, enemy, self.obstacles))
        elif self.is_sortie(*next_position):
            print('Bravo !')
            robot.move(*next_position)
            return True
        elif self.player.pos == self.enemy.pos:
            print("-----------------------------------")
            print("Vous venez de vous faire attraper !")
            print("-----------------------------------")
            return True
        else:
            enemy.move(*enemy.intelligence(robot, enemy, self.obstacles))
            robot.move(*next_position)
        return False

m = GameMap()
m.load("cartes.txt")
m.show()

while True:
    stop = m.logic()
    m.show()
    if stop:
        break
