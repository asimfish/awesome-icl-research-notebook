import numpy as np
import torch
from torch import nn


class HistoryPolicy(nn.Module):
    def __init__(self, n=5, hidden=96):
        super().__init__()
        self.n = n
        self.gru = nn.GRU(4*n+1, hidden, batch_first=True)
        self.head = nn.Sequential(nn.Linear(hidden+2*n, hidden), nn.ReLU(),
                                  nn.Linear(hidden, n+1))

    def forward(self, tokens, lengths, state, goal):
        sequence, _ = self.gru(tokens)
        indices = (lengths - 1).clamp(min=0)
        memory = sequence[torch.arange(len(lengths)), indices]
        memory = memory * (lengths > 0).float().unsqueeze(1)
        return self.head(torch.cat([memory, state, goal], dim=1))


def inputs(histories, states, goals, n):
    """Only public receipts and visible query; no task ID or hidden graph."""
    lengths = np.array([len(h) for h in histories], dtype=np.int64)
    tokens = np.zeros((len(histories), max(1, int(lengths.max())), 4*n+1), dtype=np.float32)
    for i, history in enumerate(histories):
        tokens[i, :len(history)] = history
    return (torch.from_numpy(tokens), torch.from_numpy(lengths),
            torch.from_numpy(np.array(states, dtype=np.float32)),
            torch.from_numpy(np.array(goals, dtype=np.float32)))
