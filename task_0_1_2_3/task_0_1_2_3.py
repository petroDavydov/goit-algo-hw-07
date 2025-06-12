import os
import json
import networkx as nx
import matplotlib.pyplot as plt
from colorama import Fore, Style, init
init(autoreset=True)


DATA_PATH = "task_0_1_2_3.json"

if os.path.exists(DATA_PATH):
    with open(DATA_PATH, "r") as f:
        servers = json.load(f)
else:
    servers = [
        "Server1_boss", "Server2_financial", "Server3_secretary", "Server4_developer",
        "Server5_designer", "Server6_manager", "Server7_employees_only",
        "Server8_free_for_all_1", "Server9_free_for_all_2", "Server10_firewall",
        "Server11_backup", "Server12_maintenance"
    ]


def save_servers_to_file():
    with open(DATA_PATH, "w") as f:
        json.dump(servers, f, indent=4)

# ----------------------------------------------------
# Створення ServerNode


class ServerNode:
    def __init__(self, key, name):
        self.key = key
        self.name = name
        self.height = 1
        self.left = None
        self.right = None


# use hint

def extract_id(server_name):
    return int(server_name.split("_")[0].replace("Server", ""))


def get_height(node):
    if not node:
        return 0
    return node.height


def get_balance(node):
    if not node:
        return 0
    return get_height(node.left) - get_height(node.right)


def left_rotate(z):
    y = z.right
    z.right = y.left
    y.left = z
    z.height = 1 + max(get_height(z.left), get_height(z.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def right_rotate(y):
    x = y.left
    T3 = x.right
    x.right = y
    y.left = T3
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))

    return x


# use friends knowelage(about add 'name')

def insert(root, key, name):
    if not root:
        return ServerNode(key, name)
    if key < root.key:
        root.left = insert(root.left, key, name)
    elif key > root.key:
        root.right = insert(root.right, key, name)
    else:
        return root  # no duplicates
    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)
    if balance > 1:
        if key < root.left.key:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)
    if balance < -1:
        if key > root.right.key:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)
    return root


# delete

def delete_node(root, key):
    if not root:
        return root

    if key < root.key:
        root.left = delete_node(root.left, key)
    elif key > root.key:
        root.right = delete_node(root.right, key)
    else:
        if root.left is None:
            temp = root.right
            root = None
            return temp
        elif root.right is None:
            temp = root.left
            root = None
            return temp

        temp = find_min_server_node(root.right)
        root.key = temp.key
        root.right = delete_node(root.right, temp.key)

    if root is None:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))

    balance = get_balance(root)

    if balance > 1:
        if get_balance(root.left) >= 0:
            return right_rotate(root)
        else:
            root.left = left_rotate(root.left)
            return right_rotate(root)

    if balance < -1:
        if get_balance(root.right) <= 0:
            return left_rotate(root)
        else:
            root.right = right_rotate(root.right)
            return left_rotate(root)

    return root


# --------------------
# use google and github


def find_max_server_node(node):
    current = node
    while current and current.right:
        current = current.right
    return current


def find_min_server_node(node):
    current = node
    while current and current.left:
        current = current.left
    return current


def find_sum_server_node(node):
    sum_srv = 0
    sum_srv_left = 0
    sum_srv_right = 0
    current = node
    if current:
        sum_srv_left = find_sum_server_node(current.left)
        sum_srv_right = find_sum_server_node(current.right)
        sum_srv = sum_srv + sum_srv_left + sum_srv_right + current.key
        return sum_srv
    else:
        sum_srv = sum_srv_left+sum_srv_right
        return sum_srv


# # Які сервери існують
# servers = [
#     "Server1_boss", "Server2_financial", "Server3_secretary", "Server4_developer",
#     "Server5_designer", "Server6_manager", "Server7_employees_only",
#     "Server8_free_for_all_1", "Server9_free_for_all_2", "Server10_firewall",
#     "Server11_backup", "Server12_maintenance"
# ]


# Будуємо дерево
root = None
for server in servers:
    root = insert(root, extract_id(server), server)


# --------------------------------

print(f"{Fore.WHITE}Поточні сервери:{Style.RESET_ALL}")
for s in servers:
    print("-", s)

print(f"\n{Fore.YELLOW}Що хочеш зробити з деревом серверів?{Style.RESET_ALL}")
print("1 — Додати новий сервер")
print("0 — Видалити сервер")
print("3 — Пропустити дію")

choice = input("Введи код дії: ")

if choice == "1":
    new_server = input(
        "Введи назву нового сервера (наприклад, Server13_logs): ")
    if new_server:
        new_key = extract_id(new_server)
        root = insert(root, new_key, new_server)
        servers.append(new_server)
        save_servers_to_file()
        print(f"{Fore.GREEN}Сервер додано: {new_server}{Style.RESET_ALL}")

elif choice == "0":
    del_server = input(
        "Введи назву сервера, який видалити (наприклад, Server5_designer): ")
    if del_server:
        del_key = extract_id(del_server)
        root = delete_node(root, del_key)
        servers.remove(del_server)
        save_servers_to_file()
        print(f"{Fore.RED}Сервер видалено: {del_server}{Style.RESET_ALL}")

elif choice == "3":
    print("Ви skip-нули! Дерево залишилось без змін.")

else:
    print(f"{Fore.RED}Невідома команда.{Style.RESET_ALL}")


# -----------------------------------

def draw_tree(node, graph, parent=None):
    if node is None:
        return

    graph.add_node(node.name)

    if parent:
        graph.add_edge(parent, node.name)

    draw_tree(node.left, graph, node.name)
    draw_tree(node.right, graph, node.name)


G = nx.DiGraph()
draw_tree(root, G)


def hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = {}

    def recurse(node, x, y, dx):
        pos[node] = (x, y)
        children = list(G.successors(node))
        if len(children) == 2:
            recurse(children[0], x - dx, y - vert_gap, dx / 2)
            recurse(children[1], x + dx, y - vert_gap, dx / 2)
        elif len(children) == 1:
            recurse(children[0], x, y - vert_gap, dx / 2)

    recurse(root, xcenter, vert_loc, width / 2)
    return pos


if root:
    pos = hierarchy_pos(G, root.name)  # 👈 Розташування (див. нижче)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=1200,
            node_color="lightgreen", font_size=10)
    plt.title("AVL-дерево серверів", fontsize=14)
    plt.axis("off")
    plt.show()


# -------------------------------------


sum_node = find_sum_server_node(root)
min_node = find_min_server_node(root)
max_node = find_max_server_node(root)

if root:
    print(f"{Fore.BLUE}Числова сума всіх серверів: --> {Fore.LIGHTRED_EX}{sum_node}{Style.RESET_ALL}")

    if min_node:
        print(f"{Fore.BLUE}Сервер з найменшим ID: --> {Fore.LIGHTYELLOW_EX}{min_node.name}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}Мінімальний сервер не знайдено.")

    if max_node:
        print(
            f"{Fore.BLUE}Сервер з найбільшим ID: -->{Fore.GREEN} {max_node.name}{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTRED_EX}Максимальний сервер не знайдено.{Style.RESET_ALL}")
else:
    print(f"{Fore.LIGHTRED_EX}Дерево серверів порожнє.{Style.RESET_ALL}")
