from CeeLo import *

def main():
    playerAmt = int(input("How many players?: "))
    interface = GraphicInterface()
    app = CeeLo(interface, playerAmt)
    app.run()

main()
