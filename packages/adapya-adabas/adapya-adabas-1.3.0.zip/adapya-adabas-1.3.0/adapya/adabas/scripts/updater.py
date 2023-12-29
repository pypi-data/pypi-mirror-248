""" Field update test in an Adabas Database

    If a format is provided the given fields will be read and updated.
    Otherwise the field AC (Employees sample file) will be updated.

    Usage:

        updater --dbid <dbid> --fnr <fnr> --isn <isn>
                  [--cred <safuserid>,<safpassword>[,<newpassword>]]
                  [--acbx] [--cinfo]
    Options:

        -d, --dbid              <dbid> is a valid dbid
        -f  --fnr               Adabas file number <fnr>
        -i  --isn <isn>         Adabas record number (ISN)

        -c  --format            format of requested fields. With this
                                  parameter --value is taken for the update
                                  if omitted implicit format AA,AC fields
                                  for Employees sample file is used

        -C, --cinfo             include client info with Adabas call

        -b, --backout           backout any changes
        -e, --etid <etid>       ETID to be specified with OP cmd
        -k  --cred  <uid>,<psw>[,newpsw]  Userid, password and optionally new
                                  password for security system (ADASAF)
        -n, --noclose           leave session open (use for testing only)
                                  and do not start with OP
                                  and do blind update (w/o reading record before)
        -r  --replytimeout <n>  number <n> of seconds of outstanding reply until timeout

        -s  --store             instead of update perform a store (N1/N2 with ISN)

        -v  --verbose <level>   log adabas buffers: sum of values:
                                  1 = after call  2 = before  4 = performance buffer
        -w  --value <value>     Update value  (this is used in combination
                                  of --format)
                                  if value is not given the input is prompted
        -x, --xopt              eXtended Adabas call with ACBX and ABDX buffers

        Example:
        Change the AA field of record 100 in Employee file 11 db 8 to 12345678
        updater -d8 -f11 -v1 -bn -i100 -c AA. -w "12345678"

        Increment ST field and backout change
        updater -d10025 -f50 -b -i100 -c ST,4,B.


        Update AC field (Employees Name) with a new value for ISN 100
        updater -d10028 -f11 -i100

        Update P2,2,P field with packed number 123
        (non printable characters specified in hex \\xnn
        updater -d1 -f2 -i100 -c P2. -w \\x12\\x3f



"""
from __future__ import print_function          # PY3


import time
import string
import getopt
import sys
from struct import pack, unpack

from adapya.base import dump
from adapya.base.defs import log,LOGSP,LOGRSP,LOGCB,LOGRB,LOGFB,LOGCMD,\
    LOGBEFORE,LOGPB,evalb # evals
from adapya.adabas.api import Adabas, Adabasx, DatabaseError, setsaf, adaSetTimeout

def usage():
    print(__doc__)



fnr = 0
dbid = 0
cinfo = False
etid = ''
xopt = 0
replytimeout = 7200 # 2 hours for testing
backout = 0
noclose = 0
format = ''
value = ''
isn = 0
safnew = ''
safid = ''
safpw = ''
store = 0
verbose = 0
opts = []
args = []


try:
    opts, args = getopt.getopt(sys.argv[1:],
      'Cc:hbd:e:f:i:k:nr:sv:w:x',
      ['cinfo','cred=','format=','help','backout','dbid=','etid=','fnr=','isn=','noclose','replytimeout=',
       'store','usr=','verbose=','pwd=','value=','xopt'])
except getopt.GetoptError:
    print(opts, args)
    usage()
    sys.exit(2)
for opt, arg in opts:
    if opt in ('-h', '--help'):
        usage()
        sys.exit()
    elif opt in ('-b', '--backout'):
        backout=1
    elif opt in ('-d', '--dbid'):
        dbid=int(arg)
    elif opt in ('-e', '--etid'):
        etid = arg
    elif opt in ('-f', '--fnr'):
        fnr=int(arg)
    elif opt in ('-c', '--format'):
        format=arg
    elif opt in ('-C', '--cinfo'):
        cinfo = True
    elif opt in ('-w', '--value'):
        value = evalb(arg)   # evals(arg) returns unicode string
        dump.dump(value,'--value dump:')
    elif opt in ('-i', '--isn'):
        isn=int(arg)
    elif opt in ('-k', '--cred'):
        ss = arg.split(',')
        if len(ss) == 2:                # need 2 or 3 parts
            safid, safpw = ss
        else:
            safid, safpw, safnew = ss
    elif opt in ('-n', '--noclose'):
        noclose = 1
    elif opt in ('-r', '--replytimeout'):
        replytimeout=int(arg)
    elif opt in ('-s', '--store'):
        store = 1
    elif opt in ('-v', '--verbose'):
        verbose=int(arg)
    elif opt in ('-x', '--xopt'):
        xopt = 1

    else:
        print(opts)
        print('invalid parameter %s' % arg)
        usage()
        sys.exit(2)

print('-'*80) # start of program

if isn == 0 and not store:
    print('Parameter ISN (-i --isn) required for update')
    usage()
    sys.exit(2)

if sys.hexversion >= 0x3010100: # PY3
    PY3 = True
    getinput = input

    def bytenow(encoding):
        return now().encode(encoding)
else:
    PY3 = False
    getinput = raw_input

    def bytenow(encoding):
        return now()

if xopt:
    c1=Adabasx(fbl=64,rbl=512,clientinfo=cinfo)
    c1.cb.dbid=dbid
else:
    c1=Adabas(fbl=64,rbl=128)
    c1.dbid=dbid

c1.cb.fnr=fnr

LOG=LOGRSP
LOGMIN = LOGRSP
if verbose & 4: # log performance buffer (client info)
    LOG |= LOGPB
if verbose & 2: # LOG before call
    LOG |= LOGCMD|LOGCB|LOGSP|LOGRB|LOGFB|LOGBEFORE
if verbose & 1: # Log after call
    LOG |= LOGCMD|LOGCB|LOGSP|LOGRB|LOGFB
    LOGMIN |= LOGCB
log(LOGMIN)

if replytimeout:
    rsp=adaSetTimeout(replytimeout)

if safid and safpw:
    i = setsaf(safid, safpw, safnew)
    if i:
        print('Setting adasaf parameter returned %d' % i)
    else:
        print('setsaf() with userid %r was called successfully' % safid)

try:
    if noclose: # includes blind update (no reading of record)
        i = 1
        c1.cb.cid='A1AA'
        c1.cb.isn=isn
        if format and value:
            c1.fb.write(format)
            c1.rb.write(value)
        else:
            c1.fb.write('AC,8,AA.')
            c1.rb[0:20]=b'BLINDUPDATE%08d'% i

        log(LOG)
        c1.update(hold=1)

    else:
        log(LOGMIN|LOGCMD)
        if etid:
            c1.open(etid=etid)
        else:
            c1.open()
        log(LOG)
        c1.cb.cid='A1AB'
        c1.cb.isn=isn

        if format:
            c1.fb.write(format)

            if store:
                c1.rb.seek(0)
                c1.rb.write(value)
                if xopt:
                    c1.rabd.send = c1.rb.tell() # set send size for record buffer

                c1.store(isn=isn)
            else:
                c1.get(hold=1)
                cont = getinput('After read with hold. Hit <ENTER> to continue with update')

                if format == 'ST,4,B.':
                    # increment unsigned integer field
                    v = unpack( '=L', c1.rb[0:4])
                    v += 1
                    if v > 99999999:
                        v=1
                    c1.rb[0:4] = pack( '=L', v)

                else:
                    # free format and string value update
                    cont=''
                    while not cont:
                        if value:
                            c1.rb.seek(0)
                            c1.rb.write(value)
                            if xopt:
                                c1.rabd.send = c1.rb.tell() # set send size for record buffer
                        else:
                            value=getinput('Enter value for update:')
                            if value:
                                c1.rb.seek(0)
                                c1.rb.write(value)
                                if xopt:
                                    c1.rabd.send = c1.rb.tell() # set send size for record buffer
                            else:
                                raise KeyboardInterrupt
                            value = '' # reset value
                        c1.update()
                        cont = getinput('After update: enter C to continue or <ENTER> repeat update')


        else:   # update incrementing value in field AC
            if store:
                if xopt:
                    c1.rabd.send=128           # set send size for record buffer
                c1.store(isn=isn)
            else:
                c1.fb.write('AC,AA.')
                c1.get(hold=1)
                cont = getinput('After read with hold; Hit <ENTER> to continue')
                try:
                    i=1+int(c1.rb.value[11:15])
                except ValueError:
                    i=1
                c1.rb[0:20] = b'HUNDERTMARK%04d     ' % i
                if xopt:
                    c1.rabd.send = 20 # set send size for record buffer
                c1.update()

            cont=getinput('After %s; Hit <ENTER> to continue' % ('store' if store else 'update') )

    log(LOGMIN|LOGCMD)
    if not backout:
        c1.et()

except DatabaseError as e:
    print( 'Database %5d --'%dbid, e.value)
    dump.dump(e.apa.acb, header='Control Block')
    dump.dump(e.apa.rb, header='Record Buffer')
    raise
except KeyboardInterrupt:
    # clean up
    print('\nTerminating due to KeyboardInterrupt')
finally:
    # cont=getinput('Before Termination Clean up (BT/CL)\nHit <ENTER> to continue')
    log(LOGMIN|LOGCMD)
    c1.bt()
    if not noclose:
        c1.close()
#
