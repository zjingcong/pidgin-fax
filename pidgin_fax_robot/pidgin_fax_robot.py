#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re
import dbus
import gobject
from dbus.mainloop.glib import DBusGMainLoop
import subprocess

SEARCH_NAME_TEMPLATE = r'href\=\'(\S+)\'\>'
SEARCH_SENDER_TEMPLATE = r'(\S+)\@'
BROADCAST_MESSAGE_TAG = '[BROADCAST_MESSAGE]'
BROADCAST_WINDOW_CWD = './'

# get authorized users
authorized_user_list = ['zjingcong', 'cxinpeng']


class PidginReceiveRobot:
    def __init__(self, screenshot_on, broadcast_on):
        self.bus = dbus.SessionBus()
        self.secreenshot_on = screenshot_on    # display on or off
        self.broadcast_on = broadcast_on    # broadcast popup on or off

    @staticmethod
    def is_authorized_user(sender):
        if sender not in authorized_user_list:
            return False
        return True

    @staticmethod
    def display_screenshot(message):
        name_info = re.search(SEARCH_NAME_TEMPLATE, message)
        if name_info:
            name = name_info.group(1)
            print name
        else:
            name = message

        subprocess.Popen(['display', name])

    def screenshot_cb(self, account, sender, message, conversation, flags):
        # Chat history message
        if flags == 1025 or flags == 1026:
            return

        title = 'http://media.anim.odw.com.cn/screenshots/'
        if title in message:
            self.display_screenshot(message)

    def broadcast_cb(self, account, sender, message, conversation, flags):
        # Chat history message
        if flags == 1025 or flags == 1026:
            return

        if BROADCAST_MESSAGE_TAG in message:
            if '@' in sender:
                sender_info = re.search(SEARCH_SENDER_TEMPLATE, sender)
                if sender_info:
                    sender = sender_info.group(1)
            if self.is_authorized_user(sender):
                subprocess.Popen(['python', 'broadcast_window.py', sender, message[19:]], cwd=BROADCAST_WINDOW_CWD)

    def receive_signal(self):
        bus = self.bus

        if self.secreenshot_on:
            # listener to received_im_msg
            bus.add_signal_receiver(self.screenshot_cb, dbus_interface="im.pidgin.purple.PurpleInterface",
                                    signal_name="ReceivedImMsg")
            # listener to received_chat_msg
            bus.add_signal_receiver(self.screenshot_cb, dbus_interface="im.pidgin.purple.PurpleInterface",
                                    signal_name="ReceivedChatMsg")

        if self.broadcast_on:
            # listener to received_im_msg
            bus.add_signal_receiver(self.broadcast_cb, dbus_interface="im.pidgin.purple.PurpleInterface",
                                    signal_name="ReceivedImMsg")
            # listener to received_chat_msg
            bus.add_signal_receiver(self.broadcast_cb, dbus_interface="im.pidgin.purple.PurpleInterface",
                                    signal_name="ReceivedChatMsg")


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)

    conn = PidginReceiveRobot(True, True)
    conn.receive_signal()

    loop = gobject.MainLoop()
    loop.run()
