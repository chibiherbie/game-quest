from send_msg import s_m
import config
from bots_info.journalist import journalist_info
from text_const import edit_text


# ----новости----

def news_1():
    s_m(edit_text(journalist_info[0]), config.TOKEN_JOURNALIST)


def news_2():
    s_m(edit_text(journalist_info[1]), config.TOKEN_JOURNALIST)


def news_3():
    s_m(edit_text(journalist_info[2]), config.TOKEN_JOURNALIST)


def news_4():
    s_m(edit_text(journalist_info[3]), config.TOKEN_JOURNALIST)


def news_5():
    s_m(edit_text(journalist_info[4]), config.TOKEN_JOURNALIST)


def news_end1():
    s_m(edit_text(journalist_info[5]), config.TOKEN_JOURNALIST)


def news_end2():
    s_m(edit_text(journalist_info[6]), config.TOKEN_JOURNALIST)