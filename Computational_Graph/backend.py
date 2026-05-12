import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# ============================================================
# 1. COMPUTATIONAL GRAPH ENGINE (micrograd-style autograd)
# ============================================================
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += out.grad
            other.grad += out.grad
        out._backward = _backward
        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), '*')
        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad
        out._backward = _backward
        return out

    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data ** other, (self,), f'**{other}')
        def _backward():
            self.grad += other * (self.data ** (other - 1)) * out.grad
        out._backward = _backward
        return out

    def __neg__(self): return self * (-1)
    def __sub__(self, other): return self + (-other)
    def __radd__(self, other): return self + other
    def __rmul__(self, other): return self * other
    def __rsub__(self, other): return other + (-self)

    def tanh(self):
        x = self.data
        t = (np.exp(2*x) - 1) / (np.exp(2*x) + 1)
        out = Value(t, (self,), 'tanh')
        def _backward():
            self.grad += (1 - t**2) * out.grad
        out._backward = _backward
        return out

    def exp(self):
        x = self.data
        out = Value(np.exp(x), (self,), 'exp')
        def _backward():
            self.grad += out.data * out.grad
        out._backward = _backward
        return out

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    def __repr__(self):
        return f"Value(data={self.data:.4f}, grad={self.grad:.4f})"


# ============================================================
# 2. LINEAR REGRESSION TRAINING
# ============================================================
def train_linear_regression_cg(X_np, Y_np, lr=0.01, epochs=100, log_callback=None):
    """Train using the Value-based computational graph (for education)"""
    n = len(X_np)
    W = Value(np.random.randn() * 0.1, label='W')
    b = Value(np.random.randn() * 0.1, label='b')
    losses = []

    for epoch in range(epochs):
        total_loss = Value(0.0)
        for i in range(n):
            x = Value(X_np[i], label='x')
            y = Value(Y_np[i], label='y')
            y_pred = x * W + b
            diff = y_pred - y
            loss_i = diff ** 2
            total_loss = total_loss + loss_i

        mse = total_loss * (1.0 / n)
        for p in [W, b]:
            p.grad = 0.0
        mse.backward()

        W.data -= lr * W.grad
        b.data -= lr * b.grad
        losses.append(mse.data)

        if epoch % 10 == 0 and log_callback:
            log_callback(f"Epoch {epoch:4d}, Loss = {mse.data:.6f}")

    return W.data, b.data, losses


def train_linear_regression(X_np, Y_np, lr=0.01, epochs=500, log_callback=None):
    """Train using numpy vectorized operations (fast)"""
    n = len(X_np)
    W = np.random.randn() * 0.1
    b = np.random.randn() * 0.1
    losses = []

    for epoch in range(epochs):
        Y_pred = W * X_np + b
        diff = Y_pred - Y_np
        loss = np.mean(diff ** 2)

        dW = np.mean(2 * diff * X_np)
        db = np.mean(2 * diff)

        W -= lr * dW
        b -= lr * db
        losses.append(loss)

        if epoch % 50 == 0 and log_callback:
            log_callback(f"Epoch {epoch:4d}, Loss = {loss:.6f}")

    return W, b, losses


def predict(X, W, b):
    return W * X + b


def compute_metrics(Y_true, Y_pred):
    mse = np.mean((Y_pred - Y_true) ** 2)
    r2 = 1 - np.sum((Y_true - Y_pred) ** 2) / np.sum((Y_true - np.mean(Y_true)) ** 2)
    return mse, r2


# ============================================================
# 3. VISUALIZATION
# ============================================================
from matplotlib.figure import Figure


def plot_regression(X_np, Y_np, W, b):
    fig = Figure(figsize=(10, 6))
    ax = fig.subplots()
    ax.scatter(X_np, Y_np, alpha=0.5, label='Dữ liệu thực tế')
    x_line = np.linspace(X_np.min(), X_np.max(), 100)
    y_line = W * x_line + b
    ax.plot(x_line, y_line, 'r-', linewidth=2, label=f'Dự đoán: final = {W:.4f} * midterm + {b:.4f}')
    ax.set_xlabel('Điểm giữa kỳ (Midterm)', fontsize=12)
    ax.set_ylabel('Điểm cuối kỳ (Final)', fontsize=12)
    ax.set_title('Hồi quy tuyến tính - Điểm giữa kỳ vs Cuối kỳ', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_loss_curve(losses):
    fig = Figure(figsize=(10, 5))
    ax = fig.subplots()
    ax.plot(losses, 'b-', linewidth=1)
    ax.set_xlabel('Epoch', fontsize=12)
    ax.set_ylabel('MSE Loss', fontsize=12)
    ax.set_title('Đường cong hội tụ của Loss', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def draw_computational_graph(root_val, title="Computational Graph"):
    G = nx.DiGraph()
    pos = {}
    labels = {}
    node_list = []

    def build_graph(v, layer=0, order=0):
        if v not in node_list:
            node_list.append(v)
            node_id = id(v)
            label = v.label if v.label else v._op
            val_str = f"{label}\n{v.data:.4f}\ngrad={v.grad:.4f}"
            G.add_node(node_id, label=val_str, layer=layer)
            pos[node_id] = (layer, -order)
            for child in v._prev:
                child_id = build_graph(child, layer - 1, order)
                G.add_edge(child_id, node_id)
                order += 0.5
        return id(v)

    build_graph(root_val)
    nx.set_node_attributes(G, pos, 'pos')

    fig = Figure(figsize=(12, 8))
    ax = fig.subplots()
    ax.set_title(title, fontsize=16, fontweight='bold')

    node_labels = nx.get_node_attributes(G, 'label')
    node_colors = [
        '#FFB3BA' if ',grad=' not in l
        else '#BAFFC9' if 'W' in l or 'b' in l
        else '#BAE1FF'
        for l in node_labels.values()
    ]

    nx.draw(G, pos, with_labels=True, labels=node_labels,
            node_color=node_colors, node_size=3000,
            font_size=8, font_weight='bold',
            edge_color='gray', arrows=True,
            arrowsize=20, ax=ax)
    fig.tight_layout()
    return fig


def draw_manual_computational_graph():
    G = nx.DiGraph()
    fig = Figure(figsize=(14, 8))
    ax = fig.subplots()

    nodes = {
        'x': (0, 2), 'W': (0, 0), 'b': (2, -2),
        'mul': (2, 1), 'add': (4, 0),
        'y': (6, 0), 'sub': (6, -1.5),
        'sq': (8, -1.5), 'mean': (10, -1.5)
    }
    for name, pos in nodes.items():
        G.add_node(name, pos=pos)

    edges = [('x', 'mul'), ('W', 'mul'), ('mul', 'add'),
             ('b', 'add'), ('add', 'sub'), ('y', 'sub'),
             ('sub', 'sq'), ('sq', 'mean')]
    G.add_edges_from(edges)

    labels = {
        'x': 'midterm\n(x)', 'W': 'W', 'mul': 'x * W',
        'b': 'b', 'add': '+', 'y': 'final\n(y)',
        'sub': '-', 'sq': '(.)²', 'mean': 'MSE Loss'
    }
    node_colors = [
        '#FFD700' if n in ['x', 'y'] else
        '#FF6B6B' if n in ['W', 'b'] else
        '#4ECDC4' if n in ['mul', 'add', 'sub'] else
        '#45B7D1' if n in ['sq', 'mean'] else '#FFFFFF'
        for n in G.nodes()
    ]

    pos_nx = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos_nx, with_labels=True, labels=labels,
            node_color=node_colors, node_size=3500,
            font_size=10, font_weight='bold',
            edge_color='#666666', arrows=True,
            arrowsize=25, ax=ax,
            connectionstyle='arc3,rad=0.1')

    ax.annotate('Forward', xy=(3, 3), fontsize=12, fontweight='bold', color='green',
                ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.annotate('Backward', xy=(3, -3.5), fontsize=12, fontweight='bold', color='red',
                ha='center', bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax.set_title('Đồ thị tính toán (Computational Graph) của hồi quy tuyến tính',
                 fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    fig.tight_layout()
    return fig
