from cicada import sockio
import te_main
import threading
import os
import time


def show_event(event):
    print('atonkey')
    print(event)


def start_cli():
    try:
        os.remove('/tmp/te_sock')
    except:
        pass

    with sockio.UDS_TCP('/tmp/te_sock') as te_sock:
        if te_sock.as_host():
            cli = te_sock.getcli()
            te = te_main._hndlTE(on_key=cli.write)
            cli.settimeout(.5)

            cli.read_into(te.cmd_ctrl)
            te.mainloop()

            return

#start_cli()


th = threading.Thread(target=start_cli)
th.start()

time.sleep(.1)

curline = 1
with sockio.UDS_TCP('/tmp/te_sock') as tewatch:
    if tewatch.as_guest():
        def mvline(c, n):
            tewatch.write('line_select {} {}'.format(c, n))
        while tewatch.is_connected:

            try:
                buff = tewatch.read()
            except sockio.SOCKIO_XCEPT.socktimeout:
                pass
            else:
                print(buff)
                if 'Return' in buff:
                    newline = curline + 1
                    mvline(curline, newline)
                    curline = newline
                elif 'Up' in buff:
                    newline = curline - 1
                    if newline < 1:
                        newline = 1
                    mvline(curline, newline)
                    curline = newline

