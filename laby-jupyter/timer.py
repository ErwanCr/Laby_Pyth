from threading import Timer,Thread,Event


class perpetualTimer():

    def __init__(self,t,hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t,self.handle_function)
        self.isrunning=False

    def handle_function(self):
        #controle du temps depart stop decider combien on attend ou non +s=cancel et restart //regarder si on peu chanegr la valeur dans pyton du timer 
        self.hFunction()
        self.thread = Timer(self.t,self.handle_function)
        self.thread.start()

    def set_fps(self,fps):
        self.t=fps

    def running(self):
        return self.isrunning

    def start(self):
        self.thread.start()
        self.isrunning=True

    def cancel(self):
        self.thread.cancel()
        self.isrunning=False

def printer():
    print ('ipsem lorem')

#t = perpetualTimer(5,printer)
#t.start()