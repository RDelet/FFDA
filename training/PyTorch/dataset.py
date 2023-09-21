from torch import is_tensor
from torch.utils.data import Dataset


class FDDADataset(Dataset):

    def __init__(self, data: dict):
        """@!Brief Initialize dataset
                   Makes one dataset per joint.
        """
        super().__init__()

        self.data = {}
        self.joints = data['joints']
        self.delta = data['delta']

    def __len__(self) -> int:
        return len(self.joints)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(input shape: {self.joints.shape}, " \
               f"output shape: {self.delta.shape})"

    def __getitem__(self, idx):
        if is_tensor(idx):
            idx = idx.tolist()

        joint = self.joints[idx]
        delta = self.delta[idx]

        return joint, delta
