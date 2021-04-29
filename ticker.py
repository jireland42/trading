import _thread
import threading
import time
import curses
from curses import wrapper
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
cmc = CoinMarketCapAPI('06bbbdc9-cdbd-461a-92c5-385dc3ccab5e')

stop = False

def wait_for_stop_command(stdscr):
    global stop
    time.sleep(3)
    stdscr.addstr(22, 6, "Press and key to quit", curses.color_pair(3) | curses.A_BOLD)
    stdscr.getkey()
    stdscr.addstr(22, 6, "Please wait for termination", curses.color_pair(3) | curses.A_BOLD)
    #curses.curs_set(0)
    stdscr.refresh()
    stop = True

def display_changes(stdscr, start_col, row, prices, i, decimals):
    # print most recent data
    last_change_col = start_col
    last_percent_change_col = start_col + 15

    last_change = 0
    last_percent_change = 0

    if (i == 0):
        last_change = prices[i] - prices[0]
        last_percent_change = (100 * last_change) / prices[0]
    else:
        last_change = prices[i] - prices[i - 1]
        last_percent_change = (100 * last_change) / prices[i - 1]

    if (last_change > 0):
        stdscr.addstr(row, last_change_col, '$' + str(format(last_change, '.' + decimals + 'f')), curses.color_pair(1))
        stdscr.addstr(row, last_percent_change_col, str(format(last_percent_change, '.2f')) + '%', curses.color_pair(1))
    elif (last_change == 0):
        stdscr.addstr(row, last_change_col, '$' + str(format(last_change, '.' + decimals + 'f')), curses.color_pair(4))
        stdscr.addstr(row, last_percent_change_col, str(format(last_percent_change, '.2f')) + '%', curses.color_pair(4))
    else:
        stdscr.addstr(row, last_change_col, '$' + str(format(last_change, '.' + decimals + 'f')), curses.color_pair(2))
        stdscr.addstr(row, last_percent_change_col, str(format(last_percent_change, '.2f')) + '%', curses.color_pair(2))

    # print short term data if available
    minutes_back_short = 5
    short_change_col = start_col + 30
    short_percent_change_col = start_col + 45

    short_change = 0
    short_percent_change = 0

    if (i >= minutes_back_short):
        short_change = prices[i] - prices[i - minutes_back_short]
        short_percent_change = (100 * short_change) / prices[i - minutes_back_short]
        if (short_change > 0):
            stdscr.addstr(row, short_change_col, '$' + str(format(short_change, '.' + decimals + 'f')), curses.color_pair(1))
            stdscr.addstr(row, short_percent_change_col, str(format(short_percent_change, '.2f')) + '%', curses.color_pair(1))
        elif (short_change == 0):
            stdscr.addstr(row, short_change_col, '$' + str(format(short_change, '.' + decimals + 'f')), curses.color_pair(4))
            stdscr.addstr(row, short_percent_change_col, str(format(short_percent_change, '.2f')) + '%', curses.color_pair(4))
        else:
            stdscr.addstr(row, short_change_col, '$' + str(format(short_change, '.' + decimals + 'f')), curses.color_pair(2))
            stdscr.addstr(row, short_percent_change_col, str(format(short_percent_change, '.2f')) + '%', curses.color_pair(2))
    else:
        stdscr.addstr(row, short_change_col, 'no data', curses.color_pair(4))
        stdscr.addstr(row, short_percent_change_col, 'no data', curses.color_pair(4))

    # print medium term data if available
    minutes_back_medium = 15
    medium_change_col = start_col + 60
    medium_percent_change_col = start_col + 75

    medium_change = 0
    medium_percent_change = 0

    if (i >= minutes_back_medium):
        medium_change = prices[i] - prices[i - minutes_back_medium]
        medium_percent_change = (100 * medium_change) / prices[i - minutes_back_medium]
        if (medium_change > 0):
            stdscr.addstr(row, medium_change_col, '$' + str(format(medium_change, '.' + decimals + 'f')), curses.color_pair(1))
            stdscr.addstr(row, medium_percent_change_col, str(format(medium_percent_change, '.2f')) + '%', curses.color_pair(1))
        elif (medium_change == 0):
            stdscr.addstr(row, medium_change_col, '$' + str(format(medium_change, '.' + decimals + 'f')), curses.color_pair(4))
            stdscr.addstr(row, medium_percent_change_col, str(format(medium_percent_change, '.2f')) + '%', curses.color_pair(4))
        else:
            stdscr.addstr(row, medium_change_col, '$' + str(format(medium_change, '.' + decimals + 'f')), curses.color_pair(2))
            stdscr.addstr(row, medium_percent_change_col, str(format(medium_percent_change, '.2f')) + '%', curses.color_pair(2))
    else:
        stdscr.addstr(row, medium_change_col, 'no data', curses.color_pair(4))
        stdscr.addstr(row, medium_percent_change_col, 'no data', curses.color_pair(4))

    curses.curs_set(0)
    stdscr.refresh()



def main(stdscr):
    # start listening thread
    x = threading.Thread(target=wait_for_stop_command, args=([stdscr]))
    x.start()

    # Clear screen
    stdscr.clear()

    # create window with border
    begin_x = 5; begin_y = 3
    height = 20; width = 120
    #win = curses.newwin(height, width, begin_y, begin_x)
    stdscr.border(0)
    box1 = stdscr.subwin(height, width, begin_y, begin_x)
    box1.box()

    # set up colours
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLUE)

    # set up screen layout
    heading_row = begin_y + 1
    token_col = begin_x + 2 
    price_col = begin_x + 2 + 15
    last_change_col = begin_x + 2 + 30
    last_percent_change_col = begin_x + 2 + 45
    short_change_col = begin_x + 2 + 60
    short_percent_change_col = begin_x + 2 + 75
    medium_change_col = begin_x + 2 + 90
    medium_percent_change_col = begin_x + 2 + 105
    #gain_col = begin_x + 2 + 65
    #percent_gain_col = begin_x + 2 + 80

    # print headers
    stdscr.addstr(heading_row, token_col, "Token", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, price_col, "Price", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, last_change_col, "Change", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, last_percent_change_col, "% Change", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, short_change_col, "5m Change", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, short_percent_change_col, "5m % Change", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, medium_change_col, "15m Change", curses.color_pair(3) | curses.A_BOLD)
    stdscr.addstr(heading_row, medium_percent_change_col, "15m % Change", curses.color_pair(3) | curses.A_BOLD)
    #stdscr.addstr(heading_row, gain_col, "Gain", curses.color_pair(3) | curses.A_BOLD)
    #stdscr.addstr(heading_row, percent_gain_col, "% Gain", curses.color_pair(3) | curses.A_BOLD)
    #curses.curs_set(0)
    stdscr.refresh()

    btc_row = heading_row + 1
    eth_row = heading_row + 2
    yld_row = heading_row + 3

    stdscr.addstr(btc_row, token_col, "BTC", curses.color_pair(3))
    stdscr.addstr(eth_row, token_col, "ETH", curses.color_pair(3))
    stdscr.addstr(yld_row, token_col, "YLD", curses.color_pair(3))

    i = 0
    btc_prices = []
    eth_prices = []
    yld_prices = []

    # build a whitespace string to avoid artefacting when re-painting the price lines
    clear_string = ''
    for c in range(medium_percent_change_col - price_col + 7):
        clear_string += ' '

    while(True):
        # print BTC price
        data = cmc.cryptocurrency_quotes_latest(symbol='BTC')
        btc_price = data.data['BTC']['quote']['USD']['price']
        btc_prices.append(btc_price)
        stdscr.addstr(btc_row, price_col, '$' + str(format(btc_price, '.2f')), curses.color_pair(3))

        # print ETH price
        data = cmc.cryptocurrency_quotes_latest(symbol='ETH')
        eth_price = data.data['ETH']['quote']['USD']['price']
        eth_prices.append(eth_price)
        stdscr.addstr(eth_row, price_col, '$' + str(format(eth_price, '.2f')), curses.color_pair(3))

        # print YLD price
        data = cmc.cryptocurrency_quotes_latest(symbol='YLD')
        yld_price = data.data['YLD']['quote']['USD']['price']
        yld_prices.append(yld_price)
        stdscr.addstr(yld_row, price_col, '$' + str(format(yld_price, '.4f')), curses.color_pair(3))

        display_changes(stdscr, begin_x + 32, btc_row, btc_prices, i, str(2))
        display_changes(stdscr, begin_x + 32, eth_row, eth_prices, i, str(2))
        display_changes(stdscr, begin_x + 32, yld_row, yld_prices, i, str(4))

        # sleep, but remain reasonably responsive
        for second in range(59):
            time.sleep(1)
            if (stop):
                return
            #stdscr.addch(begin_y - 1, begin_x + second + 1, ' ', curses.color_pair(5))
            if (i % 2 == 0):
                stdscr.addch(begin_y - 1, begin_x + (2 * second) + 1, ' ', curses.color_pair(5))
                stdscr.addch(begin_y - 1, begin_x + (2 * second) + 2, ' ', curses.color_pair(5))
            else:
                stdscr.addch(begin_y - 1, begin_x + (2 * second) + 1, ' ', curses.color_pair(6))
                stdscr.addch(begin_y - 1, begin_x + (2 * second) + 2, ' ', curses.color_pair(6))

            stdscr.refresh()

        # prepare for next price
        i += 1

        #clear price lines
        stdscr.addstr(btc_row, price_col, clear_string)
        stdscr.addstr(eth_row, price_col, clear_string)
        stdscr.addstr(yld_row, price_col, clear_string)


# start the main program
wrapper(main)
