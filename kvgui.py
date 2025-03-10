import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# Virtual environment Python path
VENV_PYTHON = r"d:/prjct code/Tink-Her-hack-3.0/venv/Scripts/python.exe"

class ChessAIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        
        label = Label(text="Chess AI Menu", font_size=24, bold=True)
        layout.add_widget(label)
        
        btn_start = Button(text="Start Game", font_size=18, size_hint=(1, 0.2), background_color=(0.2, 0.6, 0.9, 1))
        btn_start.bind(on_press=self.run_custom_game)
        layout.add_widget(btn_start)
        
        btn_setup = Button(text="Setup (Train Model)", font_size=18, size_hint=(1, 0.2), background_color=(0.1, 0.7, 0.3, 1))
        btn_setup.bind(on_press=self.run_training)
        layout.add_widget(btn_setup)
        
        btn_quit = Button(text="Quit", font_size=18, size_hint=(1, 0.2), background_color=(0.9, 0.2, 0.2, 1))
        btn_quit.bind(on_press=self.quit_app)
        layout.add_widget(btn_quit)
        
        return layout
    
    def run_custom_game(self, instance):
        self.show_popup("Starting Game", "The chess game will now start.")
        subprocess.run([VENV_PYTHON, "custom_game.py"])
        self.show_popup("Training Model", "Game finished! Training the model now...")
        subprocess.run([VENV_PYTHON, "train_custom.py"])
    
    def run_training(self, instance):
        self.show_popup("Training Model", "Training the model now...")
        subprocess.run([VENV_PYTHON, "train_custom.py"])
    
    def quit_app(self, instance):
        App.get_running_app().stop()
    
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, font_size=16)
        btn_close = Button(text="OK", size_hint=(1, 0.3))
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(btn_close)
        
        popup = Popup(title=title, content=popup_layout, size_hint=(0.6, 0.4))
        btn_close.bind(on_press=popup.dismiss)
        
        popup.open()

if __name__ == "__main__":
    ChessAIApp().run()
