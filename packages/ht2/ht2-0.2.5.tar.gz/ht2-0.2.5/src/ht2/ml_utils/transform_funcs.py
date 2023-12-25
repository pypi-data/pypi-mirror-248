import torchvision.transforms as T
from torch import nn
import torch.nn.functional as F
import torch


class PadCenterCrop(nn.Module):
    def __init__(self, size, fill=0, padding_mode='constant',wrap=1):
        """given a target size of image:
            1. resize image to fit within target size while keeping ratio
            2. pad image with fill to target size
            3. split image along width into [wrap] parts, stack along height dimension, h*w becomes (h*wrap)*(w/wrap)

        Args:
            size ((int,int)): target size of image
            fill (int, optional): padding value. Defaults to 0.
            padding_mode (str, optional): padding mode. Defaults to 'constant'.
            wrap (int, optional): number of pieces to wrap into. Defaults to 1.
        """
        if isinstance(size, (int, float)):
            self.size = (int(size), int(size))
        else:
            self.size = size
        self.padding_mode = padding_mode
        self.fill = fill
        self.wrap = wrap

    def __call__(self, img):
        # unify to 3 channel
        if img.size()[0] == 1:
            img = img.repeat(3,1,1)

        # resize keep ratio
        ratio = min(self.size[0]/img.size()[1], self.size[1]/img.size()[2])
        img = T.Resize((int(img.size()[1]*ratio), int(img.size()[2]*ratio)),antialias=True)(img)

        # padding
        img = F.pad(img, [0, self.size[1]-img.size()[2], 0, self.size[0]-img.size()[1]], self.padding_mode, self.fill)
        # split image along width into [wrap] parts, stack along height dimension, h*w becomes (h*wrap)*(w/wrap)
        img = torch.cat(torch.split(img, int(img.size()[2]/self.wrap), dim=2), dim=1)

        return img



