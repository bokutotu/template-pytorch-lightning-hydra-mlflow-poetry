import torch
import torch.nn as nn
import torch.nn.functional as F

from torch import Tensor
from typing import Tuple


class VAE(nn.Module):
    def __init__(self) -> None:
        super(VAE, self).__init__()

        self.fc1 = nn.Linear(784, 400)
        self.fc2_mu = nn.Linear(400, 20)
        self.fc2_logvar = nn.Linear(400, 20)
        self.fc3 = nn.Linear(20, 400)
        self.fc4 = nn.Linear(400, 784)


    def reparameterize(self, mu: Tensor, logvar: Tensor) -> Tensor:
        std = torch.exp(0.5 * logvar)
        eps = torch.randn_like(std)
        return mu + eps * std


    def encode(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        h1 = F.relu(self.fc1(x))
        mu = self.fc2_mu(h1)
        logvar = self.fc2_logvar(h1)
        return mu, logvar


    def decode(self, z: Tensor) -> Tensor:
        h3 = F.relu(self.fc3(z))
        return F.sigmoid(self.fc4(h3))


    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
        mu, logvar = self.encode(x.view(-1, 784))
        z = self.reparameterize(mu, logvar)
        out = self.decode(z)
        return out, mu, logvar