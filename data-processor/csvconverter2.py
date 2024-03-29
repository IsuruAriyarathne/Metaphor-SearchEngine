import csv 
import json 

def csv_to_json_column_wise(csvFilePath):
    jsonArray = []

    Lyricist_en = []
    Lyricist_sn = []
    Composer_en = []
    Composer_sn = []
    Singer_en = []
    Singer_sn = []

    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 

        for row in csvReader: 
            Lyricist_en.append(row["Lyricist_en"])
            Lyricist_sn.append(row["Lyricist"])
            Composer_en.append(row["Composer_en"])
            Composer_sn.append(row["Composer"])
            Singer_en.append(row["Singer_en"])
            Singer_sn.append(row["Singer"])

    #convert python jsonArray to JSON String and write to file
    with open('unique-vals/Lyricist_en.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Lyricist_en, indent=4)
        jsonf.write(jsonString)
    
    with open('unique-vals/Lyricist_sn.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Lyricist_sn, indent=4)
        jsonf.write(jsonString)

    with open('unique-vals/Composer_en.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Composer_en, indent=4)
        jsonf.write(jsonString)

    with open('unique-vals/Composer_sn.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Composer_sn, indent=4)
        jsonf.write(jsonString)

    with open('unique-vals/Singer_en.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Singer_en, indent=4)
        jsonf.write(jsonString)
    
    with open('unique-vals/Singer_sn.json', 'w', encoding='utf-8') as jsonf: 
        jsonString = json.dumps(Singer_sn, indent=4)
        jsonf.write(jsonString)

csv_to_json_column_wise("data-processor/Corpus-Unique-Vals.csv")