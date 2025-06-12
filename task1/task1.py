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

# use google and github


def find_max_server_node(node):
    current = node
    while current and current.right:
        current = current.right
    return current


# Які сервери існують
servers = [
    "Server1_boss", "Server2_financial", "Server3_secretary", "Server4_developer",
    "Server5_designer", "Server6_manager", "Server7_employees_only",
    "Server8_free_for_all_1", "Server9_free_for_all_2", "Server10_firewall",
    "Server11_backup", "Server12_maintenance"
]

# Будуємо дерево
root = None
for server in servers:
    root = insert(root, extract_id(server), server)

# Виводимо сервер з найбільшим значенням
max_node = find_max_server_node(root)
if max_node:
    print("Сервер з найбільшим ID:", max_node.name)
