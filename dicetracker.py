#!/usr/bin/env python3

from hdwallet import HDWallet
from hdwallet.symbols import BTC, ETH, LTC, BCH, BSV, DASH, ZEC, DOGE, BTCTEST
from monero.seed import Seed
import qrcode
import os
import pdfkit
from os.path import exists


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


# Checks if string is binary
def check_bin(string):
    # every char will be checked if it is in the string '01'
    t = '01'
    if all(char in t for char in string):
        return True
    else:
        return False


def getListOfFiles(dirName):
    # create a list of file and sub directories
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


# Checks if string contains the results of dice rolls (1 to 6)
def check_dice(string):
    # every char will be checked if it is in the string '01'
    t = '123456'
    if all(char in t for char in string):
        return True
    else:
        return False


# Converts string made by numbers from 1 to 6 to a binary string
def six_to_bin(string):
    binstr = ''
    for diceres in string:
        nn = int(diceres)
        binnn = nn % 2
        cc = str(binnn)
        binstr += cc
    return binstr


# Generates QR codes of keystr and stores them in a png file
def makeqr(keystr, filename):
    img = qrcode.make(keystr)
    type(img)
    filename = 'PaperWallet/' + filename
    img.save(filename)


# Intro
print(color.YELLOW + 'Welcome to dice tracker!' + color.END)
print('This tool derives private keys and public addresses from 256 bits binary keys')
print('Key can be pasted by the user (in binary or as the result of dice rolls) or can be inserted tracking the result of 256 dice rolls')

# Stores the binary string
dicestr = ''
print(color.GREEN + '\nDo you want to paste a binary key or the result of previous dice rolls?(y/n)' + color.END)
print('Unless this tool will help you tracking dice rolls')
tour0 = 1
ans = ''    # decides if the user pastes key or wants to track dice rolls
while tour0:
    ans = input()
    if ans == 'y' or ans == 'Y' or ans == 'n' or ans == 'N':
        tour0 = 0
    else:
        print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)

# User wants to paste the key
if ans == 'y' or ans == 'Y':
    tour = 1
    while tour:
        is_bin = False
        is_dice = False
        dicestr = input('Paste your string now with Ctrl + Shift + V\nnote that it must be 256 digits long\n')
        if len(dicestr) != 256:
            print(color.RED + 'Binary key has to be 256 digits long' + color.END)
        else:
            is_bin = check_bin(dicestr)
            is_dice = check_dice(dicestr)
            if is_bin:
                print(color.GREEN + 'String accepted!' + color.END)
                tour = 0
            elif is_dice:
                dicestr = six_to_bin(dicestr)
                print(color.GREEN + 'String accepted and converted to binary!' + color.END)
                tour = 0
            else:
                print(color.RED + 'String is not binary or is not the result of dice rolls!' + color.END)
                print(color.YELLOW + 'It has to contain only 0 and 1 or only numbers from 1 to 6' + color.END)

# user wants to track dice rolls
elif ans == 'n' or ans == 'N':
    # input result of dice rolls
    print(color.GREEN + "Let's go! This may take a while" + color.END)
    print('Simply type the result of each time you roll your dice')
    dicerolls = 0
    while dicerolls < 256:
        res = input(f'insert {dicerolls +1} number: ')
        if res.isdigit():
            res = int(res)
            if res > 6 or res < 1 or res == '':
                print(color.RED + 'Unallowed input! Only 6 faces dices are supported' + color.END)
            else:
                res = res % 2
                res = str(res)
                dicestr += res
                dicerolls += 1
        else:
            print(color.RED + 'Unallowed input!' + color.END)

# Printing the result of all the dice rolls
    print(color.DARKCYAN + '\nThis is your binary key:' + color.END)
    print(dicestr)

# Converting binary to HEX
hexadecimal = '%0*X' % ((len(dicestr) + 3) // 4, int(dicestr, 2))

print(color.DARKCYAN + '\nThis is your hex key:' + color.END)
print(hexadecimal)

# Coin selection
coins_dict = {1: BTC, 2: ETH, 3: LTC, 4: BCH,
              5: BSV, 6: DASH, 7: ZEC, 8: DOGE, 9: BTCTEST}
print(color.DARKCYAN + '\nPlease select coin (write the corresponding numerical index):' + color.END)
print(' 1 -> Bitcoin')
print(' 2 -> Ethereum')
print(' 3 -> Litecoin')
print(' 4 -> Bitcoin Cash')
print(' 5 -> Bitcoin SV')
print(' 6 -> Dash')
print(' 7 -> ZCash')
print(' 8 -> DogeCoin')
print(' 9 -> Bitcoin Testnet')
print('10 -> Monero')
tour2 = 1
while tour2:
    coin_sel = input(color.DARKCYAN + 'Coin: ' + color.END)
    coin_sel = int(coin_sel)
    if coin_sel > 0 and coin_sel < 10:
        print(color.GREEN + f'Selected coin: {coins_dict[coin_sel]}' + color.END)
        tour2 = 0
    elif coin_sel == 10:
        print(color.GREEN + 'Selected coin: XMR' + color.END)
        tour2 = 0
    else:
        print(color.RED + 'Unaccepted value!' + color.END)
        print('Type a number between 1 and 10')

# Check if user wants a printable paper wallet
tour3 = 1
qr = False
print(color.GREEN + 'Do you want DiceTracker to generate a printable paper wallet?' + color.END)
while tour3:
    qr_ans = input()
    if qr_ans == 'y' or qr_ans == 'Y':
        qr = True
        tour3 = 0
    elif qr_ans == 'n' or qr_ans == 'N':
        qr = False
        tour3 = 0
    else:
        print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)

# Create directory to store files
if qr:
    tour4 = True
    print(color.RED + 'Now the PaperWallet directory will be cleaned! Backup your previous paper wallets!' + color.END)
    while tour4:
        ans4 = input(color.RED + 'Do you want to continue?(y/n)\n' + color.END)
        if ans4 == 'y' or ans4 == 'Y':
            tour4 = False
        elif ans4 == 'n' or ans4 == 'N':
            quit('Exiting to avoid the deletion of pretious files')
        else:
            print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)
    dir = os.path.join('PaperWallet')
    if os.path.exists(dir):
        lof = getListOfFiles('PaperWallet')
        if 'PaperWallet/address1.png' in lof:
            os.remove('PaperWallet/address1.png')
        if 'PaperWallet/address2.png' in lof:
            os.remove('PaperWallet/address2.png')
        if 'PaperWallet/address3.png' in lof:
            os.remove('PaperWallet/address3.png')
        if 'PaperWallet/ssk.png' in lof:
            os.remove('PaperWallet/ssk.png')
        if 'PaperWallet/svk.png' in lof:
            os.remove('PaperWallet/svk.png')
        if 'PaperWallet/private_key.png' in lof:
            os.remove('PaperWallet/private_key.png')
        if 'PaperWallet/paperwallet.pdf' in lof:
            os.remove('PaperWallet/paperwallet.pdf')
        if 'PaperWallet/temp.html' in lof:
            os.remove('PaperWallet/temp.html')
    else:
        os.mkdir('PaperWallet')


# Derivation
print(color.DARKCYAN + '\n=== KEYS AND ADDRESSES ===' + color.END)
if coin_sel > 0 and coin_sel < 10:
    coin = coins_dict[coin_sel]
    # Initialize wallet
    hdwallet: HDWallet = HDWallet(symbol=coin)
    # Obtain wallet from private key
    hdwallet.from_private_key(private_key=hexadecimal)
    # printing keys
if coin_sel == 2:
    # Ethereum Private key
    ETH_priv = '0x' + str(hexadecimal)
    print(f'Wallet private key: {ETH_priv}')
    if qr:
        makeqr(ETH_priv, 'private_key.png')
    addr1 = hdwallet.p2pkh_address()
    print('P2PKH Address: ', addr1)
    if qr:
        makeqr(addr1, 'address1.png')
elif coin_sel == 1 or (coin_sel > 2 and coin_sel < 10):
    # Print WIF private key
    WIF_priv = hdwallet.wif()
    print('Wallet Important Format private key: ', WIF_priv)
    if qr:
        makeqr(WIF_priv, 'private_key.png')
    addr1 = hdwallet.p2pkh_address()
    print('P2PKH Address: ', addr1)
    if qr:
        makeqr(addr1, 'address1.png')
    if coin_sel == 1 or coin_sel == 3:
        addr2 = hdwallet.p2wpkh_in_p2sh_address()
        print('P2WPKH-P2SH Address: ', addr2)
        if qr:
            makeqr(addr2, 'address2.png')
        addr3 = hdwallet.p2wpkh_address()
        print('P2WPKH Address: ', addr3)
        if qr:
            makeqr(addr3, 'address3.png')
elif coin_sel == 10:
    # Monero derivation
    s = Seed(hexadecimal)
    ssk = s.secret_spend_key()
    print('Secret spend key: ' + ssk)
    svk = s.secret_view_key()
    print('Secret view key: ' + svk)
    psk = s.public_spend_key()
    print('Public spend key: ' + psk)
    pvk = s.public_view_key()
    print('Public view key: ' + pvk)
    addr1 = str(s.public_address())
    print('Primary address: ' + addr1)
    if qr:
        makeqr(ssk, 'ssk.png')
        makeqr(svk, 'svk.png')
        makeqr(addr1, 'address1.png')


# generating HTML (temporary) and PDF File
ft = open('PaperWallet/temp.html', 'w')
ft.write('<!doctype html>\n<body>')
if exists('PaperWallet/logo.png'):
    ft.write('<p><img src="logo.png" width="100" height="100"></p>')
ft.write('<h4>PAPER WALLET</h4>')
if coin_sel < 10:
    ft.write('<p>Coin: ' + str(coins_dict[coin_sel]) + '</p>')
elif coin_sel == 10:
    ft.write('<p>Coin: XMR</p>')
ft.write('<p><strong>Public address: </strong>' + addr1 + '</p>')
ft.write('<p><img src="address1.png" width="200" height="200"></p>')
if coin_sel == 1 or coin_sel == 3:
    ft.write('<p><strong>Segwit address: </strong>' + addr2 + '</p>')
    ft.write('<p><img src="address2.png" width="200" height="200"></p>')
    ft.write('<p><strong>Bech32 address: </strong>' + addr3 + '</p>')
    ft.write('<p><img src="address3.png" width="200" height="200"></p>')
if coin_sel == 2:
    ft.write('<p><strong>Private key: </strong>' + ETH_priv + '</p>')
    ft.write('<p><img src="private_key.png" width="200" height="200"></p>')
elif coin_sel == 10:
    ft.write('<p><strong>Secret spend key: </strong>' + ssk + '</p>')
    ft.write('<p><img src="ssk.png" width="200" height="200"></p>')
    ft.write('<p><strong>Secret view key: </strong>' + svk + '</p>')
    ft.write('<p><img src="svk.png" width="200" height="200"></p>')
else:
    ft.write('<p><strong>Private key: </strong>' + WIF_priv + '</p>')
    ft.write('<p><img src="private_key.png" width="200" height="200"></p>')
ft.write('<p></p><p></p><p><em>Made with dicetracker.py<br>More info at https://anubitux.org</em></p>')
ft.write('</body>')
ft.close()
pdfkit.from_file('PaperWallet/temp.html', 'PaperWallet/paperwallet.pdf')
os.remove('PaperWallet/temp.html')

if qr:
    print(color. DARKCYAN + '\nYour paper wallet can be found in the PaperWallet directory in the DiceTracker.py folder' + color.END)
print('')
