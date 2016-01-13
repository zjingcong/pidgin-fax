#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import gtk
import pygtk
import sys
import webkit


class BroadcastWindow(gtk.Window):
    def __init__(self, message, sender):
        self.message = message
        self.sender = sender

        gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)
        self.set_title('Broadcast~(○’ω’○)~')
        self.connect('delete_event', self.delete_event)
        self.connect('destroy', self.destroy)
        self.set_border_width(20)
        self.set_keep_above(True)
        self.set_position(1)
        self.set_default_size(480, 297)

        box = gtk.VBox(False, 0)
        button_box = gtk.HBox(False, 0)

        '''
        frame = gtk.Frame('Broadcast message from %s' % sender)
        frame.set_label_align(0.08, 0.6)

        
        message_label = gtk.Label(self.message)
        message_label.set_justify(gtk.JUSTIFY_CENTER)
        message_label.set_line_wrap(True)
        frame.add(message_label)
        '''

        html_message = self.message_pack(self.sender, self.message)

        frame = gtk.Frame()
        view = webkit.WebView()
        view.load_html_string(html_message, '')
        frame.add(view)

        box.pack_start(frame, True, True, 20)

        button = gtk.Button('Acknowledge')
        button.connect('clicked', self.acknowledge, None)
        button.connect_object('clicked', gtk.Widget.destroy, self)
        button.set_border_width(10)
        button_box.pack_start(button, True, False, 0)
        box.pack_start(button_box, False, False, 0)

        self.add(box)
        self.show_all()

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def acknowledge(self, widget, data=None):
        print 'Acknowledge!'
        gtk.main_quit()

    def message_pack(self, sender, message):
        head = 'BROADCAST MESSAGE'
        sender_info = 'From %s' % sender
        para = '%s' % message

        html_message = '<html><body bgcolor="#E8E8E8">' \
                       '<head><style type="text/css"> p{color: #696969} h1{color: #B5B5B5} </style></head>' \
                       '<body>' \
                       '<span style="line-height:15px;"><div align="right"><h1>%s</h1></div>' \
                       '<span style="line-height:0px;"><div align="right"><h3><p>%s</p></div>' \
                       '<span style="line-height:30px;"><div align="center"><h3>%s</h3></div>' \
                       '</body>' \
                       '</html>' % (head, sender_info, para)

        return html_message

    def main(self):
        gtk.main()


if __name__ == '__main__':
    assert len(sys.argv) == 3
    sender = sys.argv[1]
    message = sys.argv[2]
    broadcast_win = BroadcastWindow(message, sender)
    broadcast_win.main()
