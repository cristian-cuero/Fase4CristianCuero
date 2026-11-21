import tkinter as tk
from tkinter import messagebox
from datetime import datetime


_MISSING = object()


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self, max_levels=4):
        self.root = None
        self.max_levels = max_levels

    def get_height(self, node=_MISSING):
        if node is _MISSING:
            node = self.root
        if node is None:
            return 0
        return 1 + max(self.get_height(node.left), self.get_height(node.right))

    def count_nodes(self, node=_MISSING):
        if node is _MISSING:
            node = self.root
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    def insert(self, value):
        if self.root is None:
            self.root = BSTNode(value)
            return True, "Node added successfully."

        current = self.root
        level = 1

        while current is not None:
            if value == current.value:
                return False, f"Node {value} already exists in the tree."

            if level >= self.max_levels:
                return (
                    False,
                    f"Cannot insert node {value}.\n"
                    f"This tree is limited to {self.max_levels} levels.\n"
                    f"Adding this node would exceed the maximum depth.\n"
                    f"Clear the tree or choose a different value."
                )

            if value < current.value:
                if current.left is None:
                    current.left = BSTNode(value)
                    return True, f"Node {value} added successfully."
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(value)
                    return True, f"Node {value} added successfully."
                current = current.right

            level += 1

        return False, "Unable to insert node."

    def search(self, value):
        path = []
        current = self.root
        while current is not None:
            path.append(current.value)
            if value == current.value:
                return True, path
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False, path

    def preorder_traversal(self):
        result = []
        self._preorder(self.root, result)
        return result

    def _preorder(self, node, result):
        if node is not None:
            result.append(node.value)
            self._preorder(node.left, result)
            self._preorder(node.right, result)

    def inorder_traversal(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is not None:
            self._inorder(node.left, result)
            result.append(node.value)
            self._inorder(node.right, result)

    def postorder_traversal(self):
        result = []
        self._postorder(self.root, result)
        return result

    def _postorder(self, node, result):
        if node is not None:
            self._postorder(node.left, result)
            self._postorder(node.right, result)
            result.append(node.value)

    def clear(self):
        self.root = None


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Fase4CristianCuero — Login")
        self.root.geometry("540x620")
        self.root.config(bg="#091622")
        self.root.resizable(False, False)

        self.build_ui()

    def build_ui(self):
        title_label = tk.Label(
            self.root,
            text="🌲  BST Explorer",
            font=("Segoe UI", 24, "bold"),
            fg="#00b4d8",
            bg="#091622"
        )
        title_label.pack(pady=(25, 2))

        subtitle_label = tk.Label(
            self.root,
            text="Binary Search Tree — Phase 4",
            font=("Segoe UI", 11),
            fg="#94a3b8",
            bg="#091622"
        )
        subtitle_label.pack(pady=(0, 18))

        # Info Box
        info_frame = tk.Frame(self.root, bg="#0f2436", bd=1, relief="solid", highlightbackground="#00b4d8", highlightthickness=1)
        info_frame.pack(padx=40, pady=10, fill="x")

        current_date = datetime.now().strftime("%B %d, %Y")
        info_lines = [
            ("Application:", "Fase4CristianCuero"),
            ("Student:", "Cristian Stiven Cuero Caicedo"),
            ("Group:", "301305_155"),
            ("Course:", "Data Structures · 301305"),
            ("Date:", current_date),
        ]

        for idx, (label, val) in enumerate(info_lines):
            row = tk.Frame(info_frame, bg="#0f2436")
            row.pack(fill="x", padx=18, pady=(10 if idx == 0 else 4, 10 if idx == len(info_lines) - 1 else 4))
            tk.Label(row, text=label, font=("Consolas", 10), fg="#7dd3fc", bg="#0f2436", width=15, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=("Consolas", 10, "bold"), fg="#e2e8f0", bg="#0f2436", anchor="w").pack(side="left")

        # Password Section
        pwd_label = tk.Label(
            self.root,
            text="Enter Password",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#091622"
        )
        pwd_label.pack(anchor="w", padx=40, pady=(20, 5))

        pwd_box = tk.Frame(self.root, bg="#0f2436", highlightbackground="#00b4d8", highlightthickness=1)
        pwd_box.pack(fill="x", padx=40, pady=2)

        tk.Label(pwd_box, text="🔒", font=("Segoe UI", 12), fg="#00b4d8", bg="#0f2436").pack(side="left", padx=(10, 5))

        self.password_entry = tk.Entry(
            pwd_box,
            show="*",
            font=("Segoe UI", 13),
            bg="#0f2436",
            fg="#ffffff",
            insertbackground="#ffffff",
            bd=0
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=5)
        self.password_entry.bind("<Return>", lambda event: self.verify_password())

        self.show_pwd = False
        self.toggle_btn = tk.Button(
            pwd_box,
            text="👁",
            font=("Segoe UI", 10),
            bg="#0f2436",
            fg="#94a3b8",
            bd=0,
            cursor="hand2",
            command=self.toggle_password
        )
        self.toggle_btn.pack(side="right", padx=8)

        tk.Label(
            self.root,
            text="Password is masked ( * * * )",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#091622"
        ).pack(anchor="w", padx=40, pady=(4, 15))

        # Access Button
        access_btn = tk.Button(
            self.root,
            text="Access BST Explorer   →",
            font=("Segoe UI", 12, "bold"),
            bg="#00b4d8",
            fg="#06121c",
            activebackground="#38bdf8",
            bd=0,
            cursor="hand2",
            command=self.verify_password
        )
        access_btn.pack(fill="x", padx=40, pady=10, ipady=10)

        tk.Label(
            self.root,
            text="UNAD · ECBTI · Systems Engineering",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#091622"
        ).pack(side="bottom", pady=14)

    def toggle_password(self):
        self.show_pwd = not self.show_pwd
        self.password_entry.config(show="" if self.show_pwd else "*")

    def verify_password(self):
        password = self.password_entry.get().strip()
        if password == "UNAD":
            self.root.destroy()
            main_root = tk.Tk()
            BSTExplorerApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Invalid Password", "Incorrect password. Please enter 'UNAD'.")


class BSTExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fase4CristianCuero — BST Explorer")
        self.root.geometry("1220x740")
        self.root.minsize(1024, 650)
        self.root.config(bg="#07131e")

        self.bst = BinarySearchTree(max_levels=4)
        self.highlighted_nodes = set()
        self.found_node = None

        self.build_main_ui()
        self.refresh_all()

    def build_main_ui(self):
        # Top Header Bar
        header = tk.Frame(self.root, bg="#0d2133", height=42)
        header.pack(fill="x", side="top")

        tk.Label(
            header,
            text="🌲  BST Explorer — Binary Search Tree",
            font=("Segoe UI", 12, "bold"),
            fg="#00b4d8",
            bg="#0d2133"
        ).pack(side="left", padx=15, pady=8)

        tk.Label(
            header,
            text="Cristian Stiven Cuero Caicedo  |  Data Structures 301305_155",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#0d2133"
        ).pack(side="right", padx=15, pady=8)

        # Body Frame
        body = tk.Frame(self.root, bg="#07131e")
        body.pack(fill="both", expand=True, padx=8, pady=8)

        # Left Controls Panel
        controls_frame = tk.Frame(body, bg="#0b1b29", width=210, highlightbackground="#16324a", highlightthickness=1)
        controls_frame.pack(side="left", fill="y", padx=(0, 8))
        controls_frame.pack_propagate(False)

        tk.Label(
            controls_frame,
            text="⚙  Controls",
            font=("Segoe UI", 11, "bold"),
            fg="#38bdf8",
            bg="#0b1b29"
        ).pack(pady=(14, 10), padx=12, anchor="w")

        tk.Label(
            controls_frame,
            text="Node Value (integer)",
            font=("Segoe UI", 9),
            fg="#cbd5e1",
            bg="#0b1b29"
        ).pack(padx=12, anchor="w")

        self.value_entry = tk.Entry(
            controls_frame,
            font=("Segoe UI", 12, "bold"),
            bg="#06101a",
            fg="#ffffff",
            insertbackground="#ffffff",
            relief="flat",
            highlightbackground="#1e4976",
            highlightthickness=1
        )
        self.value_entry.pack(fill="x", padx=12, pady=(4, 12), ipady=5)
        self.value_entry.bind("<Return>", lambda event: self.add_node())

        # Buttons
        btn_add = tk.Button(
            controls_frame,
            text="+ Add Node",
            font=("Segoe UI", 10, "bold"),
            bg="#00b4d8",
            fg="#051018",
            bd=0,
            cursor="hand2",
            command=self.add_node
        )
        btn_add.pack(fill="x", padx=12, pady=4, ipady=6)

        btn_search = tk.Button(
            controls_frame,
            text="🔍 Search Node",
            font=("Segoe UI", 10, "bold"),
            bg="#10b981",
            fg="#051018",
            bd=0,
            cursor="hand2",
            command=self.search_node
        )
        btn_search.pack(fill="x", padx=12, pady=4, ipady=6)

        btn_clear = tk.Button(
            controls_frame,
            text="🗑 Clear Tree",
            font=("Segoe UI", 10, "bold"),
            bg="#f59e0b",
            fg="#051018",
            bd=0,
            cursor="hand2",
            command=self.clear_tree
        )
        btn_clear.pack(fill="x", padx=12, pady=4, ipady=6)

        btn_exit = tk.Button(
            controls_frame,
            text="✖ Exit",
            font=("Segoe UI", 10, "bold"),
            bg="#ef4444",
            fg="#ffffff",
            bd=0,
            cursor="hand2",
            command=self.root.quit
        )
        btn_exit.pack(fill="x", padx=12, pady=4, ipady=6)

        # Tree Statistics
        stats_box = tk.LabelFrame(
            controls_frame,
            text=" Tree Statistics ",
            font=("Segoe UI", 9, "bold"),
            fg="#7dd3fc",
            bg="#0b1b29",
            bd=1,
            relief="groove"
        )
        stats_box.pack(fill="x", padx=12, pady=(18, 10), ipadx=6, ipady=6)

        self.lbl_nodes = tk.Label(stats_box, text="Nodes: 0", font=("Consolas", 9), fg="#e2e8f0", bg="#0b1b29", anchor="w")
        self.lbl_nodes.pack(fill="x", pady=1)

        self.lbl_height = tk.Label(stats_box, text="Height: 0", font=("Consolas", 9), fg="#e2e8f0", bg="#0b1b29", anchor="w")
        self.lbl_height.pack(fill="x", pady=1)

        self.lbl_root = tk.Label(stats_box, text="Root: —", font=("Consolas", 9), fg="#e2e8f0", bg="#0b1b29", anchor="w")
        self.lbl_root.pack(fill="x", pady=1)

        # Legend
        legend_box = tk.LabelFrame(
            controls_frame,
            text=" Legend ",
            font=("Segoe UI", 9, "bold"),
            fg="#7dd3fc",
            bg="#0b1b29",
            bd=1,
            relief="groove"
        )
        legend_box.pack(fill="x", padx=12, pady=5, ipadx=6, ipady=6)

        legends = [
            ("#00b4d8", "Regular node"),
            ("#10b981", "Found node"),
            ("#f59e0b", "Search path"),
            ("#eab308", "Traversal node"),
        ]
        for color, text in legends:
            row = tk.Frame(legend_box, bg="#0b1b29")
            row.pack(fill="x", pady=2)
            dot = tk.Canvas(row, width=12, height=12, bg="#0b1b29", highlightthickness=0)
            dot.pack(side="left", padx=(2, 6))
            dot.create_oval(2, 2, 10, 10, fill=color, outline=color)
            tk.Label(row, text=text, font=("Segoe UI", 8), fg="#cbd5e1", bg="#0b1b29").pack(side="left")

        # Right Area: Tree Canvas + 3 Traversal Panels
        right_panel = tk.Frame(body, bg="#07131e")
        right_panel.pack(side="right", fill="both", expand=True)

        # Panel 1: BST Tree
        tree_panel = tk.LabelFrame(
            right_panel,
            text=" 🌲 BST Tree (max 4 levels) ",
            font=("Segoe UI", 9, "bold"),
            fg="#38bdf8",
            bg="#091826",
            bd=1,
            relief="groove"
        )
        tree_panel.pack(fill="both", expand=True, pady=(0, 6))

        self.tree_canvas = tk.Canvas(tree_panel, bg="#081522", highlightthickness=0)
        self.tree_canvas.pack(fill="both", expand=True, padx=4, pady=4)
        self.tree_canvas.bind("<Configure>", lambda e: self.draw_tree())

        # Bottom Traversals Container (Panels 2, 3, 4)
        traversals_frame = tk.Frame(right_panel, bg="#07131e", height=115)
        traversals_frame.pack(fill="x", side="bottom")
        traversals_frame.pack_propagate(False)

        self.preorder_canvas = self._create_traversal_panel(traversals_frame, "↳ Pre-order", "left")
        self.inorder_canvas = self._create_traversal_panel(traversals_frame, "↳ In-order", "left")
        self.postorder_canvas = self._create_traversal_panel(traversals_frame, "↳ Post-order", "right")

        # Status Bar
        self.status_label = tk.Label(
            self.root,
            text="Ready.",
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#07131e",
            anchor="w"
        )
        self.status_label.pack(fill="x", side="bottom", padx=10, pady=(0, 4))

    def _create_traversal_panel(self, parent, title, side):
        panel = tk.LabelFrame(
            parent,
            text=f" {title} ",
            font=("Segoe UI", 9, "bold"),
            fg="#7dd3fc",
            bg="#091826",
            bd=1,
            relief="groove"
        )
        padx = (0, 5) if side == "left" else (0, 0)
        panel.pack(side=side, fill="both", expand=True, padx=padx)

        canvas = tk.Canvas(panel, bg="#081522", height=70, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=3, pady=3)
        canvas.bind("<Configure>", lambda e: self.refresh_all())
        return canvas

    def _parse_integer_input(self):
        raw = self.value_entry.get().strip()
        if not raw:
            messagebox.showwarning("Empty Input", "Please enter an integer node value.")
            return None
        try:
            return int(raw)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                f"'{raw}' is not a valid integer.\nOnly whole numbers are accepted (e.g. 10, -5, 42)."
            )
            return None

    def add_node(self):
        val = self._parse_integer_input()
        if val is None:
            return

        self.highlighted_nodes.clear()
        self.found_node = None

        success, message = self.bst.insert(val)
        if success:
            self.value_entry.delete(0, tk.END)
            self.status_label.config(text=f"✓ {message}", fg="#10b981")
            self.refresh_all()
        else:
            self.status_label.config(text=f"⚠ Could not insert node {val}.", fg="#f59e0b")
            messagebox.showwarning("Maximum Depth Reached", message)

    def search_node(self):
        val = self._parse_integer_input()
        if val is None:
            return

        if self.bst.root is None:
            messagebox.showinfo("Empty Tree", "The tree is currently empty.")
            return

        found, path = self.bst.search(val)
        path_str = " -> ".join(str(x) for x in path)

        if found:
            self.found_node = val
            self.highlighted_nodes = set(path)
            self.status_label.config(text=f"✓ Node {val} found! Path: {path_str}", fg="#10b981")
            self.refresh_all()
            messagebox.showinfo("Node Found", f"Node {val} was found in the tree.\nSearch path: {path_str}")
        else:
            self.found_node = None
            self.highlighted_nodes = set(path)
            self.status_label.config(text=f"✕ Node {val} not found. Path: {path_str}", fg="#ef4444")
            self.refresh_all()
            messagebox.showwarning("Node Not Found", f"Node {val} does not exist in the tree.\nSearched path: {path_str}")

    def clear_tree(self):
        self.bst.clear()
        self.highlighted_nodes.clear()
        self.found_node = None
        self.value_entry.delete(0, tk.END)
        self.status_label.config(text="Tree cleared successfully.", fg="#38bdf8")
        self.refresh_all()

    def refresh_all(self):
        nodes_count = self.bst.count_nodes()
        height_val = self.bst.get_height()
        root_val = self.bst.root.value if self.bst.root else "—"

        self.lbl_nodes.config(text=f"Nodes: {nodes_count}")
        self.lbl_height.config(text=f"Height: {height_val}")
        self.lbl_root.config(text=f"Root: {root_val}")

        self.draw_tree()
        self.draw_traversal(self.preorder_canvas, self.bst.preorder_traversal(), "No pre-order data")
        self.draw_traversal(self.inorder_canvas, self.bst.inorder_traversal(), "No in-order data")
        self.draw_traversal(self.postorder_canvas, self.bst.postorder_traversal(), "No post-order data")

    def draw_tree(self):
        c = self.tree_canvas
        c.delete("all")

        width = c.winfo_width()
        height = c.winfo_height()
        if width <= 10 or height <= 10:
            return

        if self.bst.root is None:
            c.create_text(
                width // 2,
                height // 2,
                text="Empty tree",
                fill="#64748b",
                font=("Segoe UI", 12)
            )
            return

        radius = 20
        top_margin = 42
        level_gap = max(55, (height - top_margin - 30) // 4)

        positions = {}

        def compute_positions(node, level, left_bound, right_bound):
            if node is None:
                return
            x = (left_bound + right_bound) // 2
            y = top_margin + (level - 1) * level_gap
            positions[id(node)] = (x, y, node.value)
            mid = (left_bound + right_bound) // 2
            compute_positions(node.left, level + 1, left_bound, mid)
            compute_positions(node.right, level + 1, mid, right_bound)

        compute_positions(self.bst.root, 1, 30, width - 30)

        def draw_edges(node):
            if node is None:
                return
            x1, y1, _ = positions[id(node)]
            for child in (node.left, node.right):
                if child is not None:
                    x2, y2, _ = positions[id(child)]
                    c.create_line(x1, y1, x2, y2, fill="#38bdf8", width=2)
                    draw_edges(child)

        draw_edges(self.bst.root)

        for _, (x, y, val) in positions.items():
            if val == self.found_node:
                fill_color = "#10b981"
                outline_color = "#a7f3d0"
            elif val in self.highlighted_nodes:
                fill_color = "#f59e0b"
                outline_color = "#fde68a"
            else:
                fill_color = "#00b4d8"
                outline_color = "#bae6fd"

            c.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                fill=fill_color, outline=outline_color, width=2
            )
            c.create_text(
                x, y,
                text=str(val),
                fill="#051018",
                font=("Segoe UI", 10, "bold")
            )

    def draw_traversal(self, canvas, values, empty_text):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 10:
            width = 340
        if height <= 10:
            height = 65

        if not values:
            canvas.create_text(
                width // 2,
                height // 2,
                text=empty_text,
                fill="#64748b",
                font=("Segoe UI", 9)
            )
            return

        n = len(values)
        margin_x = 16
        usable_width = max(40, width - 2 * margin_x)
        cy = height // 2

        # Dynamic spacing and radius so all nodes fit within the canvas width
        if n == 1:
            r = min(14, max(8, height // 2 - 6))
            positions = [width // 2]
        else:
            step = usable_width / (n - 1)
            step = min(step, 36.0)
            r = int(min(14.0, max(7.0, step * 0.38, (height - 12) / 2.0)))
            total_span = step * (n - 1)
            start_x = (width - total_span) / 2.0
            positions = [start_x + idx * step for idx in range(n)]

        font_size = max(7, min(9, int(r * 0.65)))

        for idx, (val, cx) in enumerate(zip(values, positions)):
            if idx > 0:
                prev_x = positions[idx - 1]
                if cx - prev_x > 2 * r:
                    canvas.create_line(
                        prev_x + r, cy, cx - r, cy,
                        fill="#eab308", width=1.5
                    )

            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill="#eab308", outline="#fef08a", width=1.5
            )
            canvas.create_text(
                cx, cy,
                text=str(val),
                fill="#091622",
                font=("Segoe UI", font_size, "bold")
            )
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width <= 10:
            width = 340
        if height <= 10:
            height = 65

        if not values:
            canvas.create_text(
                width // 2,
                height // 2,
                text=empty_text,
                fill="#64748b",
                font=("Segoe UI", 9)
            )
            return

        r = 14
        spacing = 34
        start_x = 24
        cy = height // 2

        for idx, val in enumerate(values):
            cx = start_x + idx * spacing
            if idx > 0:
                prev_x = start_x + (idx - 1) * spacing
                canvas.create_line(prev_x + r, cy, cx - r, cy, fill="#eab308", width=1.5)

            canvas.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill="#eab308", outline="#fef08a", width=1.5
            )
            canvas.create_text(
                cx, cy,
                text=str(val),
                fill="#091622",
                font=("Segoe UI", 8, "bold")
            )


if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()