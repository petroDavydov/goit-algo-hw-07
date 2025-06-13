# Comment
from colorama import Fore, Style, init
init(autoreset=True)


class Comment:
    def __init__(self, text, author) -> str:
        self.text = text
        self.author = author
        self.replies = []
        self.is_delete = False

    def add_reply(self, comment_with_reply):
        self.replies.append(comment_with_reply)

    def remove_replay(self):
        self.text = "Remove comment"
        self.is_delete = True

    def show_on_display(self, indent=0):
        prefix = " " * indent
        if self.is_delete:
            print(f"{Fore.RED}{prefix}{self.text}{Style.RESET_ALL}")
        else:
            print(f"{Fore.LIGHTBLUE_EX}{prefix}{self.author}: {self.text}")

        for reply in self.replies:
            reply.show_on_display(indent + 4)


root_comment = Comment("Яка чудова книга!", "Бодя")
reply1 = Comment("Книга повне розчарування :(", "Андрій")
reply2 = Comment("Що в ній чудового?", "Марина")

root_comment.add_reply(reply1)
root_comment.add_reply(reply2)

reply1_1 = Comment("Не книжка, а перевели купу паперу ні нащо...", "Сергій")
reply1.add_reply(reply1_1)

reply1.remove_replay()

root_comment.show_on_display()
