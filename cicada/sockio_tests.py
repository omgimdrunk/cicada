from cicada import _sockio


def intohere(data):
    print(data, end='')


def inetguest(typeinet):
  """
    read_into :: def read_into(self, on_read)

      This will dup the socket but doesn't destroy the parent!
      From this point on it can only read,
      while the parent can only write.
  
  """
  with typeinet('freechess.org', 5000) as muhsock:
    if muhsock.as_guest():
      muhsock.read_into(on_read=intohere)
      while muhsock.is_connected:
        x = input();
        try:
          d_out = muhsock.write(x)
        except Exception as E:
          sys.stderr.write("[{}] : {} {} !err \n".format(time.time(), E, d_out))
          sys.exit()
            
inetguest(INET_TCP)

#
#
#
def inethost(typeinet, ip, port, on_exit=None, on_read=intohere, on_client=None):
    global muhsock
    with typeinet(ip, port, on_exit=on_exit) as muhsock:

        if muhsock.as_host():
            while muhsock.is_connected:
                try:
                    muhsock.getcli(on_client=on_client)

                except:
                    raise
        else:
            print('nope')
            return

        
        
def onexit():
    global muhsock
    print(muhsock.exmsg)


class inet_WO_Context:
    def __init__(self, typeinet, on_exit=None):
        _sock = typeinet('freechess.org', 5000, on_exit=on_exit)
        self.sock = _sock._socket_obj
        self.sock()
        try:
            self.sock.as_guest()
        except Exception as E:
            raise E




class udsguest:
    def __init__(self, sock, uds, on_exit=None):
        try:
            with sock(uds) as self.sock:
                try:
                    if self.sock.as_guest():
                        th = self.sock.read_into(intohere)
                        self.sock.on_exit = th.join
                    else:
                        raise ConnectionError
                except:
                    raise
            print('past context')
            while self.sock.is_connected:
                x = input()
                self.sock.write(x)
        except:
            raise
iwoc = inet_WO_Context(_sockio.INET_TCP)
