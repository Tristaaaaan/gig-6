# main.py
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database file
DATABASE_FILE = "tasks.db"

# Create an SQLite database engine
engine = create_engine(f"sqlite:///{DATABASE_FILE}", echo=True)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the Task model


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String(100), nullable=False)


# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()


class FirstWindow(Screen):
    Builder.load_file('firstwindow.kv')

    def add_task(self):
        task_name = self.ids.task_input.text.strip()
        if task_name:
            task = Task(task_name=task_name)
            session.add(task)
            session.commit()
            self.ids.task_input.text = ""
            self.update_task_list()

    def update_task_list(self):
        task_list = self.ids.task_list
        task_list.clear_widgets()

        tasks = session.query(Task).all()
        for task in tasks:
            task_widget = MDTextField(text=task.task_name, readonly=True)
            task_list.add_widget(task_widget)


class WindowManager(ScreenManager):
    pass


class RawApp(MDApp):

    def build(self):
        return WindowManager()


if __name__ == '__main__':
    RawApp().run()
