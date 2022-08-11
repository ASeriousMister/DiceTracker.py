#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH, LTC, BCH, BSV, DASH, ZEC, DOGE, BTCTEST


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def check_bin(string):
    # every char will be checked if it is in the string '01'
    t = '01'
# registers failure
    fail = 0
# iterate through the string
    for char in string:
        if char not in t:
            fail = 1
            break
        else:
            pass
# returns True or False
    if fail:
        return False
    else:
        return True


# Intro
print(color.YELLOW + 'Welcome to dice tracker!' + color.END)
print('This tool derives private keys and public addresses from 256 bits binary keys')
print('Binary key can be pasted by the user or can be inserted tracking the result of 256 dire rolls')

# Stores the binary string
dicestr = ''

print(color.GREEN + '\nDo you want to paste a binary key?(y/n)' + color.END)
print('Unless this tool will help you tracking dice rolls')
tour0 = 1
while tour0:
    ans = input()
    if ans == 'y' or ans == 'Y' or ans == 'n' or ans == 'N':
        tour0 = 0
    else:
        print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)
# user wants to paste the key
if ans == 'y' or ans == 'Y':
    tour = 1
    while tour:
        dicestr = input('Paste your string now with Ctrl + Shift + V\nnote that it must be 256 bits long\n')
        if len(dicestr) != 256:
            print(color.RED + 'Binary key has to be 256 bits long' + color.END)
        elif check_bin(dicestr) is False:
            print(color.RED + 'String is not binary! It has to contain only 0 and 1' + color.END)
        else:
            print(color.GREEN + 'String accepted!' + color.END)
            tour = 0
# user wants to track dice rolls
elif ans == 'n' or ans == 'N':
    # input result of dice rolls
    print(color.GREEN + "Let's go! It may take some time" + color.END)
    print('Simply tipe the result of each time you roll your dice')
    dicerolls = 0
    while dicerolls < 256:
        res = input(f'insert {dicerolls +1} number: ')
        if res == '':
            print(color.RED + 'Unallowed input!' + color.END)
        elif res.isalpha():
            print(color.RED + 'Unallowed input!' + color.END)
        else:
            res = int(res)
            if res > 6 or res < 1 or res == '':
                print(color.RED + 'Unallowed input!' + color.END)
            else:
                res = res % 2
                res = str(res)
                dicestr += res
                dicerolls += 1
# Printing the result of all the dice rolls
    print(color.DARKCYAN + '\nThis is your binary key:' + color.END)
    print(dicestr)

# converting binary to HEX
hexadecimal = '%0*X' % ((len(dicestr) + 3) // 4, int(dicestr, 2))

print(color.DARKCYAN + '\nThis is your hex key:' + color.END)
print(hexadecimal)

# Coin selection
coins_dict = {1: BTC, 2: ETH, 3: LTC, 4: BCH, 5: BSV, 6: DASH, 7: ZEC, 8: DOGE, 9: BTCTEST}
print(color.DARKCYAN + 'Please select coin (write the corresponding numerical index):' + color.END)
print('1 -> Bitcoin')
print('2 -> Ethereum')
print('3 -> Litecoin')
print('4 -> Bitcoin Cash')
print('5 -> Bitcoin SV')
print('6 -> Dash')
print('7 -> ZCash')
print('8 -> DogeCoin')
print('9 -> Bitcoin Testnet')
tour2 = 1
while tour2:
    coin_sel = input(color.DARKCYAN + 'Coin: ' + color.END)
    coin_sel = int(coin_sel)
    if (coin_sel > 0 and coin_sel < 10):
        print(color.GREEN + f'Selected coin: {coins_dict[coin_sel]}' + color.END)
        tour2 = 0
    else:
        print(color.RED + 'Unaccepted value!' + color.END)
        print('Type a number between 1 and 9')


# Derivation
print(color.DARKCYAN + '\n=== KEYS AND ADDRESSES ===' + color.END)
coin = coins_dict[coin_sel]
# Initialize wallet
hdwallet: HDWallet = HDWallet(symbol=coin)
# Obtain wallet from private key
hdwallet.from_private_key(private_key=hexadecimal)
# printing keys
if coin_sel == 2:
    print(f'Wallet private key: 0x{hexadecimal}')
else:
    print('Wallet Important Format private key: ', hdwallet.wif())
print('P2PKH Address: ', hdwallet.p2pkh_address())
if ((coin_sel == 1) or (coin_sel == 3)):
    print('P2WPKH-P2SH Address: ', hdwallet.p2wpkh_in_p2sh_address())
    print('P2WPKH Address: ', hdwallet.p2wpkh_address())
print('')