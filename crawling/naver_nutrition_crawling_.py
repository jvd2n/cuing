import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import chain


class Nutrition(object):
    # url = 'https://terms.naver.com/list.naver?cid=59320&categoryId=59320'
    url = None
    driver_path = 'C:/chromedriver'
    dict = {}
    df = None
    food_name = []
    food_nut = []
    new_food_nut = []
    new_food_gram = []
    new_food_kcal = []
    final_food_nut = []
    page = 3

    def scrap_name(self):
        for i in range(1, self.page):
            # 1 페이지부터 3페치지 차례대로 링크로 이동
            self.url = f'https://terms.naver.com/list.naver?cid=59320&categoryId=59320&page={i}'
            driver = webdriver.Chrome(self.driver_path)
            driver.get(self.url)
            all_div = BeautifulSoup(driver.page_source, 'html.parser')
            ls1 = all_div.find_all("div", {"class": "subject"})
            for i in ls1:
                # 현재 페이지에 보이는 음식 이름 하나씩 가져오기
                self.food_name.append(i.find('a').text)
            # print(self.food_name)

            ls2 = all_div.find_all("p", {"class": "desc __ellipsis"})
            for i in ls2:
                # 현재 페이지에 보이는 영양성분 정보(탄수화물, 단백질, 지방, 당류, 나트륨 등) 하나씩 가져오기
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

            self.food_name.remove('인문과학')     # 불필요한 요소 제거
            # print(len(self.food_name))  # 15

            for i in self.food_nut:
                temp = i.replace('\n', '').replace('\t', '').replace(' ', '').replace('[영양성분]', '').replace(
                    '조사년도', '').replace('지역명전국(대표)', '').replace('자료출처식약처영양실태조사', '')     # 불필요한 요소 제거
                self.new_food_nut.append(temp)
            # print(self.new_food_nut)

            for i, j, k in zip(self.new_food_nut, self.new_food_gram, self.new_food_kcal):
                temp = i + ',' + j + ',' + k
                # nutrition 칼로리, 1회 제공량, 영양성분을 하나의 변수로 합침
                self.final_food_nut.append(temp)

            for i, j in enumerate(self.food_name):
                # 음식 이름과 영양성분을 병합해서 딕셔너리로 만듬 {'고구마': '- 탄수화물...'}
                self.dict[self.food_name[i]] = self.final_food_nut[i]
            driver.close()
        food_ls = []
        unique_ls = []  # 유니크 값을 확인하기 위한 배열

        for key, value in self.dict.items():  # 크롤링한 음식 가지수만큼 반복
            # 1회 제공량이나 칼로리부터는 '-'문자열이 없고, ','로 구분 돼서 그 전까지 분리 ['', '탄수화물:23g', '단백질:123g']
            nut_tr = self.dict[key].split('-')[:-1]
            nut_tr = ' '.join(nut_tr).split()  # 앞 공백 요소 제거
            print('nut_tr', nut_tr)
            # 1회 제공량, 칼로리는 ','로 각 요소가 분리돼서 따로 분리
            kal_tr = self.dict[key].split('-')[-1].split(',')
            # 제공량, 칼로리는 해당 영양성분에 대한 내용이 띄어쓰기로 분류되어있어서 한 번에 바꾸기 위해 replace시켜줌
            kal_tr = [x.replace(' ', ':') for x in kal_tr]
            print('kal_tr', kal_tr)
            ls = nut_tr[:] + kal_tr  # 둘이 합침
            print('ls', ls)
            # {'탄수화물':5g, '단백질':4g} 처럼 모든 영양성분을 키와 값으로 나눔
            new_dict = {sub.split(":")[0]: sub.split(":")[1] for sub in ls[:]}
            new_dict.update({'음식명': key})  # 음식명도 영양성분 dictioanry와 합침
            print('new_dict', new_dict)
            # 유니크 값을 확인하기 위한 배열에 키값을 추가함.
            unique_ls.append(list(new_dict.keys()))
            unique_value = ['나트륨', '포화지방산', '당류', '음식명', '1회제공량', '지방',
                            '콜레스테롤', '탄수화물', '단백질', '트랜스지방', '칼로리']  # 크롤링한 데이터에서의 유니크값 들
            for i, j in enumerate(unique_value):  # 유니크값만큼 돌아서 비교함.
                if (j in list(new_dict.keys())) == False:  # 영양성분이 존재하지 않으면 추가
                    # 데이터프레임으로 만들기 위해 해당성분에 없는 영양성분은 0g으로 추가
                    new_dict.update({j: '0g'})

            food_ls.append(new_dict)  # 만들어진 음식 dictionary를 하나씩 리스트 자료형에 추가

        # unique_ls = list(chain.from_iterable(unique_ls)) # 2d -> 1d
        # test = set(unique_ls) # 유니크 값 출력
        # print('test', test)

        food = pd.DataFrame([i for i in food_ls], columns=['음식명', '나트륨', '포화지방산', '당류',
                            '1회제공량', '지방', '콜레스테롤', '탄수화물', '단백질', '트랜스지방', '칼로리'])  # dataframe 자료형으로 변환

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
