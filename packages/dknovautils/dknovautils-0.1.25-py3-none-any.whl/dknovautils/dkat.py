
from typing import Any
import dknovautils
from dknovautils.commons import *

import threading

import http.server
import socketserver


DkAppVer = '0.1.25'

_unknown_err = '_unknown_err4035'

class staticproperty(property):
    """
    https://stackoverflow.com/questions/1697501/staticmethod-with-property

    """
    def __get__(self, owner_self, owner_cls):         
        return self.fget()

class classproperty(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class AT(object):

    _innerLoggerFun_ = None

    _AstErrorCnt_ = 0
    _err_msgs = deque(maxlen=10)

    __logger = None

    _is_windows = sys.platform.startswith('win')
    _is_linux = sys.platform.startswith('linux')
    
    @classproperty
    def is_windows(cls):
        # r=sys.platform.startswith('win')
        r=cls._is_windows
        return r
    
    @classproperty
    def is_linux(cls):
        # r=sys.platform.startswith('win')
        r=cls._is_linux
        return r    

    @classmethod
    def logger(cls, loggerName='dkn'):
        if cls.__logger is None:
            logger = logging.getLogger(loggerName)
            cls.__logger = logger

        return cls.__logger

    @staticmethod
    def log_loggerFun(loggerName='dkn', initInnerLoggerFun=True, beepError=True, beepWarn=False):
        '''
        创建一个logger 作为系统的缺省logger
        '''

        _logger = logging.getLogger(loggerName)

        def mloggerFun(obj, llevel):
            assert isinstance(llevel, LLevel)
            if False:
                pass
            elif llevel == LLevel.Trace:
                # 也用debug级别。只是在prod模式下可以关闭。
                _logger.debug(obj)
            elif llevel == LLevel.Debug:
                _logger.debug(obj)
            elif llevel == LLevel.Info:
                _logger.info(obj)
            elif llevel == LLevel.Warn:
                _logger.warning(obj)
                if beepWarn:
                    AT.beep_error_buffered()
            elif llevel == LLevel.Error:
                _logger.error(obj)
                if beepError:
                    AT.beep_error_buffered()
            else:
                assert False, f"bad {llevel}"

            pass

        if initInnerLoggerFun:
            AT._innerLoggerFun_ = mloggerFun

        return mloggerFun

    _LOG_FORMAT_100 = "%(asctime)s - %(levelname)s - %(message)s"
    _DATE_FORMAT_100 = "%m/%d/%Y %H:%M:%S %p"
    # _DATE_FORMAT_iso_simple = "%m/%d/%Y %H:%M:%S %p"

    STRFMT_ISO_COMPACT_SIMPLE = "%Y%m%dT%H%M%S"
    STRFMT_ISO_COMPACT_ALL_A = "%Y%m%dT%H%M%SS%fZ%Z"
    STRFMT_ISO_ALL_A = "%Y-%m-%dT%H:%M:%S.%f%Z"
    STRFMT_ISO_SEC_A = "%Y-%m-%dT%H:%M:%S"

    STRFMT_LOGGER_MS_A = "%Y-%m-%d %H:%M:%S.%f"

    _default_time_format = '%Y-%m-%d %H:%M:%S'

    _LOG_FORMAT_106 = '%(asctime)s.%(msecs)03d %(name)s %(threadName)s [%(levelname)s] %(message)s'

    '''
    
    dtstr = datetime.now().strftime("%Y%m%dT%H%M%S")

        
    '''

    @classmethod
    def log_basicConfig(cls, filename=None, loggerName='dkn', level=logging.DEBUG, initInnerLoggerFun=True):
        '''
        这个 dkn logger的设置好像不太好。
        暂时不用这个

        '''

        # AT.unsupported()

        logging.basicConfig(filename=filename, level=level,
                            format=cls._LOG_FORMAT_106,
                            datefmt=AT.STRFMT_ISO_SEC_A,
                            # datefmt=cls._DATE_FORMAT_100,
                            force=True)

        logger = logging.getLogger(loggerName)
        logger.setLevel(level)

        # # create console handler and set level to debug
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)

        # # create formatter
        # formatter = logging.Formatter(
        #     cls._LOG_FORMAT_106)

        # # add formatter to ch
        # ch.setFormatter(formatter)

        # # add ch to logger
        # logger.addHandler(ch)

        mloggerFun = AT.log_loggerFun(loggerName, initInnerLoggerFun)

        return mloggerFun

    @staticmethod
    def assertAllNotNone(*args):
        assert isinstance(args, tuple)
        AT.assert_(all(_ is not None for _ in args),
                   'err7540 some value is None')

    @staticmethod
    def deg_to_rad(d):
        return d/180.0*math.pi

    __beep_last_time = 0

    @staticmethod
    def beep_error_buffered(tone='ping'):
        '''
        在0.5秒内最多播放一次 类似防止按钮双击的效果

        '''
        t = 0.5
        now = AT.fepochSecs()
        if now < AT.__beep_last_time+t:
            return
        else:
            AT.__beep_last_time = now
            AT.beep(tone)

    @staticmethod
    def beep(tone='ping'):
        if False:
            import beepy
            beepy.beep(sound=tone)

    @staticmethod
    def beep2():
        #!wget -q -T 1 http://localhost:333/hello
        print('\7')

    @classmethod
    def mybeep(cls, *, freq=440, dur=500, sleep: float = None, n: int = 1, lastDurRate: float = 1.0):
        if False:
            # 没用用到。只能播放特定wav文件。不适合动态生成信号。
            import beepy
            beepy.beep(sound=tone)

        if True and cls._is_windows:
            # from beep import beep
            import winsound

            freq = int(freq)
            dur = int(dur)

            for i in range(n):
                # beep(freq, dur)  # duration in ms, frequency in Hz
                r = 1.0 if i != n-1 else lastDurRate
                dur2 = int(dur*r)
                winsound.Beep(freq, dur2)
                if sleep is not None:
                    time.sleep(sleep)

        if True and cls._is_linux:
            freq = int(freq)

            for i in range(n):
                # beep -f 2000 -l 1500
                r = 1.0 if i != n-1 else lastDurRate
                dur2 = int(dur*r)
                os.system(f"beep -f {freq} -l {dur2}")
                if sleep is not None:
                    time.sleep(sleep)

    @staticmethod
    def vassert_(b: bool, s: str = None):
        AT.assert_(b, s)

    @classmethod
    def never(cls, s=None):
        AT.assert_(False,  s if s is not None else 'should never come here')

    @classmethod
    def fail(cls, s=None):
        AT.assert_(False,  s if s is not None else 'expected failure err20384')

    @staticmethod
    def checksys():
        assert sys.version_info >= (3, 11)

    @classmethod
    def fepochMillis(cls) -> int:
        millisec = int(AT.fepochSecs() * 1000)
        return millisec

    _last_epochsecs = 0.0

    @classmethod
    def fepochSecs(cls) -> float:
        '''
         time.monotonic()不是epoch值！！F**K
        # return time.monotonic()

        '''
        r = time.time()
        if r <= cls._last_epochsecs:
            return cls._last_epochsecs
        else:
            cls._last_epochsecs = r
            return r

    '''
        # dd/mm/YY H:M:S
    dts = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dts)

    # 20200101T120000
    dts = datetime.now().strftime("%Y%m%dT%H%M%S")
    print("date and time =", dts)
    
    
    '''

    @classmethod
    def sdf_isocompact_format_datetime(cls, dt=None, *, precise: str = 's'):
        """
        20201201T080100
        
        """
        assert precise in ['d', 's', 'ms', 'a'], 'err5554 bad precise'
        
        AT.assert_(dt is None or isinstance(dt,datetime),'err95219')

        # if not isinstance(dt,datetime) and dt is not None:
        #     AT.unsupported()

        if dt is None:
            dt:datetime = AT._now_dt()
            
        dts = dt.strftime(AT.STRFMT_ISO_COMPACT_ALL_A)

        if precise == 'a':
            pass
        elif precise == 'ms':
            dts = dts[:(8+0+1+6+4)]
        elif precise == 's':
            dts = dts[:(8+0+1+6)]
        elif precise == 'd':
            dts = dts[:(8)]
        else:
            AT.never()

        return dts

    @staticmethod
    def sdf_logger():
        AT.unimplemented()
        pass

    @staticmethod
    def _now_dt():
        '''
        这个名称为何用下划线开头?

        '''
        dt = datetime.now()
        return dt

    @classmethod
    def sdf_logger_format_datetime(cls, dt: int = None, *, precise: str = 's', noColon=False) -> str:
        '''
https://strftime.org/    
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
https://man7.org/linux/man-pages/man3/strftime.3.html

-   增加一个参数，可以将冒号转换为-符号 这样的话 生成的结果可以直接用于文件名称中。

2023-12-01T08:30:00.123456

缺省返回
"yyyy-MM-ddTHH:mm:ss"

date -I

d date
s seconds
ms millis
a all

        '''
        assert precise in ['d', 's', 'ms', 'a'], 'err5554 bad precise'

        if dt is not None:
            dt = datetime.fromtimestamp(dt/1000, tz=None)
        else:
            dt = datetime.now()

        dts = dt.strftime(AT.STRFMT_ISO_ALL_A)

        if precise == 'a':
            pass
        elif precise == 'ms':
            dts = dts[:(10+1+8+4)]
        elif precise == 's':
            dts = dts[:(10+1+8)]
        elif precise == 'd':
            dts = dts[:(10)]
        else:
            AT.never()

        if noColon:
            dts = dts.replace(':', '-')

        return dts

    @staticmethod
    def assert_(b: Any, s: str = None):
        # 改成完善的形式

        # assert isinstance(b, bool)

        if b:
            return

        # AT._AstErrorCnt_ += 1 后面的 iprint_error已经记录了错误 此处就不记录了
        msg = _unknown_err if s is None else s

        dknovautils.commons.iprint_error(msg)

        raise DkAstException(msg)

    @staticmethod
    def mychdir(s):
        assert isinstance(s, str) and len(s) > 0
        iprint_debug(f'chdir: {s}')
        os.chdir(s)

    @staticmethod
    def astTrace(b: bool, s: str):
        '''在prod中完全不需要的'''
        AT.assert_(b, s)

    @staticmethod
    def unsupported(s: str = 'feature'):
        AT.assert_(False, f'err8255 unsupported [{s}]')

    @staticmethod
    def unimplemented(s: str = 'feature'):
        AT.assert_(False, f'err4173 unimplemented [{s}]')

    # @staticmethod
    # def f_matploglib_logger():
    #     logger = logging.getLogger('matplotlib.font_manager')
    #     logger.setLevel(level=logging.INFO)

    @staticmethod
    def log_conf_matploglib_logger(level=logging.INFO):
        logger = logging.getLogger('matplotlib.font_manager')
        logger.setLevel(level=level)
        
    @staticmethod
    def dict_group_value(d:Dict)->Dict:
        d2 = {}
        for k,v in d.items():
            if not v in d2:
                d2[v]=[k]
            else:
                d2[v].append(k)
        return d2

    @classmethod
    def bindport_httpserver(cls, *, port) -> bool:
        '''
        如果绑定成功 将启动一个线程 长期占用该端口 并返回 True
        否则返回 False

        '''
        AT.assert_(port > 0, 'err10591 port error')
        PORT = port
        Handler = http.server.SimpleHTTPRequestHandler

        try:
            startOk = True

            def tf():
                nonlocal startOk
                try:
                    with socketserver.TCPServer(("", PORT), Handler) as httpd:
                        iprint_debug(f"serving at port {port}")
                        httpd.serve_forever()
                except:
                    startOk = False

            thread = threading.Thread(target=tf, args=())
            thread.start()

            time.sleep(1.0)
            iprint_debug(f'bind tcp port ok. {port} {startOk}')
            return startOk

        except Exception as e:
            iprint_debug(f'some err here: {e}')
            return False

    # end
    VERSION = DkAppVer


class DkAstException(Exception):
    pass


'''

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='/mnt/d/tmp/demo0726.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)





'''
