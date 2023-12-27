import subprocess
import sys
from typing import List, Tuple
from dknovautils.dk_imports import *

# 导入module避免某些循环import的问题
from dknovautils import commons, iprint_debug, iprint_warn,AT


class DKProcessUtil(object):
    
    _cmdid=1000

    # 这个例子说明 call() 函数具有不可替代的价值。
    @staticmethod
    def run_simple_a(cmd):
        cmdid = DKProcessUtil._cmdid
        DKProcessUtil._cmdid +=1
                
        iprint_debug(f"run_simple_a {cmdid} "+cmd)
        try:
            retcode = subprocess.call(cmd, shell=True)
            if retcode < 0:
                print("Child was terminated by signal", -retcode, file=sys.stderr)
            else:
                print("Child returned", retcode, file=sys.stderr)
        except OSError as e:
            iprint_warn(f"run_simple_a {cmdid} Execution failed:", e, file=sys.stderr)


    @staticmethod
    def run_simple_b(cmd: str,*, splitLines=False, _debug=False) -> Tuple[int, List,List]:
        # Tuple[int, str|List,str|List]
        cmdid = DKProcessUtil._cmdid
        DKProcessUtil._cmdid +=1
        
        if _debug:
            print(f'run_simple_b start {cmdid}')

        # Use shell to execute the command, store the stdout and stderr in sp variable
        # 运行中，会缓存结果，直到执行完成才会输出。
        sp = subprocess.Popen(cmd,
                            shell=True,
                            universal_newlines=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

        # Store the return code in rc variable
        # 这个rc值如何获取？如果打开这一行，将在某些情况下产生死锁问题。
        # 来自文档中的说明: This will deadlock when using stdout=PIPE or stderr=PIPE and the child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use Popen.communicate() when using pipes to avoid that.    
        # rc = sp.wait()

        # Separate the output and error by communicating with sp variable.
        # This is similar to Tuple where we store two values to two different variables
        out, err = sp.communicate()
        rc = sp.returncode

        if _debug:
            print('Return Code:', rc, '\n')
            print('stdout is: \n', out)
            if rc !=0:
                print('stderr is: \n', err)

        if out is None:
            out = ''
        if err is None:
            err = ''

        if splitLines:
            out = out.splitlines()
            err = err.splitlines()
            
        if _debug:
            print(f'run_simple_b end {cmdid}')            

        return (rc,out, err)
    
    

run_simple_a = DKProcessUtil.run_simple_a
run_simple_b = DKProcessUtil.run_simple_b


"""

run_simple_a = dknovautils.dkprocess.DKProcessUtil.run_simple_a

for i in range(20):
    cmd=f''
    run_simple_a(cmd)




"""