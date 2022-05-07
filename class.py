import os

rootFolder = r'/home/nvidia/Desktop/BDAFinal'   # ??????????
destination = os.path.join(rootFolder, r'yolo_data')

files = os.listdir(destination)
numTrainingData = int(len(files) * 0.8)

with open(os.path.join(rootFolder, 'train.txt'), 'w', encoding='UTF-8') as outfile:
    for filename in files[:numTrainingData]:
        if os.path.splitext(filename)[1] != '.txt':            
            outfile.writelines(os.path.join(destination, filename) + '\n')
            
with open(os.path.join(rootFolder, 'val.txt'), 'w', encoding='UTF-8') as outfile:
    for filename in files[numTrainingData:]:
        if os.path.splitext(filename)[1] != '.txt':            
            outfile.writelines(os.path.join(destination, filename) + '\n')
