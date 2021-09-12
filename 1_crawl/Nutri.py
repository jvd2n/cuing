import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

class Nutrition(object):
    url = 'https://terms.naver.com/list.naver?cid=59320&categoryId=59320'
    # https://terms.naver.com/list.naver?cid=59320&categoryId=59320&page=1
    driver_path = 'D:/chromedriver'
    dict = {}
    df = None
    food_name = []
    food_nut = []
    new_food_nut = []

    def scrap_name(self):
        driver = webdriver.Chrome(self.driver_path)
        driver.get(self.url)
        all_div = BeautifulSoup(driver.page_source, 'html.parser')
        ls1 = all_div.find_all("div", {"class": "subject"})
        for i in ls1:
            self.food_name.append(i.find('a').text)
        # print(self.food_name)

        ls2 = all_div.find_all("p", {"class": "desc __ellipsis"})
        for i in ls2:
            self.food_nut.append(i.text)
        # print(self.food_nut)
        
        # for i, j in enumerate(ls1):
        #     print(i.find("a").text)
        #     self.dict[ls1.find("a").text] = ls2[i]
        
        print(len(self.food_name))
        print(len(self.food_nut))
        self.food_name.remove('인문과학')
        for i in self.food_nut:
            temp = i.replace('\n', '').replace('\t', '').replace(' ', '').replace('[영양성분]', '')
            self.new_food_nut.append(temp)
        
        for i, j in enumerate(self.food_name):
            # print(i, j)
            # print(self.food_name[i])
            # print(self.food_nut[i])
            self.dict[self.food_name[i]] = self.new_food_nut[i]
        
        print(self.dict)
        
        driver.close()

        '''
        for i in ls:
            print()
            self.food_nut.append(i.find("p").text)
        driver.close()
    def insert_dict(self):
        for i, j in zip(self.food_name, self.food_nut):
            self.dict[i] = j
            print(f'{i}:{j}')
    def dict_to_dataframe(self):
        dt = self.dict
        self.df = pd.DataFrame.from_dict(dt, orient='index')
        print(self.df)
    def df_to_csv(self):
        path = './data/food_nutrition.csv'
        self.df.to_csv(path, sep=',', na_rep='Nan')
'''
    @staticmethod
    def main():
        nut = Nutrition()
        while 1:
            menu = input('0-Exit\n1-print\n') #2-insert dict\n3-dataframe\n4-csv\n')
            if menu == '0':
                break
            elif menu == '1':
                nut.scrap_name()
            #     nut.scrap_nut()
            # elif menu == '2':
            #     nut.insert_dict()
            # elif menu == '3':
            #     nut.dict_to_dataframe()
            # elif menu == '4':
            #     nut.df_to_csv()
            else:
                continue

Nutrition.main()