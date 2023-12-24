from error import ProgressBarError
import time
from datetime import datetime
"""Class __ProgressBar_class That is not yet complete,
 but it can be used and we will quickly develop it to be perfect."""
class __ProgressBar:
    def __init__(self):
        self.__start = "[current_step/total_steps]"
        self.__current_step = 0

    def length_bar(self, n):
        self.__length = n

    def bar_character(self, n):
        self.__bar_character = n

    def empty_character(self, n):
        self.__empty_character = n

    def set_start(self, n="[current_step/total_steps]", y=':', start='[', end=']'):
        """set: [current_step/total_steps]
            time: year, month, day, hour, minute,second, microsecond, all
            example:  
            ProgressBar.set_start("all")
            for i in ProgressBar.generate(range(20000)):
                ProgressBar.Progress_print(i ** 2)"""
        self.__start = [n, [y, start, end]]
    
    def __n(self):
        starts = {"[current_step/total_steps]":"["+str(self.__current_step)+"/"+str(self.__total_steps)+"]",
                  "time": {"year": datetime.now().year, "month":datetime.now().month,"day": datetime.now().day,"hour": datetime.now().hour,"minute": datetime.now().minute,"second": datetime.now().second,"microsecond": datetime.now().microsecond,"all": datetime.now().strftime("%Y-%m-%d %H:%M:%S")+':'+str(datetime.now().microsecond)}  # แปลงเป็น string ในรูปแบบที่กำหนด}
        }   
        
        try:
            return str(str(self.__start[1][2]) + str(starts[self.__start[0]]) + str(self.__start[1][3]))
        except (KeyError, TypeError):
            if isinstance(self.__start[0], tuple) or isinstance(self.__start[0], list):
                n =''
                m = 0
                for i in self.__start[0]:
                    print(starts["time"][str(i)])
                    s = '' if m - (len(self.__start[0]) -1) == 0 else str(self.__start[1][0])
                    n += str(starts["time"][str(i)]) + s
                    m += 1
                return str(str(self.__start[1][1]) + n + str(self.__start[1][2]))
            else:
                return str(str(self.__start[1][1]) + str(starts["time"][self.__start[0]]) + str(self.__start[1][2]))
        except KeyError:
            return self.__start[0]

    def generate(self, iterable, length=50, bar_character="#", empty_character="-"):
        self.__bar_character = bar_character
        self.__empty_character = empty_character
        self.__length = length
        self.__total_steps = len(iterable) - 1
        for value in iterable:
            
            self.__progress_percentage = (self.__current_step / self.__total_steps) * 100
            self.__progress_bar_length = int((self.__current_step / self.__total_steps) * self.__length)
            self.__bar = self.__bar_character * self.__progress_bar_length + self.__empty_character * (self.__length - self.__progress_bar_length)
            self.__current_step += 1
            self.start = self.__n()
            print(f"\r {self.start} [{self.__bar}] {self.__progress_percentage:.2f}%", end='', flush=True)
            yield value
            
    def Progress_print(self, value):
        print(f"\r {self.start} [{self.__bar}] {self.__progress_percentage:.2f}%  value: {value}", end='',flush=True)

    def sleep(self, n:float):
        time.sleep(n)
ProgressBar = __ProgressBar()
"""Because of class __ProgressBar_func It is not yet finished due to various problems.
We are accelerating development Please be patient and wait."""

# class __ProgressBar_func:
#     def __init__(self) -> None:
#         self.__length = 50
#         self.__bar_character = '#'
#         self.__empty_character = '-'
#         self.__current_step = 1
#         self.__total_steps:int = 0
#         self.__start ="[current_step/total_steps]"
#         self.__name = 'ProgressBar_func'
#     def __iter__(self):
#         return self

#     def length_bar(self, n):
#         self.__length = n

#     def bar_character(self, n):
#         self.__bar_character = n

#     def empty_character(self, n):
#         self.__empty_character = n

#     def set_start(self, n):
#         self.__start = n

#     def _f(self):
#         self.__progress_percentage = (self.__current_step / self.__total_steps) * 100
#         self.__progress_bar_length = int((self.__current_step / self.__total_steps) * self.__length)
#         self.__bar = self.__bar_character * self.__progress_bar_length + self.__empty_character * (self.__length - self.__progress_bar_length)

#     def name(self, name:str) -> None:
#         self.__name = name

#     def __n(self):
#         starts = {"[current_step/total_steps]":"["+str(self.__current_step)+"/"+str(self.__total_steps)+"]"}
#         try:
#             self.start = starts[self.__start]
#         except KeyError:
#             self.start = self.__start
#     def run(self, func=None, value: bool = False):  
#         text = inspect.getsource(func)
        
#         print(text)
#         self.__total_steps += text.count(f"{self.__name}.run(") - text.count(f"#{self.__name}.run(")
#         print([self.__total_steps, text.count(f"{self.__name}.run("), text.count(f"#{self.__name}.run(")])
        
#         self._f()
#         self.__n()

#         if self.__current_step > self.__total_steps:
#             raise ProgressBarError(f'{self.__total_steps}, {self.__current_step}')
        
#         print(func)
#         print(f"\r{self.start}[{self.__bar}] {self.__progress_percentage:.2f}% {'value: '+ str(func) if value else ''}", end='', flush=True)
#         self.__current_step += 1
#         return func
    
#     def set_bar_loop(self, f):
#         self.__total_steps += len(f) - 2
#         return f

#     def Progress_print(self, value):
#         print(f"\r{self.start}[{self.__bar}] {self.__progress_percentage:.2f}%  value: {value}", end='', flush=True)
        
# ProgressBar_func = __ProgressBar_func()
