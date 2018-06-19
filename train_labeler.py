train_names = open("train.txt", "r")
train_labels = open("train_labels.txt", "r")

result = []

image_list = []
labels = []

for line in train_names:
    line_temp = line[ : -4]
    line_temp_int = int(float(line_temp))
    image_list.append(line_temp_int)

for line in train_labels:
    
