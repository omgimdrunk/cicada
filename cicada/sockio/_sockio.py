import socket
import os
import sys
import threading
import traceback
from loguru import logger

__all__ = ['INET_TCP', 'UDS_TCP']


class SOCKIO_XCEPT(Exception):
    conerr = ConnectionError
    socktimeout = socket.timeout

    def __call__(self, msg=None):
        return msg

    @staticmethod
    def timeout(msg=None):
        return SOCKIO_XCEPT.socktimeout(msg)

    @staticmethod
    def sock_closed(msg=None):
        print(SOCKIO_XCEPT.conerr(msg))

    @staticmethod
    def user_interupt():
        msg =  '¯\_(ツ)_/¯ User Interupt'
        return SOCKIO_XCEPT(msg)

#
# Lib Catchall, not working yet. Needs to be nested and called from itself, otherwise
# the raise passes back to the calling function
#

def _FLEX_CEPT(proc):
    def wrap(*args, **kwargs):
        try:
            sult = proc(*args, **kwargs)
        except KeyboardInterrupt:
            sys.stdout.write(str(SOCKIO_XCEPT.user_interupt()))
            sys.exit()
        except SOCKIO_XCEPT.timeout:
            raise
        except SOCKIO_XCEPT.conerr as E:
            print(E())
            sys.exit()

        except Exception as E:
            psult = 'tmplogger {} \n {}'.format(E, traceback.walk_tb(E))
            print(psult)
            raise
        else:
            return sult
    return wrap


def ascii_decode(sbytes):
    try:
        _data = sbytes.decode("ascii")
    except:
        _data = ''
        for i in sbytes:
            _data += chr(i)
    return _data


class INET_TCP:
    def __init__(self, addr: str, port: int, on_exit=None, is_connected=False):

        _obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._socket_obj = _SockIO(_obj)
        self._host_addr = addr
        self._host_port = port
        self._socket_obj.connector = (self._host_addr, int(self._host_port))
        self._is_connected = is_connected
        self.on_exit = on_exit

    def __call__(self, *args, **kwargs):
        print('at call')


    def __enter__(self):
        return self._socket_obj

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._socket_obj.halt()
        if self.on_exit:
            self.on_exit()


class _inet_gram(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM)


class UDS_TCP:

    def __init__(self, addr: str, on_exit=None, is_connected=False):

        _obj = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        _obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._socket_obj = _SockIO(_obj)
        self._host_addr = addr
        self._socket_obj.connector = self._host_addr
        self._is_connected = is_connected
        self._socket_obj.on_exit = on_exit

    def __enter__(self):
        return self._socket_obj

    def __exit__(self, exc_type, exc_val, exc_tb):

        if self._socket_obj.on_exit:
            self._socket_obj.on_exit()
        self._socket_obj.halt()


class _uds_gram(socket.socket):
    def __init__(self):
        super().__init__(socket.AF_UNIX, socket.SOCK_DGRAM)


#
# main socket object
#


class _SockIO:

    def __init__(self, _sock:socket.socket):

        self.sock: socket.socket = _sock
        self.connector = None
        self.is_connected = False
        self._timeout = None
        self.on_exit = None

    def settimeout(self, sec: float):
        self._timeout = sec
        self.sock.settimeout(sec)

    def halt(self):
        self.sock.close()
        self.is_connected = False

    def as_guest(self):
        try:
            self.sock.connect(self.connector)
        except Exception as E:
            self.halt()
            return False
        else:
            self.is_connected = True
            return True

    def stream_from(self):
        data, addr = self.sock.recvfrom(1024)
        return '{} :: {}'.format(addr, data)

    def stream_to(self, data, send_ip, send_port):
        self.sock.sendto(data, (send_ip, send_port))

    def as_host(self):
        try:
            self.sock.bind(self.connector)
        except Exception as E:
            self.halt()
            print(E)

        else:
            self.sock.listen(1)
            self.is_connected = True
            return True

    def read_into(self, on_read):
        _th = threading.Thread(target=self._hndl_read, args=(self, on_read))
        _th.start()
        return _th

    @logger.catch
    def _hndl_read(self, sock, read_into):
        while sock.is_connected:
            try:
                if sock._timeout:
                    sock.settimeout(sock._timeout)
                data = sock.read()
            except SOCKIO_XCEPT.socktimeout:
                pass
            except OSError as E:
                return SOCKIO_XCEPT.sock_closed(E)
            except Exception as E:
                print('other err line 184', E.args)
                raise E

            else:
                read_into(data)

        print('ending reading')

    def read(self):
        try:
            data = self.sock.recv(1024)
            while b'\r' not in data:
                peek = self.sock.recv(1024)
                if len(peek) == 0:
                    raise SOCKIO_XCEPT.conerr(self.sock)
                data += peek
        except SOCKIO_XCEPT.socktimeout:
            raise SOCKIO_XCEPT.socktimeout
        except:
            raise
        else:
            return ascii_decode(data)

    def write(self, data):
        _data = '{}\n\r'.format(data).encode()
        try:
            self.sock.sendall(_data)
        except SOCKIO_XCEPT.socktimeout:
            self.halt()
            raise SOCKIO_XCEPT.socktimeout
        except:
            raise

    def getcli(self, on_client=None):
        try:
            c, a = self.sock.accept()
            _newcli = _SockIO(c)
            _newcli.is_connected = True
            _newcli.connector = a
        except:
            self.halt()
            raise
        else:
            if on_client:
                #
                # Move thread to its own function, or probably a generator class
                # That will also sit at join()
                #
                th = threading.Thread(target=on_client, args=(_newcli,))
                th.start()
            else:
                return _newcli
