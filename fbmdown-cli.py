#!/usr/bin/env python
#coding: utf-8
"""
Command-line and interactive interface for fbmdown - Facebook message downloader
"""

import sys
import cmd
import argparse
import time
import fbmdown

class FBMCmdUI(cmd.Cmd):
    ROWSPPAGE = 25
    API_LIMIT = 7000

    def __init__(self, token):
        cmd.Cmd.__init__(self)
        self.fb = fbmdown.FBMDown(token)
        self.pprinter = fbmdown.FBMPPrinters()
        self.prompt = '> '

    def do_quit(self, l):
        print '- Bye!'
        return True

    def do_EOF(self, l):
        self.do_quit(l)

    def do_list(self, l):
        """list
        List names and thread ids of your friends you got messages from"""

        for i, thread in enumerate(self.fb.list_threads(), 1):
            print u'- ID: {0} - {1}'.format(thread.msg_id, thread.sender)
            if i % self.ROWSPPAGE == 0:
                cmd = raw_input('-- Press ENTER to scroll, type q to break -- ')
                if cmd == 'q':
                    break

    def do_download(self, l):
        """download [thread_id, filename]
        Save the given thread_id as filename on your disk"""
        try:
            thread_id, filename = l.split()
        except ValueError:
            print '! Please type exactly 2 arguments. Example: save 1337 chatlog'
            return

        #TODO: This is not working from Windows console
        with file(u'{0}.txt'.format(filename.encode('utf-8')), 'w') as f:
            down_total, down_actual, time_delta = 0, 0, 0
            start = time.time()

            for msg in self.fb.get_thread(thread_id):
                print >> f, self.pprinter.prettify_2(msg)

                if not down_total:
                    down_total = self.fb.last_msg_count
                    if down_total >= self.API_LIMIT:
                        print '! Warning: You have >{0} messages in this thread. This might exceed ' \
                              'Facebook API Limit.'.format(self.API_LIMIT)

                if down_actual % self.fb.OFFSET == 0:
                    time_delta = time.time() - start
                    msgPs = down_actual / time_delta
                    if msgPs > 0:
                        print '- [{0}/{1}] Downloaded. {2:.2f} msg/s. ETA: {3:.2f}s\r'.format(down_actual, down_total,
                            msgPs, (down_total / msgPs) - time_delta),
                down_actual += 1

        print '- {0} saved as {1}.txt Completed in {2:.2f} s'.format(thread_id, filename, time_delta)

parser = argparse.ArgumentParser(description='Facebook Message Downloader')
parser.add_argument('-t', dest='token', help="Facebook Graph API token with 'inbox_read' permissions")
parser.add_argument('-tid', dest='thread_id', help='ID of thread')
parser.add_argument('-o', dest='filename', help='Output file')
q = parser.parse_args()

#
#CLI
#
if q.token and q.thread_id and q.filename:
    print 'Facebook Message Downloader is running in command line mode'
    print '- Checking your token'

    try:
        ui = FBMCmdUI(q.token)
    except fbmdown.FBError, e:
        if e.code == e.INVALID_TOKEN:
            print 'The access token you entered is invalid.'
        sys.exit(0)

    print '- Downloading Thread {0}'.format(q.thread_id)
    ui.do_download(u'{0} {1}'.format(q.thread_id, q.filename))

#
#Interactive
#
else:
    print 'Facebook Message Downloader is running in interactive mode'
    print "See 'fbmsgsave-cli.py -h' for command line arguments"
    print
    print "Please enter your 'Graph API Explorer Access Token'"
    print "See the readme if you don't know how to get it"
    token = raw_input('Access Token: ')

    ui = FBMCmdUI(token)
    print "- Type ? for available commands. Type quit or press CTRL+Z to quit."
    ui.cmdloop()