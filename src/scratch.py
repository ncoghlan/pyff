# scratch.py -
# Copyright (C) 2007-2008  Bastian Venthur
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


# 1. simple
def mydec(f):
    def _f(*args, **kwargs):
        f(*args, **kwargs)
        print str(i)
    return _f

# 2. ... with argument
def mydec2(i):
    def mydec2_inner(f):
        def _f(*args, **kwargs):
            f(*args, **kwargs)
            print str(i)
        return _f
    return mydec2_inner

# 3. same as 2. but as class:
class mydec3(object):
    def __init__(self, i):
        self.i = i
    def __call__(self, f):
        def _f(*args, **kwargs):
            f(*args, **kwargs)
            print str(self.i)
        return _f

from threading import Thread

# ok, now the real thing
class timeout(object):
    
    def __init__(self, timeout):
        self.timeout = timeout
        
    def __call__(self, f):
        
        def _f(*args, **kwargs):
            worker = ThreadMethodThread(f, args, kwargs)
            if self.timeout is None:
                return worker
            worker.join(self.timeout)
            if worker.isAlive():
                raise ThreadMethodTimeoutError()
            elif worker.exception is not None:
                raise worker.exception
            else:
                return worker.result
            
        return _f

class ThreadMethodTimeoutError(Exception): pass

class ThreadMethodThread(Thread):
    def __init__(self, target, args, kwargs):
        Thread.__init__(self)
        self.target, self.args, self.kwargs = target, args, kwargs
        self.start()
        
    def run(self):
        try:
            self.result = self.target(*self.args, **self.kwargs)
        except Exception, e:
            self.exception = e
        except:
            self.exception = Exception()
        else:
            self.exception = None

@timeout(5)
def infinite_loop():
    while 1:
        pass        

@timeout(5)
def mymethod():
    print "foo"


if __name__ == '__main__':
    try:
        infinite_loop()
    except ThreadMethodTimeoutError, e:
        print "timeout"
    except:
        print "some other exception"

