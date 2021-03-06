#!/usr/bin/env python
# -*- coding: utf8 -*-

import random

all_list = ['石头', '剪刀', '布']
win_list = [['石头', '剪刀'], ['剪刀', '布'], ['布', '石头']]
prompt = """(0) 石头
(1) 剪刀
(2) 布
Please input your choice(0/1/2): """
pwin = 0
cwin = 0

while pwin < 2 and cwin < 2:
    computer = random.choice(all_list)
    ind = int(raw_input(prompt))
    player = all_list[ind]

    # print "Your choice:", player, "Computer's choice:", computer
    print "Your choice:%s, Computer's choice: %s" % (player, computer)
    if computer == player:
        print "\033[32;1m平局\033[0m"
    elif [player, computer] in win_list:
        pwin += 1
        print "\033[31;1mYou WIN!!!\033[0m"
    else:
        cwin += 1
        print "\033[31;1mYou LOSE!!!\033[0m"
else:
    if pwin == 2:
        print "Finally, You WIN!!!"
    else:
        print "Finally, You LOSE!!!"
