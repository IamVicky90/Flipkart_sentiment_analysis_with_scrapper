import os
import argparse
from bs4 import BeautifulSoup as bs
import requests 
from urllib.request import urlopen as ureq
from src.logger_file import logger
import csv
class scrapper:
    def __init__(self):
        self.log=  logger.log()
    def scrap_data(self,search_string):
        """
        This is a funtion to scrap data from flipkart and convert it into a csv file
        - search_string: Type the name of the prodict to scrap it's data
        Written By: vicky
        Version: 1.0
        Revisions: None
        """
        self.log.log_writter(f'Process to scrap the data is started','scrapper.log')
        url='https://www.flipkart.com/search?q='+search_string.replace(' ','')
        self.log.log_writter(f'search string is {search_string}','scrapper.log')
        try:
            uclient=ureq(url)
            flipkart_page=uclient.read()
            uclient.close()
            self.log.log_writter(f'Successfully created the uclient for flipkart_page','scrapper.log')
        except Exception as e:
            self.log.log_writter(f'Error occured while creating the uclient for flipkart_page, error: {str(e)}','scrapper.log',message_type='ERROR')
        try:
            flipkart_html=bs(flipkart_page,'html.parser')
            self.log.log_writter(f'Successsfully parse the flipkart_html by BeautifulSoup','scrapper.log')
        except Exception as e:
            self.log.log_writter(f'Couldnot parse the flipkart_html by BeautifulSoup, error: {str(e)}','scrapper.log',message_type='ERROR')
        try:
            bigbox=flipkart_html.findAll('div',{'class':'_1AtVbE col-12-12'},)
            self.log.log_writter(f'Sucessfully take the bigbox comment sections','scrapper.log')
        except Exception as e:
            self.log.log_writter(f'Couldnot take the bigbox comment sections, error: {str(e)}','scrapper.log',message_type='ERROR')
        del bigbox[0:3]
        columns=['product','customer_name','ratings','header','comment']
        csv_data_path=os.path.join('data','raw')
        try:
            if os.sys=='Windows':
                path=csv_data_path+"\\"+f'{str(len(os.listdir(csv_data_path)))}_{search_string}.csv'
            else:
                path=csv_data_path+"/"+f'{str(len(os.listdir(csv_data_path)))}_{search_string}.csv'
            self.log.log_writter(f'Sucessfully take the path for csv_data_path that is {csv_data_path} for system {str(os.sys)}','scrapper.log')
        except Exception as e:
            self.log.log_writter(f'Couldnot take the path for csv_data_path for system {str(os.sys)}','scrapper.log',message_type='ERROR')
        for iter,box in enumerate(bigbox):
            if iter==10:
                break
            try:
                product_link='https://www.flipkart.com'+box.div.div.div.a['href']
                self.log.log_writter(f'product link for {search_string} {product_link}','scrapper.log')
                product_page=requests.get(product_link)
                product_html=bs(product_page.text,'html.parser')
                comments_settion=product_html.findAll('div',{'class':'col JOpGWq'})
                link='https://www.flipkart.com'+comments_settion[0].a['href'].split('&aid')[0]
                self.log.log_writter(f' link for comments_section {link}','scrapper.log')
                full_product_page=requests.get(link)
                full_product_html=bs(full_product_page.text,'html.parser')
                pages_links=full_product_html.findAll('a',{'class':'ge-49M'})
                for i,page_link in enumerate(pages_links):
                    if i==10:
                        break
                    page_request_link='https://www.flipkart.com'+page_link['href']
                    page_request=requests.get(page_request_link)
                    self.log.log_writter(f'page request link is: https://www.flipkart.com+{page_request_link}','scrapper.log')
                    page_html=bs(page_request.text,'html.parser')
                    product_review_section=page_html.findAll('div',{'class':'col _2wzgFH K0kLPL'})
                    for var_i,review in enumerate(product_review_section):
                        data_list=[]
                        data_list.append(str(search_string))
                        try:
                            customer_name=review.findAll('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
                        except Exception as e:
                            customer_name='Unknown'
                        data_list.append(str(customer_name))
                        try:
                            ratings=review.div.div.text
                        except Exception as e:
                            ratings='Unknown'
                        data_list.append(str(ratings))
                        try:
                            header=review.div.p.text
                        except Exception as e:
                            header='Unknown'
                        data_list.append(str(header))
                        try:
                            comment=review.findAll('div',{'class':'t-ZTKy'})[0].div.text
                        except Exception as e:
                            comment='Unknown'
                        data_list.append(str(comment))

                        with open(path, 'a', encoding='UTF8', newline='') as f:
                            writer = csv.writer(f)
                            # write the header
                            if iter==0 and i==0 and var_i==0:
                                writer.writerow(columns)
                            # write multiple rows
                            writer.writerow(data_list)
            except Exception as e:
                self.log.log_writter(f'Error occured while scraping the data so we stop here','scrapper.log',message_type='ERROR')
        self.log.log_writter(f'Sucessfully scrapped the data and completed the process','scrapper.log')

parser = argparse.ArgumentParser(description='Enter the string to search that product')
parser.add_argument('string', type=str,
                    help='Enter the string to search that product')
args = parser.parse_args()
scrapper_obj=scrapper()
scrapper_obj.scrap_data(args.string)