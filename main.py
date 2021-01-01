from App import App


def main():
    game = App((800, 600), "Pacman")

    game.prerun()
    game.run()


if __name__ == '__main__':
    main()
