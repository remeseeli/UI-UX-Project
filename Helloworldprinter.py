#Imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

#This was made with help of AI

# KV string for additional styling and layout
KV = '''
<TaskManagerScreen>:
    BoxLayout:
        orientation: 'vertical'

        # App bar with night mode toggle
        MDTopAppBar:
            title: "75%"
            elevation: 4
            left_action_items: []
            right_action_items: [["weather-night", lambda x: app.toggle_theme()]]

        # Slim progress bar under the app bar
        MDBoxLayout:
            size_hint_y: None
            height: dp(4)
            MDProgressBar:
                id: progress_bar
                value: 40
                color: 1, 1, 1, 1  # white bar for contrast
                type: "determinate"

        # Main content area
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(16)
            spacing: dp(8)
            md_bg_color: 0.9, 1, 0.9, 1

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
'''

class TaskManagerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_sample_tasks()
    
    def add_sample_tasks(self):
        sample_tasks = [
            {"title": "Workout", "description": "10:00", "icon": "weight-lifter"},
            {"title": "Grocery Shopping", "description": "14:00", "icon": "cart"},
            {"title": "Hanging out", "description": "18:00", "icon": "account-group"},
            {"title": "Call Mom", "description": "20:00", "icon": "phone"}
        ]
        
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
    
    def toggle_task_status(self, instance):
        if instance.icon == "checkbox-blank-circle-outline":
            instance.icon = "checkbox-marked-circle"
        else:
            instance.icon = "checkbox-blank-circle-outline"
    
    def show_task_dialog(self):
        self.dialog = MDDialog(
            title="Add New Task",
            type="custom",
            content_cls=TaskDialogContent(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="ADD",
                    on_release=self.add_task
                ),
            ],
        )
        self.dialog.open()
    
    def close_dialog(self, instance):
        self.dialog.dismiss()
    
    def add_task(self, instance):
        content = self.dialog.content_cls
        title = content.ids.title.text
        description = content.ids.description.text
        
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
            
        self.close_dialog(None)


class TaskDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(15)
        self.size_hint_y = None
        self.height = dp(120)
        
        self.title = MDTextField(
            hint_text="Task title",
            required=True,
        )
        self.title.id = "title"
        
        self.description = MDTextField(
            hint_text="Description",
        )
        self.description.id = "description"
        
        self.add_widget(self.title)
        self.add_widget(self.description)


class TaskManagerApp(MDApp):
    def build(self):
        Builder.load_string(KV)
        Window.size = (360, 640)  # Mobile-like dimensions
        self.theme_cls.primary_palette = "Green"
        
        screen = TaskManagerScreen(name="task_manager")
        
        # Add floating action button for adding new tasks
        fab = MDFloatingActionButton(
            icon="plus",
            pos_hint={"right": 0.95, "bottom": 0.05},
            on_release=lambda x: screen.show_task_dialog()
        )
        screen.add_widget(fab)
        
        return screen


if __name__ == "__main__":
    TaskManagerApp().run()
