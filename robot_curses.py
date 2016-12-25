import curses
from robot_propre import GameMap, Robot, ENEMY, PLAYER

class CurseGameMap(GameMap):

    def __init__(self, *args, **kwargs):
        self.screen = kwargs.pop('screen')
        super(CurseGameMap, self).__init__(*args, **kwargs)

    @property
    def last_line(self):
        return len(self.grid) + 1

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
            self.screen.addstr(y, 0, ''.join(temp_line))


    def status(self, text):
        s = self.screen
        line = self.last_line + 1
        if not text:
            y, x = s.getyx()
            s.move(line, 0)
            s.clrtoeol()
            s.move(y, x)
        else:
            self.screen.addstr(line, 0, '> {}'.format(text))

    def instruction(self, text):
        self.screen.addstr(self.last_line + 2, 0, text)

    def logic(self):
        self.instruction("Destination ? ({})".format('/'.join(Robot.deltas)))
        dest = self.screen.getkey()
        robot = self.player
        enemy = self.enemy
        reader = robot.lecteur(dest)
        next_position = robot.next(*reader)
        next_enemy = enemy.intelligence(robot, self.obstacles)
        if self.is_obstacle(*next_position):
            self.status("Pas par la !")
            enemy.move(*next_enemy)
        elif self.is_sortie(*next_position):
            self.status('Bravo !')
            robot.move(*next_position)
            return True
        elif self.player.pos == next_enemy or next_position == next_enemy:
            enemy.move(*next_enemy)
            robot.move(*next_position)
            self.status("Vous venez de vous faire attraper !")
            return True
        else:
            self.status('')
            enemy.move(*next_enemy)
            robot.move(*next_position)
        return False

def main(screen):
    m = CurseGameMap(screen=screen)
    m.load("cartes.txt")
    screen.clear()
    m.show()
    while True:
        stop = m.logic()
        m.show()
        if stop:
            screen.getch()
            break

if __name__ == '__main__':
    curses.wrapper(main)
