from bs4 import BeautifulSoup as bs
import requests 
from urllib.request import urlopen as ureq
from logger_file import logger
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
        url='https://www.flipkart.com/search?q='+search_string
        uclient=ureq(url)
        flipkart_page=uclient.read()
        uclient.close()
        flipkart_html=bs(flipkart_page,'html.parser')
        bigbox=flipkart_html.findAll('div',{'class':'_1AtVbE col-12-12'},)
        del bigbox[0:3]
        columns=['product','customer_name','ratings','header','comment']
        for iter,box in enumerate(bigbox):
            try:
                product_link='https://www.flipkart.com'+box.div.div.div.a['href']
                product_page=requests.get(product_link)
                product_html=bs(product_page.text,'html.parser')
                comments_settion=product_html.findAll('div',{'class':'col JOpGWq'})
                link='https://www.flipkart.com'+comments_settion[0].a['href'].split('&aid')[0]
                full_product_page=requests.get(link)
                full_product_html=bs(full_product_page.text,'html.parser')
                pages_links=full_product_html.findAll('a',{'class':'ge-49M'})
                for i,page_link in enumerate(pages_links):
                    if i==10:
                        break
                    print(page_link['href'])
                    page_request=requests.get('https://www.flipkart.com'+page_link['href'])
                    page_html=bs(page_request.text,'html.parser')
                    product_review_section=page_html.findAll('div',{'class':'col _2wzgFH K0kLPL'})
                    for review in product_review_section:
                        data_list=[]
                        data_list.append(str(search_string))
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
                        try:
                            customer_name=review.findAll('p',{'class':'_2sc7ZR _2V5EHH'})[0].text
                        except Exception as e:
                            customer_name='Unknown'
                        data_list.append(str(customer_name))
                        
                        with open('data.csv', 'a', encoding='UTF8', newline='') as f:
                            writer = csv.writer(f)
                            # write the header
                            if iter==0:
                                writer.writerow(columns)
                            # write multiple rows
                            writer.writerow(data_list)
            except Exception as e:
                break
scrap_obj=scrapper()
scrap_obj.scrap_data('iphone')
