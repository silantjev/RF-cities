# gui-версия игры
# с одним обновляющимся окном

from tkinter import *
from cities import * # модуль cities с функциями


class City():
    DF = df_city_load()
    def __init__(self,i):
        self.i = i
    
    @property
    def name(self):
        return city_region_by_index(City.DF, self.i)
    
    def __str__(self):
        return self.name
    
    @staticmethod
    def make_cities():
        """ Создаёт объект City для всех городов из DF """
        cities = dict()
        for i in City.DF.index:
            cities[i] = City(i)
        City.cities = cities


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
        self.max_mass = max_mass_t * 1000 # кг.
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
    def __init__(self, root):
        self.root = root
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
            self.warning('Неверный тип фуры')
        else:
            self.warning('Можно иметь только одну фуру')
    
    def buy_commodity(self, mass):
        commodity_mass = self.mass_in_truck
        if commodity_mass + mass > self.truck.max_mass:
            self.warning('Не влезает. Купите фуру побольше.')
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
            self.warning('У Вас нет фуры.')
    
    def sell_commodity(self, i):
        cc = self.commodity
        if i in range(len(cc)):
            c = cc.pop(i)
            self.money += c.sell_cost(self.city)
        else:
            self.warning(f'Товар с индексом {i} отсутствует.')
    
    def warning(self, message):
        l = Label(self.frame, text=message)
        l.grid()

    def change(self, first_truck_command, menu_command):
        frame = self.frame
        def change_bttn():
            ch = choice.get()
            if ch == None:
                return None
            if self.truck:
                self.sell_truck()
            self.buy_truck(int(ch))
            menu_command()
        def cancel_bttn():
            if self.truck:
                menu_command()
            else:
                first_truck_command()
        if self.truck:
            Label(frame, text=f'Стоимость старой фуры: {self.truck.sell_cost}').grid()
        Label(frame, text='Выберете новую фуру:').grid()
        choice = StringVar(frame)
        choice.set(None)
        for k in range(len(Truck.TRUCKS)):
            new = Truck.TRUCKS[k]
            text = f'{k} \u2014 Цена: {new[0]} тыс. руб., грузоподъёмность: {new[1]} тонн, расход: {new[2]} литров на 100 км.'
            Radiobutton(frame, text=text, variable=choice, value=str(k)).grid()
        if self.truck:
            text = 'Поменять'
        else:
            text = 'Купить'
        Button(frame, text=text, command=change_bttn).grid()
        Button(frame, text='Отмена', command=cancel_bttn).grid()
    def buy(self, next_command):
        frame = self.frame
        def buy_bttn():
            try:
                mass = int(entry.get())
            except:
                self.warning('Введите целое число')
                return None
            if mass > mmax:
                self.warning('Столько не влезет')
                return None
            self.buy_commodity(mass)
            next_command()
        def cancel_bttn():
            next_command()
        mmax = self.truck.max_mass - self.mass_in_truck
        if mmax <= 0:
            self.warning('В фуре нет места')
            return None
        text = f'Цена товара: {Commodity.PRICE}'
        Label(frame, text=text).grid()
        text = f'\nВ фуре осталось место для {mmax} кг.'
        Label(frame, text=text).grid()
        text = 'Сколько кг. товара Вы хотите купить?'
        entry = Entry(frame)
        entry.grid()
        Button(frame, text='Купить', command=buy_bttn).grid()
        Button(frame, text='Отмена', command=cancel_bttn).grid()
    
    def sell(self, next_command):
        frame = self.frame
        def sell_bttn():
            ch = choice.get()
            if ch == '':
                return
            if ch == 'a':
                for j in range(l):
                    self.sell_commodity(l-1-j)
            else:
                k = int(ch)
                self.sell_commodity(k)
            next_command()
        def cancel_bttn():
            next_command()
        cc = self.commodity
        l = len(cc)
        if l ==0:
            text = 'У Вас нет товаров'
            Label(frame, text=text).grid()
            Button(frame, text='OK', command=next_command).grid()
            return None
        choice = StringVar(value='')
        for k in range(l):
            c = cc[k]
            text = f'{c} Можно продать за {c.sell_cost(self.city)} тыс. руб.'
            Radiobutton(frame, text=text, variable=choice, value=str(k)).grid()
        text = 'Продать весь товар'
        Radiobutton(frame, text=text, variable=choice, value='a').grid()    
        Button(frame, text='Продать', command=sell_bttn).grid()
        Button(frame, text='Отмена', command=cancel_bttn).grid()

    def move(self, next_command, n):
        if self.truck == None:
            self.warning('Сначала купите фуру')
            next_command()
            return None
        DIESEL_PRICE = 56 / 1000 # тыс. руб. / литр
        df = City.DF
        self.i = self.city.i
        self.distance = 0
        self.total_distance = 0
        def diesel_cost(d):
            return (d / 100) * self.truck.consumption * DIESEL_PRICE
        def command_move():
            k = choice.get()
            if k == -1:
                return None
            j = nearst[k]
            self.distance = dist(City.DF, self.i, j)
            self.total_distance += self.distance
            self.i = j
            self.frame.destroy()
            self.frame = Frame(self.root)
            self.frame.grid()
            move_step()
        def command_rest():
            self.city = City.cities[self.i]
            self.money -= diesel_cost(self.total_distance) 
            next_command()
        def move_step():
            text = f'Текущий город: {city_region_by_index(df,self.i)}'
            Label(self.frame, text=text).grid()
            text = f'Текущие координаты: ({coords_by_ind(df, self.i)[0]:.2f}, {coords_by_ind(df, self.i)[1]:.2f})'
            Label(self.frame, text=text).grid()
            text = 'Выберете город:'
            Label(self.frame, text=text).grid()
            global nearst
            nearst = nearst_cities(df, self.i, n)
            global choice
            choice = IntVar(self.frame)
            choice.set(-1)
            for k in range(n):
                j = nearst[k]
                text = f'{city_region_by_index(df,j)}: ({coords_by_ind(df, j)[0]:.2f}, {coords_by_ind(df, j)[1]:.2f})'
                Radiobutton(self.frame, text=text, variable=choice, value=k).grid()
            Button(self.frame, text='Поехать', command=command_move).grid()
            Button(self.frame, text='Остаться', command=command_rest).grid()
            if self.distance:
                text = f'Вы проехали {self.distance:.0f} км.'
                Label(self.frame, text=text).grid()
                text = f'На дизель ушло {diesel_cost(self.distance):.3f} тыс. руб.'
                Label(self.frame, text=text).grid()
            if self.total_distance != self.distance:
                text = f'Всего:\n{self.total_distance:.0f} км.\n{diesel_cost(self.total_distance):.3f} тыс. руб.'
                Label(self.frame, text=text).grid()
        move_step()


    def new_window(self, action):
        self.frame.destroy()
        frame = Frame(self.root)
        self.frame = frame
        frame.grid()
        def buy_first_truck():
            self.new_window('first_truck')
        def buy_truck():
            self.new_window('change')
        def to_menu():
            self.new_window('menu')
        def after_move():
            self.new_window('menu')
        if action == 'move':
            self.move(after_move, self.n)
        elif action == 'sell':
            self.sell(to_menu)
        elif action == 'buy':
            self.buy(to_menu)
        elif action == 'change':
            self.change(buy_first_truck, to_menu)
        elif action == 'intro':
            text = 'Вы торговец-дальнобойщик.'
            Label(frame, text=text).grid()
            text = 'Вы находитесь в городе ' + self.city.name
            Label(frame, text=text).grid()
            Button(frame, text='Дальше', command=buy_first_truck).grid()
            Button(frame, text='Выйти из игры', command=self.root.destroy).grid()
        elif action == 'first_truck':
            text = 'Сначала надо купить фуру'
            Label(frame, text=text).grid()
            Button(frame, text='Купить фуру', command=buy_truck).grid()
            Button(frame, text='Выйти из игры', command=self.root.destroy).grid()
        elif action == 'menu':
            self.menu()


    def menu(self):
        frame = self.frame
        text ='Вы находитесь в городе' + self.city.name
        Label(frame, text=text).grid()
        text = f'У Вас {self.money:.3f} тыс. рублей, фура вместимостью {self.truck.max_mass} кг. и {len(self.commodity)} товаров общим весом {self.mass_in_truck} кг.'
        Label(frame, text=text).grid()
        def command_m():
            self.new_window('move')
        Button(frame, text = f'Отправиться в другой город', command=command_m).grid()
        def command_s():
            self.new_window('sell')
        Button(frame, text = f'Продать товар', command=command_s).grid()
        def command_b():
            self.new_window('buy')
        Button(frame, text = f'Купить товар', command=command_b).grid()
        def command_c():
            self.new_window('change')
        Button(frame, text = f'Поменять фуру', command=command_c).grid()
        Button(frame, text='Выйти из игры', command=self.root.destroy).grid()
        

    def game(self, city_name, n=10, money=0):
        i = city_indices(City.DF, city_name)[0]
        self.city = City.cities[i]
        self.n = n
        self.money = money
        self.frame = Frame(self.root)
        self.frame.grid()
        self.new_window('intro')
    


# body

if __name__ == '__main__':
    City.make_cities()
    root = Tk()
    root.title('Game')
    player = Player(root)
    city_name = 'Москва' # Начальный город
    player.game(city_name, n=10, money=10000)
    root.mainloop()

