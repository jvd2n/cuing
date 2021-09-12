import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import chain


class Nutrition(object):
    # url = 'https://terms.naver.com/list.naver?cid=59320&categoryId=59320'
    url = None
    driver_path = 'D:/chromedriver'
    dict = {}
    df = None
    food_name = []
    food_nut = []
    new_food_nut = []
    new_food_gram = []
    new_food_kcal = []
    final_food_nut = []

    def scrap_name(self):

        for i in range(1, 3):
            self.url = f'https://terms.naver.com/list.naver?cid=59320&categoryId=59320&page={i}'
            driver = webdriver.Chrome(self.driver_path)
            driver.get(self.url)
            all_div = BeautifulSoup(driver.page_source, 'html.parser')
            ls1 = all_div.find_all("div", {"class": "subject"})
            for i in ls1:
                self.food_name.append(i.find('a').text)     # name
            # print(self.food_name)


            ls2 = all_div.find_all("p", {"class": "desc __ellipsis"})
            for i in ls2:
                self.food_nut.append(i.text)
            
            # ls3 = all_div.find_all("div", {"class": "related"})
            ls3 = all_div.find_all("span", {"class": "info"})        # 1회 제공량
            
            for i, j in enumerate(ls3):
                # print(f'{i} // {j.text}')
                if '1회제공량' in j.text:
                    self.new_food_gram.append(j.text)
                elif '칼로리' in j.text:
                    self.new_food_kcal.append(j.text)
                else:
                    pass
            
            # print(len(self.food_name))  # 16
            # print(len(self.food_nut))   # 15
            self.food_name.remove('인문과학')     # 불필요한 요소 제거
            # print(len(self.food_name))  # 15
            
            for i in self.food_nut:
                temp = i.replace('\n', '').replace('\t', '').replace(' ', '').replace('[영양성분]', '').replace('조사년도', '').replace('지역명전국(대표)', '').replace('자료출처식약처영양실태조사', '')     # 불필요한 요소 제거
                self.new_food_nut.append(temp)
            # print(self.new_food_nut)
            
            for i, j, k in zip(self.new_food_nut, self.new_food_gram, self.new_food_kcal):
                temp = i + ',' + j + ',' + k
                self.final_food_nut.append(temp)                # nutrition
            # print(self.final_food_nut)
            
            # print(self.new_food_gram)
            # print(self.new_food_kcal)
            # print(len(self.food_name))
            # print(len(self.new_food_gram))
            # print(len(self.new_food_kcal))
            
            for i, j in enumerate(self.food_name):
                # print('i,j :\n',i, j)
                # print('name :\n',self.food_name[i])
                # print('nutrition :\n',self.food_nut[i])
                self.dict[self.food_name[i]] = self.final_food_nut[i]
            driver.close()
        food_ls = []
        unique_ls = [] # 유니크 값을 확인하기 위한 배열
        for key, value in self.dict.items():
            nut_tr = self.dict[key].split('-')[:-1]
            nut_tr = ' '.join(nut_tr).split()
            print('nut_tr', nut_tr)
            kal_tr = self.dict[key].split('-')[-1].split(',')
            kal_tr = [x.replace(' ', ':') for x in kal_tr]
            print('kal_tr', kal_tr)
            ls = nut_tr[:] + kal_tr
            print('ls', ls)
            new_dict = {sub.split(":")[0]: sub.split(":")[1] for sub in ls[:]}
            new_dict.update({'음식명' : key})
            print('new_dict',new_dict)
            unique_ls.append(list(new_dict.keys()))
            unique_value = ['나트륨', '포화지방산', '당류', '음식명', '1회제공량', '지방', '콜레스테롤', '탄수화물', '단백질', '트랜스지방', '칼로리']
            for i, j in enumerate(unique_value):
                print('ㅐㅐ', list(new_dict.keys()))
                if (j in list(new_dict.keys())) == False:
                    new_dict.update({j : '0g'})

            food_ls.append(new_dict)

        unique_ls = list(chain.from_iterable(unique_ls)) # 2d -> 1d
        test = set(unique_ls) # 유니크 값 출력
        # print('test', test)
        for i in food_ls:
            print('testtest',i)
        
        food = pd.DataFrame([i for i in food_ls], columns=['음식명', '나트륨', '포화지방산', '당류', '1회제공량', '지방', '콜레스테롤', '탄수화물', '단백질', '트랜스지방', '칼로리'])
    
        food.to_csv('food.csv', index=False)
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
        nut.scrap_name()

Nutrition.main()