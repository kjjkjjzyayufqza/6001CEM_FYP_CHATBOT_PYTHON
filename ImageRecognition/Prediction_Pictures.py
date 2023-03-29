import os
import torch
import torchvision
from PIL import Image
from torch import nn
import io

#create image class json
# with open('imageClassName.json', 'w+') as outfile:
#     for i in data_folderList:
#         outfile.write(i + "\n")

current_path = os.path.dirname(__file__) + '/'
data_folderList = []
with open(current_path + 'imageClassName.json', 'r') as outfile:
    lines = outfile.readlines()
    lines = [line.rstrip() for line in lines]
    data_folderList = lines

def PredictionPictures(imageByte: bytes):
    # read image data
    image = Image.open(io.BytesIO(imageByte))
    transforms = torchvision.transforms.Compose([torchvision.transforms.Resize((64, 64)),
                                                torchvision.transforms.ToTensor()])
    image = transforms(image)
    model_ft = torchvision.models.resnet18()  # 需要使用训练时的相同模型
    in_features = model_ft.fc.in_features
    model_ft.fc = nn.Linear(60, 23)  # 此处也要与训练模型一致
    model = torch.load(current_path + "best_model_yaopian.pth",
                       map_location=torch.device("cpu"))  # 选择训练后得到的模型文件
    image = torch.reshape(image, (1, 3, 64, 64))  # 修改待预测图片尺寸，需要与训练时一致
    model.eval()
    with torch.no_grad():
        output = model(image)
    return ("The picture is predicted to be : {}".format(
        data_folderList[int(output.argmax(1))]))

