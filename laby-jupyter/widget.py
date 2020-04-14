import ipywidgets as widgets
from ipywidgets import HBox, VBox ,Layout

from laby import *

class labyrinth_text_view(labyrinth_view): 
    
    widget=widgets.HTML(
    value="",
    placeholder='',
    description='',
    )
    def display(self):
        return display(self.widget)
    
    def __init__(self , labyrinth): 
        labyrinth_view.__init__(self,labyrinth) 
        self.update()
    
    def update(self): 
        self.widget.value = "<pre>\n" + self.value.tostring() + "</pre>\n"
    

class labyrinth_SVG_view_monolith (labyrinth_view): 
    widget=widgets.HTML(
    value="",
    placeholder='',
    description='',
    )
    def display(self) :
        return display(self.widget)
    
    def __init__(self,labyrinth) :
        labyrint_view.__init__(labyrinth) 
        self.update()

    def update(self) :
        self.widget.value = self.value.html()
    





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
        slider.observe()
        widgets.HBox([fast_backward,backward,step_backward,pause,step_forward,play,fast_forward,slider])
    def display(self):
        return display(self.widget)


class laby_SVG_view_player_app(labyrinth_SVG_view_monolith):
    def __init__(self,labyrinth): 
        labyrinth_SVG_view_monolith.__init__(self,labyrinth) ## super remplace le nom de l'héritage mais ici trop long 
        self.controls = player_view(player(labyrinth))
        self.widget=VBox([self.view.widget,self.controls.widget])
    def display(self):
        self.player.run() #// Or should this be already be done in e.g. PlayerView
        return display(self.widget)
    


def laby_bar(s):
    app = laby_SVG_view_player_app(labyrinth(s))
    app.player.run()
    app.display()
    return app

#level = string du level
def laby_level(level) :
    laby=labyrinth(level)
    app = laby_SVG_view_player_app(laby)
    app.player.run()
    app.display()
    return app
