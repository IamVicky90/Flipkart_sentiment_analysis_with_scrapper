import pymongo
import csv
import os
def main():
    client = pymongo.MongoClient("mongodb+srv://vicky:<password>@cluster0.whn7h.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client['web_scrapper']
    csv_data_path=os.path.join('data','raw')
    files_list=os.listdir(csv_data_path)
    for file in files_list:
        if '.csv' in file:
            product_name=file.split('.csv')[0]
            print(product_name)
            reviews = db[product_name].find({})
            if reviews.count()>0:
                continue
            table=db[product_name]
            with open(os.path.join(csv_data_path,file),'r') as f:
                reader=csv.reader(f)
                next(reader)
                for row in reader:
                    dic={}
                    dic['product']=row[0]
                    dic['customer_name']=row[1]
                    dic['ratings']=row[2]
                    dic['header']=row[3]
                    dic['comment']=row[4]
                    table.insert_one(dic)
main()
