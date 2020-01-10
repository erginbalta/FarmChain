import UI.Search as src
import UI.User as usr
import UI.Miner as mnr
import UI.SignUp as sgn

def menu():
    while(True):
        print("x"*20)
        print("1-> Search")
        print("x"*10)
        print("2-> User Log In")
        print("x"*10)
        print("3-> Miner Log In")
        print("x" * 10)
        print("4-> Sign Up")
        print("x"*10)
        print("5-> EXIT")
        print("x"*20)
        ch = int(input("Enter Choice : "))
        if ch == 1:
            src.searchProduct()
        elif ch == 2:
            usr.userEnterScreen()
        elif ch == 3:
            mnr.minerEnter()
        elif ch == 4:
            sgn.signUpScreen()
        elif ch == 4:
            break
        else:
            print(">> Enter Number <<")

def main():
    menu()


if __name__ == '__main__':
    main()

