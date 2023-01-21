import os
from cities import * # модуль cities с функциями

path_dir = os.path.dirname(__file__)
path_file =  os.path.join(path_dir, 'goroda.csv')
nas_punkt_df = pd.read_csv(path_file)
goroda_df = nas_punkt_df[(nas_punkt_df['Тип города'] == 'г') | (nas_punkt_df['Тип региона'] == 'г')]
goroda_df = goroda_df[goroda_df['Тип н/п'] != 'г']
POP = 200000
big_cities_df = goroda_df[goroda_df['Население'] > POP] # Оставляем города с населением > POP

class City():
    DF = big_cities_df
    def __init__(self,i):
        self.i = i
    
    @property
    def name(self):
        return city_region_by_index(City.DF, self.i)
    
    def __str__(self):
        return self.name

class Property():
    """Собственность: товар или фура"""
    def __init__(self, city, cost):
        self.bought = city # где куплен
        self.cost = cost # стоимость в тыс. руб.

class Commodity(Property):
    """Абстрактный товар без названия"""
    PRICE = 1 # цена при покупке тыс. руб./кг.
    def __init__(self, city, mass):
        cost = mass * Commodity.PRICE
        super().__init__(city, cost)
        self.mass = mass
    
    def __str__(self):
        str1 = 'Товар весом ' + str(self.mass) + ' кг.\t'
        str2 = 'Куплен в городе ' + self.bought.name + ' за ' + str(self.cost) + ' тыс. рублей'
        return  str1 + str2
    
    def sell_cost(self, city):
        """Товар дорожает в зависимости от расстояния между точкой покупки и продажи"""
        i = city.i
        j = self.bought.i
        d = dist(City.DF, i, j)
        c = self.cost
        COEF = 1/1000 # коэффициэнт подорожания в тыс руб./(км. * кг)
        return c + COEF * d


class Truck(Property):
    """Абстрактная фура с абстрактным номером типа"""
    
    # Типы фур (с прицепом) по цене (тыс. руб.), грузоподъёмности (тонн), расходу топлива (литров дизеля на 100 км.):
    TRUCKS = [(2000, 2, 11), (4500, 6, 20), (7000, 13, 35)]
    
    @staticmethod
    def is_correct_type(truck_type):
        return truck_type in range(len(Truck.TRUCKS))
    
    def __init__(self, city, truck_type):
        if not Truck.is_correct_type(truck_type):
            return None
        cost, max_mass_t, consumption = Truck.TRUCKS[truck_type]
        super().__init__(city, cost)
        self.max_mass = max_mass_t * 1000
        self.consumption = consumption
    
    def __str__(self):
        str1 = 'Фура грузоподъёмностью ' + str(self.mass) + ' кг.\n'
        str2 = 'Можно продать за ' + str(self.cost) + ' тыс. рублей.\n'
        return  str1 + str2 
    
    @property
    def sell_cost(self):
        """Подержаная фура стоит дешевле"""
        return self.cost * 0.7

class Player():
    def __init__(self, city, money = 0):
        self.city = city
        self.money = money
        self.commodity = []
        self.truck = None
    
    @property
    def mass_in_truck(self):
        commodity_mass = 0
        for comm in self.commodity:
            commodity_mass += comm.mass
        return commodity_mass

    def buy_truck(self, truck_type):
        if self.truck == None and Truck.is_correct_type(truck_type):
            truck = Truck(self.city, truck_type)
            self.truck = truck
            self.money -= truck.cost
        elif not Truck.is_correct_type(truck_type):
            print('Неверный тип фуры')
        else:
            print('Можно иметь только одну фуру.')
    
    def buy_commodity(self, mass):
        commodity_mass = self.mass_in_truck
        if commodity_mass + mass > self.truck.max_mass:
            print('Не влезает. Купите фуру побольше.')
        else:
            c = Commodity(self.city, mass)
            self.commodity.append(c)
            self.money -= c.cost
    
    def sell_truck(self):
        if self.truck:
            truck = self.truck
            self.money += truck.sell_cost
            self.truck = None
        else:
            print('У Вас нет фуры.')
    
    def sell_commodity(self, i):
        cc = self.commodity
        if i in range(len(cc)):
            c = cc.pop(i)
            self.money += c.sell_cost(self.city)
        else:
            print(f'Товар с индексом {i} отсутствует.')
    
    def change(self):
        if self.truck:
            print('\nСтоимость старой фуры:', self.truck.sell_cost)
        print('\nВыберете новую:')
        for k in range(len(Truck.TRUCKS)):
            new = Truck.TRUCKS[k]
            print(f'{k} \u2014 Цена: {new[0]} тыс. руб., грузоподъёмность: {new[1]} тонн, расход: {new[2]} литров на 100 км.')
        print('c \u2014 отмена\n')
        while True:
            choice = input('Ваш выбор: ')
            if choice:
                ch = choice.lower()[0]
            else:
                ch = 'c'
            if ch == 'c':
                break
            try:
                k = int(choice)
            except:
                continue
            if k in range(len(Truck.TRUCKS)):
                break
        
        if k in range(len(Truck.TRUCKS)):
            if self.truck:
                self.sell_truck()
            self.buy_truck(k)

    def buy(self):
        mmax = self.truck.max_mass - self.mass_in_truck
        if mmax <= 0:
            print('\nВ фуре нет места\n')
            return None
        print('\nЦена товара:', Commodity.PRICE)
        print(f'\nВ фуре осталось место для {mmax} кг.')
        while True:
            try:
                mass = int(input('\nСколько кг. товара Вы хотите купить? '))
            except:
                continue
            if mass > mmax:
                print('\nСтолько не влезет')
                continue
            break
        self.buy_commodity(mass)
    
    def sell(self):
        cc = self.commodity
        l = len(cc)
        if l ==0:
            print('\nУ вас нет товаров\n')
            return None
        print()
        for k in range(l):
            c = cc[k]
            print(f'{k} \u2014 {c} Можно продать за {c.sell_cost(self.city)} тыс. руб.')
        print('a \u2014 продать весь товар')
        print('c \u2014 отмена')
        while True:
            choice = input('Ваш выбор: ')
            if choice:
                ch = choice.lower()[0]
            else:
                ch = 'c'
            if ch in ['c', 'a']:
                break
            try:
                k = int(choice)
            except:
                continue
            if k in range(l):
                break
        if ch == 'c':
            return None
        if ch == 'a':
            for j in range(l):
                self.sell_commodity(l-1-j)
        else:
            self.sell_commodity(k)

    def move(self, n):
        if self.truck == None:
            print('\nСначала купите фуру.\n')
            return None
        DIESEL_PRICE = 56 / 1000 # тыс. руб. / литр
        df = City.DF
        i = self.city.i
        d = 0
        print('Текущий город {city_region_by_index(df,i)}')
        print('\nВыберете город:')
        while True:
            nearst = nearst_cities(df, i, n)
            for k in range(n):
                j = nearst[k]
                print(f'{k} \u2014 {city_region_by_index(df,j)}: ({coords_by_ind(df, j)[0]:.2f}, {coords_by_ind(df, j)[1]:.2f})')
            
            print(f'r \u2014 остаться\n')
            while True:
                choice = input('Ваш выбор: ')
                if choice:
                    ch = choice.lower()[0]
                else:
                    ch = 'r'
                if ch == 'r':
                    break
                try:
                    k = int(choice)
                except:
                    continue
                if k in range(n):
                    break
        
            if choice == 'r':
                break
        
            j = nearst[k]
            d += dist(City.DF, i, j)
            i = j
        
        self.city = City(i)
        diesel_cost = (d / 100) * self.truck.consumption * DIESEL_PRICE
        self.money -= diesel_cost
        print(f'\nНа дизель ушло {diesel_cost:.3f} тыс. руб.\n')


class Game():
    def __init__(self, city_name):
        i = city_indices(City.DF, city_name)[0]
        city = City(i)
        self.player = Player(city)
    
    def play(self, n):
        player = self.player
        print('Вы торговец-дальнобойщик.')
        print('\nВы находитесь в городе', self.player.city.name)
        while self.player.truck == None:
            print('\nСначала надо купить фуру')
            player.change()
        while True:
            print('\nВы находитесь в городе', player.city.name)
            print(f'У Вас {player.money:.3f} тыс. рублей, фура вместимостью {player.truck.max_mass} кг. и {len(player.commodity)} товаров общим весом {player.mass_in_truck} кг.\n')
            print()
            print(f'm \u2014 отправиться в другой город')
            print(f's \u2014 продать товар')
            print(f'b \u2014 купить товар')
            print(f'c \u2014 поменять фуру')
            print(f'q \u2014 выйти')
            while True:
                choice = input('\nВаш выбор: ')
                if choice:
                    choice = choice.lower()[0]
                else:
                    continue
                if choice not in ['m', 's', 'b', 'c', 'q']:
                    continue
                elif choice == 'm':
                    player.move(n)
                elif choice == 's':
                    player.sell()
                elif choice == 'b':
                    player.buy()
                elif choice == 'c':
                    player.change()
                break
            
            if choice == 'q':
                break



#city_name = 'Москва' # Начальный город
#game = Game(city_name)
#game.play(10)

def main():
    while True:
        N = 10 # Количество ближайший городов
        city_name = 'Москва' # Начальный город
        game = Game(city_name)
        game.play(N)
        while True:
            resp = input('Хотите ещё сыграть? (y/n): ')
            if resp == '':
                continue
            char = resp[0].lower()
            if char in ['y', 'д', 'n', 'н']:
                break

        if char in ['n', 'н']:
            break
    
    print('Пока!')

if __name__ == '__main__':
    main()

