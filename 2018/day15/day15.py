from sys import argv

from battle import Battle

if __name__ == '__main__':
    data_file = argv[1]
    with open(data_file, 'r') as f_in:
        battle = Battle(f_in)
    battle.run()
    # battle.print_metrics()
    print("WINNERS:", battle.winners)
    print("OUTCOME:", battle.outcome)
    battle.print_battle()
