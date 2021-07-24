import pymongo
import csv
import os
from src.logger_file import logger
def main():
    log=logger.log()
    try:
        client = pymongo.MongoClient(os.environ.get('VICKY_MONGODB_ACESS_KEY'))
        log.log_writter(f'Connected to the mongodb client','mongodb_operations.log')
    except Exception as e:
        log.log_writter(f'Could not connected to the mongodb client, error: {str(e)}','mongodb_operations.log',message_type='ERROR')
    try:
        db = client['web_scrapper']
        log.log_writter(f'Successfully creating the web_scrapper database','mongodb_operations.log')
    except Exception as e:
        log.log_writter(f'Error while  creating the web_scrapper database','mongodb_operations.log',message_type='ERROR')
    csv_data_path=os.path.join('data','raw')
    files_list=os.listdir(csv_data_path)
    for file in files_list:
        if '.csv' in file:
            product_name=file.split('.csv')[0]
            reviews = db[product_name].find({})
            if reviews.count()>0:
                log.log_writter(f'{product_name} data is already dumped into database so leave this process','mongodb_operations.log',message_type='Warning')
                continue
            log.log_writter(f'The process of dumping the data of product {product_name} is now starting in a while','mongodb_operations.log',message_type='Warning')
            try:
                table=db[product_name]
                log.log_writter(f'database has been created successfully with name {product_name}','mongodb_operations.log')
            except Exception as e:
                log.log_writter(f'Error occured while creating the database with name {product_name}, error: {str(e)}','mongodb_operations.log',message_type='ERROR')
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
    log.log_writter(f'mongodb_operations module has been done','mongodb_operations.log')    
                
main()
