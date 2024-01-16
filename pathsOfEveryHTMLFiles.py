import json


def pathOfEveryHTMLFiles(textFileName:str)-> list:
    with open(textFileName, 'r') as file:
        text = file.read()
        listOfLines = text.splitlines()
        cpListOfLines = listOfLines[::]
        for i in range(len(cpListOfLines)):
            currentFileSplited = f"{cpListOfLines[i]}".split(".")
            currentFileExtension = currentFileSplited[len(currentFileSplited)-1]
            if(currentFileExtension != "html"):
                listOfLines.remove(cpListOfLines[i])
        listOfLines.sort()
        for i in range(len(listOfLines)):
            listOfLines[i] = listOfLines[i].replace("- assets/", "")
        return listOfLines

filePath = 'file_paths.txt'
output_file = 'OnlyHTMLFileList.json'
listOfLines=  pathOfEveryHTMLFiles(filePath)

with open(output_file, 'w') as file:
    json.dump({"list":listOfLines}, file, indent=4)

print("File paths saved to:", output_file)