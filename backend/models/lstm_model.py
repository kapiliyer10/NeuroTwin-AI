try:
    import torch.nn as nn
except ImportError:  # pragma: no cover - torch is optional for lightweight API tests.
    nn = None


if nn is not None:

    class CognitiveLSTM(nn.Module):
        def __init__(self, input_size: int = 4, hidden_size: int = 64, output_size: int = 4) -> None:
            super().__init__()
            self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
            self.fc = nn.Linear(hidden_size, output_size)

        def forward(self, x):
            _, (hidden, _) = self.lstm(x)
            return self.fc(hidden[-1])

else:

    class CognitiveLSTM:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs) -> None:
            raise ImportError("Install torch to use CognitiveLSTM.")
