#Imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.button import MDFloatingActionButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder

#This src was made with help of ChatGPT
#All design elements/choices were made by our group
#Versio 1.0.0

#KV file to define the UI
KV = '''
<TaskManagerScreen>:
    BoxLayout:
        orientation: 'vertical'

        #Top bar with night mode toggle
        MDTopAppBar:
            id: top_bar
            title: "15.4.2025"
            elevation: 4
            left_action_items: []
            right_action_items: [["weather-night", lambda x: app.toggle_theme()]]

        #Progress bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(4)
            padding: 0
            spacing: 0

            MDProgressBar:
                id: progress_bar
                value: 0 
                color: 0.949, 0.227, 0.227, 1
                type: "determinate"
                size_hint_x: 1
                size_hint_y: None
                height: dp(4)

        #Everything else
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(8)

            MDLabel:
                text: "Today's Tasks"
                font_style: "H5"
                size_hint_y: None
                height: self.texture_size[1]

            ScrollView:
                do_scroll_x: False
                MDList:
                    id: task_list
                    padding: 0

        #Floating Add Button
        MDFloatingActionButton:
            icon: "plus"
            md_bg_color: app.theme_cls.primary_color
            pos_hint: {"center_x": 0.5}
            elevation_normal: 8
            on_release: root.show_task_menu()

        #Bottom Icon Bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(72)
            padding: dp(24), dp(12)
            spacing: dp(48)
            pos_hint: {"center_x": 0.5}
            md_bg_color: 0.95, 0.95, 0.95, 1
            halign: "center"

            Widget:  # Spacer for left alignment

            MDIconButton:
                icon: "home"
                icon_size: "36sp"
                theme_icon_color: "Custom"
                icon_color: 0.3, 0.3, 0.3, 1

            MDIconButton:
                icon: "calendar"
                icon_size: "36sp"
                theme_icon_color: "Custom"
                icon_color: 0.3, 0.3, 0.3, 1

            MDIconButton:
                icon: "cog"
                icon_size: "36sp"
                theme_icon_color: "Custom"
                icon_color: 0.3, 0.3, 0.3, 1

            Widget: 
'''

class TaskManagerScreen(MDScreen):
    total_tasks = 0
    completed_tasks = 0 
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_sample_tasks()

    #Function to add sample task
    def add_sample_tasks(self):
        sample_tasks = [
            {"title": "Workout", "description": "10:00", "icon": "weight-lifter"},
            {"title": "Homework", "description": "15:00", "icon": "clipboard-text"},
            {"title": "Grocery Shopping", "description": "18:00", "icon": "cart"},
            {"title": "Hangout", "description": "20:00", "icon": "account-group"},
        ]

        self.total_tasks = len(sample_tasks) 
        for task in sample_tasks:
            item = TwoLineAvatarIconListItem(
                text=task["title"],
                secondary_text=task["description"],
            )
            item.add_widget(IconLeftWidget(icon=task["icon"]))
            item.add_widget(IconRightWidget(
                icon="checkbox-blank-circle-outline",
                on_release=self.toggle_task_status
            ))
            self.ids.task_list.add_widget(item)

    #Function to toggle task status
    def toggle_task_status(self, instance):
        if instance.icon == "checkbox-blank-circle-outline":
            instance.icon = "checkbox-marked-circle"
            self.completed_tasks += 1 
        else:
            instance.icon = "checkbox-blank-circle-outline"
            self.completed_tasks -= 1 
        self.update_progress_bar()

    #Function to update progressbar
    def update_progress_bar(self):
        if self.total_tasks > 0:
            progress = (self.completed_tasks / self.total_tasks) * 100  
            self.ids.progress_bar.value = progress  

    #Function to open the task menu
    def show_task_menu(self):
        self.dialog = MDDialog(
            title="Add New Task",
            type="custom",
            content_cls=TaskMenuContent(),
            buttons=[ 
                MDFlatButton(text="CANCEL", on_release=self.close_menu),
                MDFlatButton(text="ADD", on_release=self.add_task),
            ],
        )
        self.dialog.open()

    #Function to close the task menu
    def close_menu(self, instance):
        self.dialog.dismiss()

    #Function to add task
    def add_task(self, instance):
        content = self.dialog.content_cls
        title = content.title_field.text
        description = content.description_field.text

        if title.strip():
            item = TwoLineAvatarIconListItem(
                text=title,
                secondary_text=description,
            )
            item.add_widget(IconLeftWidget(icon="clipboard-text"))
            item.add_widget(IconRightWidget(
                icon="checkbox-blank-circle-outline",
                on_release=self.toggle_task_status
            ))
            self.ids.task_list.add_widget(item)

            self.total_tasks += 1
            self.update_progress_bar()

        self.close_menu(None)

#Class for task menu content
class TaskMenuContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(15)
        self.size_hint_y = None
        self.height = dp(120)

        self.title_field = MDTextField(hint_text="Task title", required=True)
        self.description_field = MDTextField(hint_text="Description")

        self.add_widget(self.title_field)
        self.add_widget(self.description_field)

#Class to define the theme etc
class TaskManagerApp(MDApp):
    def build(self):
        Builder.load_string(KV)
        Window.size = (360, 640) 

        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.theme_style = "Light"

        screen = TaskManagerScreen(name="task_manager")

        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            on_release=lambda x: screen.show_task_menu(),
        )


        return screen

    #Function to toggle between light and dark
    def toggle_theme(self):
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.theme_style = "Dark"
            self.update_theme_icon("weather-sunny") 
        else:
            self.theme_cls.theme_style = "Light"
            self.update_theme_icon("weather-night")

    #Function to update theme logo
    def update_theme_icon(self, icon_name):
        top_bar = self.root.ids.top_bar
        top_bar.right_action_items = [[icon_name, lambda x: self.toggle_theme()]] 

if __name__ == "__main__":
    TaskManagerApp().run()
