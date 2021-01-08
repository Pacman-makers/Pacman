from App import App


def main():
    game = App((475, 650), "Pacman")

    game.prerun()
    game.run()


if __name__ == '__main__':
    main()
