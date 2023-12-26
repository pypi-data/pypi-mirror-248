import torch
from torch import nn
from torch.utils.data import DataLoader

device = "cuda" if torch.cuda.is_available() else "cpu"


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        size = 20
        # self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Conv1d(2, 4, 1, stride=1),
            nn.ReLU(),
            # nn.Linear(50, size),
            nn.Conv1d(4, 8, 5, stride=5),
            nn.ReLU(),
            nn.Conv1d(8, 16, 5, stride=5),
            nn.ReLU(),
            # nn.Conv1d(size, size, 5, stride=2),
            # nn.ReLU(),
            # nn.Conv1d(size, 1, 1, stride=2),
            # nn.ReLU(),
            nn.Flatten(),
            nn.Linear(16, 1),
        )

    def forward(self, x):
        # x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def train(dataloader, model, loss_fn, optimizer, y_mean):
    total_loss = 0
    mean_loss = 0
    for batch_idx, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)
        y = y.unsqueeze(1)

        # 損失誤差を計算
        pred = model(X)
        loss = loss_fn(pred, y)

        # バックプロパゲーション
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        mean_pred = torch.full_like(y, y_mean)
        mean_loss += loss_fn(mean_pred, y) * len(X)
        total_loss += loss.item() * len(X)
    total_loss /= len(dataloader.dataset)
    mean_loss /= len(dataloader.dataset)
    print(f"Train Error: Avg loss: {total_loss:>7f}, One loss: {mean_loss:>8f}")


def test(dataloader, model, loss_fn, y_mean):
    size = len(dataloader.dataset)
    model.eval()
    test_loss = 0
    mean_loss = 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            y = y.unsqueeze(1)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()

            mean_pred = torch.full_like(y, y_mean)
            mean_loss += loss_fn(mean_pred, y).item()
    test_loss /= size
    mean_loss /= size
    print(f"Test Error: Avg loss: {test_loss:>8f}, One loss: {mean_loss:>8f}")
