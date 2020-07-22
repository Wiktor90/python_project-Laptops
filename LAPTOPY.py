# -*- coding: utf-8 -*-
import functools
import datetime
import csv,os,sys

#--------------------------------------
# PART I - LOGIC AND FUNCTIONS
#--------------------------------------

def Wrapper_with_Logs(activity, path):
    def Function_with_wrapper(func):
        def Wrapper(*args, **kwargs):
            with open(path,'a') as f:
                f.write(25*'-' + '\n')
                f.write('Function: {}, Activity: {}, time: {}\n'.format(func.__name__,activity,datetime.datetime.now().isoformat()))
                f.write('Following items were used:\n')
                f.write(' '.join('{}'.format(x) for x in args))
                f.write('\n')
                f.write(25*'-')
            result = func(*args, **kwargs)
            return result
        return Wrapper
    return Function_with_wrapper


def path_creator(filename):    
    os.getcwd()
    try:
        os.makedirs('Laptops_log')
    except FileExistsError:
        pass

    temp_path = os.path.join(os.getcwd(),'Laptops_log')
    end_path = os.path.join(temp_path, filename)
    return end_path


class Laptop:

    @classmethod
    def export_to_csv(cls,path):
        with open(path, 'w') as f:
            writer = csv.writer(f,delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['name', 'screen', 'parameters', 'IsOnSale', 'price'])
            for i in cls.items:
                writer.writerow([i.name, i.screen, i.parameters, i._Laptop__IsOnSale, i._Laptop__price])
        print('Current list was successfuly exported to the CSV file: {}'.format(path))

    @classmethod
    def item_list(cls):
        print('CURRENT LAPTOP LIST:')
        print('-'*26)
        for n,i in enumerate(cls.items):
            print('| Position {:2d} - {:8s} |'.format(n+1,i.name))
        print('-'*26)

    @classmethod
    def promotion_list(cls):
        print('CURRENT PROMOTION LIST:')
        print('-'*26)
        for n,i in enumerate(cls.promotion):
            print('| Position {:2d} - {:8s} |'.format(n+1,i))
        print('-'*26)

    @classmethod
    def Show_Laptop_List(cls, lap_list):
        for n,i in enumerate((lap_list),1):
            cls.Set_Price(i)
            print('Positon:   {}'.format(n))
            cls.Get_Info(i)

    items = []
    promotion = ['dell']

    def __init__(self, name, screen, parameters, IsOnSale, price):
        self.name = name
        self.screen = screen
        self.parameters = parameters.copy()
        self.__IsOnSale = IsOnSale
        self.__price = price
        self.items.append(self)

    def Get_Info(self):
        print('Model:      {}'.format(self.name))
        print('Screen:     {}[cal]'.format(self.screen))
        print('Parameters:')
        for par in self.parameters:
            print('\t{}'.format(par))
        print('On Sale:    {}'.format(self.__IsOnSale))
        print('Regular Pr: {} PLN'.format(self.__price))
        print('Promotion:  {} PLN'.format(self.Set_Price()))
        print('-'*25)
    
    def __str__(self):
        return 'Product {}'.format(self.name)

    def add_parameters(self,parameters):
        self.parameters.append(parameters)
    
    def remove_parameters(self,parameters):
        self.parameters.remove(parameters)

    @Wrapper_with_Logs('Add_to_Promotion', path_creator('promotion_logs.txt'))
    def Add_Item_to_promotion(self):
        self.promotion.append(self.name.lower())
        return self.promotion

    @property
    def IsOnSale(self):
        return self.__IsOnSale

    @IsOnSale.setter
    @Wrapper_with_Logs('Change_Sale_Status', path_creator('sale_logs.txt'))
    def IsOnSale(self, newStatus):
        if self.name.lower() in self.promotion:
            self.__IsOnSale = newStatus
        else:
            print('Cannot change status IsOnSale. Sale valid only for{}'.format([i for i in self.promotion]))

    def Set_Price(self):
        if self.__IsOnSale == True and self.name.lower() in self.promotion:
            prom_price = round((self.__price * 0.95),2)
        else:
            return self.__price
        return prom_price

    @Wrapper_with_Logs('Delete_Obj', path_creator('delete_logs.txt'))
    def remove_item(self):
        self.items.remove(self)

lap_01 = Laptop('DELL',13.3,['Intel Core i5-8250U','RAM[GB]:8','SSD[GB]:256','Intel UHD Graphics 620','Windows 10'],True,3499)
lap_02 = Laptop('ASUS',14,['Intel Core i3-8145U','RAM[GB]:4','SSD[GB]:256','Intel UHD Graphics 620','Windows 10 Home'],False,2257)

#--------------------------------------
# PART II - CONSOLE INTERFACE
#--------------------------------------

@Wrapper_with_Logs('Create_New_Obj', path_creator('create_logs.txt'))
def Create_Obj():
    while True:
        choice = input('Do you want to add new object (Y/N): ')
        if choice.lower() == 'y':
            name = input('Brand name: ')
            screen = input('Screen[cal]: ')
            parameters = []
            
            while True:
                choice = input('Press (Y/N) to add parameter: ')
                if choice.lower() == 'y':
                    parameter = input('Add parameter: ')
                    parameters.append(parameter)
                else:
                    break
            choice = input('Is on sale? Press True or False (T/F): ')

            if choice.lower() == 't':
                IsOnSale = True
            else:
                IsOnSale = False
            try:
                price = float(input('Price: '))
            except ValueError:
                input('Error related to price: Invalid input! PRESS ENTER AND TRY AGAIN: ')
                continue
            Laptop(name, screen, parameters, IsOnSale, price)
        else:
            break
    
def Interface():
    option = [
        'PRESS NUMBER TO CHOOSE THE ACTION:',
        '\t1- CREATE NEW LAPTOP',
        '\t2- ADD/REMOVE PARAMETER',
        '\t3- ADD/REMOVE LAPTOP FROM PROMOTION',
        '\t4- DELETE LAPTOP',
        '\t5- SHOW CURRENT LAPTOP LISTS',
        '\t6- EXPORT CURRENT LIST TO CSV',
        '\t7- QUIT']
    print('-'*45)
    for line in option:
        if line == option[0]:
            print('| {:42s} |'.format(line))
        else:
            print('| {:37s} |'.format(line))
    print('-'*45)
    User_action()

def User_action():
    action = input('PRESS: ')
    if action =='1':
        Create_Obj()
        return_to_menu()

    elif action == '2':
        ADD_OR_REM_PARAMETER()

    elif  action == '3':
        ADD_OR_REM_FROM_PROM()

    elif action == '4':
        DELETE_LAPTOP()

    elif action == '5':
        SHOW_CURRENT_LAPTOP_LISTS()

    elif action == '6':
        Laptop.export_to_csv(path_creator('Laptop_list.csv'))
        input('PRESS ENTER to continue: ')
        return_to_menu()

    elif action =='7':
        QUIT()
    else:
        return_to_menu()

def return_to_menu():
    os.system('cls')
    Interface()

def position(base_list, kind):
    while True:
        try:
            position = int(input('Provide POSITION NUMBER of Laptop from current {} list: '.format(kind)))
            if position <= len(base_list):
                return base_list[position-1]
            else:
                input('Error: POSITION NUMBER out of range! PRESS ENTER AND TRY AGAIN! ')
                continue
        except ValueError:
            input('Error: Invalid input! PRESS ENTER AND TRY AGAIN: ')
            continue

def ADD_OR_REM_PARAMETER():
    try:
        choice = input('Choose action: ADD/REMOVE parameter. PRESS (A/R) or ENTER to continue: ')
        upadate_parameter = []
        if choice.lower() == 'a':

            Laptop.item_list()
            pos_item = position(Laptop.items,'LAPTOP')
            count = int(input('How many parameters do you want to add(ENTER NUMBER): '))
            
            for i in range(count):
                i = input('parameter: ')
                pos_item.add_parameters(i)
            upadate_parameter.append(pos_item) 

        elif choice.lower() == 'r':
            Laptop.item_list()
            pos_item = position(Laptop.items,'LAPTOP')
            for n,p in enumerate((pos_item.parameters),1):
                print(n,p)
            try:
                pos_parameter = int(input('Provide position of prameter to remove: '))
                pos_item.remove_parameters(pos_item.parameters[pos_parameter-1])
                upadate_parameter.append(pos_item)
            except IndexError:
                input('Error: Value out of range! PRESS ENTER AND TRY AGAIN: ')
                return_to_menu()
        else:
            return_to_menu()
    except ValueError:
            input('Error: Invalid input! PRESS ENTER AND TRY AGAIN: ')
            return_to_menu()

    Laptop.Show_Laptop_List(upadate_parameter)
    input('UPDATED. PRESS ENTER to continue: ')    
    return_to_menu()
    
def ADD_OR_REM_FROM_PROM():
    Laptop.promotion_list()
    Laptop.item_list()
    choice = input('Choose: ADD/REMOVE. PRESS (A/R) or ENTER to continue: ')

    if choice.lower() == 'a':
        pos_item = position(Laptop.items, 'LAPTOP')

        if pos_item.name.lower() in Laptop.promotion:
            input('Laptop is already in promotion. PRESS ENTER to continue:: ')
            
        else:
            Laptop.Add_Item_to_promotion(pos_item)
            pos_item.IsOnSale = True
            Laptop.promotion_list()
            input('UPDATED. PRESS ENTER to continue: ')

    elif choice.lower() == 'r':
        pos_item = position(Laptop.items, 'LAPTOP')
        if pos_item.name.lower() in Laptop.promotion:
            Laptop.promotion.remove(pos_item.name.lower())
            pos_item.IsOnSale = False
            Laptop.promotion_list()
            input('UPDATED. PRESS ENTER to continue: ')
        
        else:
            input('Laptop is NOT in promotion. You can not remove it. PRESS ENTER to continue:: ')
    else:
        pass
    return_to_menu()

def DELETE_LAPTOP():
    Laptop.item_list()
    pos_item = position(Laptop.items, 'LAPTOP')
    choice = input('Do you want to delete {} ? PRESS (Y/N): '.format(pos_item.name))

    if choice.lower() == 'y':
        if pos_item.name.lower() in Laptop.promotion:
            Laptop.promotion.remove(pos_item.name.lower())

        Laptop.remove_item(pos_item)
        Laptop.promotion_list()
        Laptop.item_list()
        input('UPDATED. PRESS ENTER to continue: ')
    else:
        pass
    return_to_menu()

def SHOW_CURRENT_LAPTOP_LISTS():
    Laptop.Show_Laptop_List(Laptop.items)
    Laptop.promotion_list()
    input('RETURN TO MENU - PRESS ENTER:')
    return_to_menu()

def QUIT():
    sys.exit(1)

Interface()