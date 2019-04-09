import csv

csvData = [['Name', 'Age'], ['Peter', '22'], ['me', '1'], ['you', '45']]
with open('person.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(csvData)
print(csvData[1][1])

myCSVDataList = [['Name', 'IOU', 'Recall']]
pic1='/home/sdflsj.jpg'
pic1I = 0.1
pic1R = 0.5
myCSVDataList.append([pic1, pic1I, pic1R])
print(myCSVDataList)