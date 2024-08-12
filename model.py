import torch.nn as nn

class LightNet(nn.Module):
    def __init__(self, category_num):
        super(LightNet, self).__init__()

        self.feture_extracter = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(),
            nn.Flatten(),

        )

        self.classifier = nn.Sequential(
            nn.Linear(in_features=514560, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=category_num),
            nn.Softmax(dim=1)
        )

    def forward(self, target_input):
        feature = self.feture_extracter(target_input)
        res = self.classifier(feature)
        return res