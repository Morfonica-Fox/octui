from textual.app import App
from textual.widgets import Header, Footer, Placeholder, Button, Input

class MyApp(App):
    def compose(self):
        yield Header()
        yield Placeholder(name="body")
        yield Button("Click me", name="button")
        yield Input(name="input")
        yield Footer()
    def on_button_click(self, button: Button):
        if button.label == "Click me":
            self.query_one("#body", Placeholder).update("按钮被点击了！")

if __name__ == "__main__": # 因为octui的目标是对标textual这种现代化UI框架 所以这个是用作参照
    app = MyApp()
    app.run()
