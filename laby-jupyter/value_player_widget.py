from enum import Enum
import ipywidgets
from functools import partial 
from ipywidgets import HBox, VBox ,Layout
PlayDirection = Enum('PlayDirection','Forward Backward None')
from threading import *
class player(VBox) :
    
        
       

        def run(self):
            self.timer.run()
        
        def update(self):
            self.value = self.history[self.time]
            self.view.update()
        def get_value(self):
            
            return self.history[len(self.history)-1]
        
        def set_value(self,value): ## = player.value=data
            if (len(self.history) > 10000):
                raise RunTimeError("Votre programme a pris plus de 1000 étapes")
                
            self.history.append(value)
            if ( not self.timer.running() and self.time == len(self.history) -2):
                self.time=self.time+1
                self.update()
        def tick(self):
            if(self.play_direction == PlayDirection.Forward ):  
                self.step_forward()
            else:
                self.step_backward()
        
        def reset(self,value):      
                self.time=0
                self.history=[value]
                self.update()
        
        def begin(self):
            self.time=0
            self.update()
        
        def end(self):
            self.time= len(self.history)-1  
            self.update()
        def step_backward(self):
            if( self.time >0):
                self.time=self.time-1
                self.update()
        def step_forward(self):
            if( self.time <len(self.history)-1):  
                self.time=self.time+1
                self.update()        
        def backward (self):
            self.play_direction = PlayDirection.Backward # a check
            self.timer.set_fps(self.play_fps)
        
        def play(self):
            self. play_direction = PlayDirection.Forward # a check
            self.timer.set_fps(self.play_fps)
        
        def pause(self):
            self.play_direction=None
            self.timer.set_fps(0)
        
        def set_fps(self,fps):
            self.play_fps=fps
            if(self.play_direction != None):
                self.timer.set_fps(fps)
        
        def won(self):
            return self.history[len(self.history)-1].won()

        def __init__(self, _view):
            self.view = _view
            self.original_value=self.view.value
            self.play_direction=PlayDirection.Forward
            self.play_fps=1
            self.reset(self.original_value)
            self.timer =Timer ( partial( self.tick ), self.play_fps)
            self.history=[]

class player_view:
    def __init__(self,player):
        widget=widgets.HTML(
        value="",
        placeholder='',
        description='',
        )
        output = widgets.Output()

        def fast_backward_clicked(b):
            with output:
                player.begin()
                player.pause()
            
        def backward_clicked(b):
            with output:
                player.backward()
        def step_backward_clicked(b):
            with output: 
                player.pause()
                player.step_backward()
        def pause_clicked(b):
            with output:
                player.pause()
        def step_forward_clicked(b):
            with output:
                player.pause()
                player.step_forward()

        def play_clicked(b):
            with output:
                player.play()
        def fast_forward_clicked(b):
            with output:
                player.pause()
                player.end()
                            

        slider=widgets.FloatSlider(
        value=1.0,
        min=0.0,
        max=5.0,
        step=1,
            description="Speed:"
        )

        def on_value_change(change,player):
            fps=1
            value=int (change['new'])
            for i in range (0,value):
                fps=fps*2
            player.set_fps(fps)
        
        slider.observe(on_value_change, names='value')

        play= widgets.Button(description="",icon='fa-play',layout=Layout(width='25px'))
        fast_backward= widgets.Button(description="",icon='fa-fast-backward',layout=Layout(width='35px'))
        backward= widgets.Button(description="",icon='fa-backward',layout=Layout(width='35px'))
        step_backward= widgets.Button(description="",icon='fa-step-backward',layout=Layout(width='35px'))
        pause= widgets.Button(description="",icon='fa-pause',layout=Layout(width='35px'))
        step_forward= widgets.Button(description="",icon='fa-step-forward',layout=Layout(width='35px'))
        fast_forward= widgets.Button(description="",icon='fa-fast-forward',layout=Layout(width='35px'))

        play.on_click(play_clicked)
        fast_backward.on_click(fast_backward_clicked)
        backward.on_click(backward_clicked)
        step_backward.on_click(step_backward_clicked)
        pause.on_click(pause_clicked)
        step_forward.on_click(step_forward_clicked)
        fast_forward.on_click(fast_forward_clicked)

        widgets.HBox([fast_backward,backward,step_backward,pause,step_forward,play,fast_forward,slider])
    def display(self):
        return display(self.widget)