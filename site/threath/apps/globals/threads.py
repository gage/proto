import threading, Queue

class GeneralThread(threading.Thread):
    # While thread_num = 0, it stands that there is no thread 
    MAX_NUM = 1
    thread_num = 0    
    Pool = Queue.Queue( 0 )
        
    @classmethod
    def single_start(cls):
        if cls.thread_num < cls.MAX_NUM:
            cls.thread_num += 1
            cls().start()
        else:
            pass
    
    @classmethod
    def put(cls, obj):
        # Put object into pool
        cls.Pool.put(obj)
        # Do single start if there is no thread running
        cls.single_start()        
                
    def run(self):
        # Function run should be implemented by each thread.
        while True:          
            _ = self.Pool.get()
            self.Pool.task_done()
