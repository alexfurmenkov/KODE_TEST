import requests
from bs4 import BeautifulSoup
import mailscript
from subscriber import Subscriber


class App:
    email = ''

    # функция, которая следит за изменением как min_price, так и max_price
    @staticmethod
    def send_mail_both(price, ticker_name, max_price, min_price):
        y = 0  # нужна для получения значения цены
        for i in price:
            y = float(i)
            subj = f'Change of the ticker {ticker_name}'
            if y > max_price:
                msge = f'Current price of the ticker {ticker_name} is now {y} and it is higher than the maximum price'
                mailscript.send_email(subj, msge)
            elif y < min_price:
                msge = f'Current price of the ticker {ticker_name} is now {y} and it is lower than the minimum price'
                mailscript.send_email(subj, msge)

    # функция, которая следит за изменением только max_price
    @staticmethod
    def send_mail_maximum(price, ticker_name, max_price):
        y = 0  # нужна для получения значения цены
        for i in price:
            y = float(i)
            subj = f'Change of the ticker {ticker_name}'
            if y > float(max_price):
                msge = f'Current price of the ticker {ticker_name} is now {y} and it is higher than the maximum price'
                mailscript.send_email(subj, msge)

    # функция, которая следит за изменением только min_price
    @staticmethod
    def send_mail_minimum(price, ticker_name, min_price):
        y = 0  # нужна для получения значения цены
        for i in price:
            y = float(i)
            subj = f'Change of the ticker {ticker_name}'
            if y < float(min_price):
                msge = f'Current price of the ticker {ticker_name} is now {y} and it is lower than the minimum price'
                mailscript.send_email(subj, msge)

    @staticmethod
    def setEmail(self):
        self.email = Subscriber.getSubscribers()['email']

    @staticmethod
    def run():
        try:
            while True:
                source = requests.get('https://finance.yahoo.com/trending-tickers').text
                soup = BeautifulSoup(source, 'lxml')

                ticker_name = Subscriber.getSubscribers()['ticker']
                max_price = Subscriber.getSubscribers()['max_price']
                min_price = Subscriber.getSubscribers()['min_price']
                App.setEmail(App)

                # Если подписка на один тикер
                if type(ticker_name) == str and (type(max_price) == int or type(max_price) == float) and (
                        type(min_price) == int or type(min_price == float)):
                    max_price = float(Subscriber.getSubscribers()['max_price'])
                    min_price = float(Subscriber.getSubscribers()['min_price'])

                    ticker_search = f'/quote/{ticker_name}?p={ticker_name}'
                    ticker_find = soup.find('a', href=ticker_search)
                    parent = ticker_find.parent.parent
                    price = parent.find('td', class_='data-col2 Ta(end) Pstart(20px)')

                    # Функция отправки письма. Если использовать другую функцию (send_mail_minimum или send_mail_maximum),
                    # то получим подписку на изменение только min_price или max_price.
                    # Сейчас подписка на два параметра сразу.
                    App.send_mail_both(price, ticker_name, max_price, min_price)

                # Если подписка на несколько тикеров
                elif type(ticker_name) == list and type(max_price) == list and type(min_price) == list:
                    assert len(ticker_name) <= 5
                    ticker_list = []
                    max_price_list = []
                    min_price_list = []
                    for element_ticker in ticker_name:
                        ticker_list.append(element_ticker)
                    for max_element in max_price:
                        max_price_list.append(max_element)
                    for min_element in min_price:
                        min_price_list.append(min_element)

                    for tl_element in ticker_list:
                        if tl_element == ticker_list[0]:
                            max_price = max_price_list[0]
                            min_price = min_price_list[0]
                        elif tl_element == ticker_list[1]:
                            max_price = max_price_list[1]
                            min_price = min_price_list[1]
                        elif tl_element == ticker_list[2]:
                            max_price = max_price_list[2]
                            min_price = min_price_list[2]
                        elif tl_element == ticker_list[3]:
                            max_price = max_price_list[3]
                            min_price = min_price_list[3]
                        elif tl_element == ticker_list[4]:
                            max_price = max_price_list[4]
                            min_price = min_price_list[4]

                        ticker_search = f'/quote/{tl_element}?p={tl_element}'
                        ticker_find = soup.find('a', href=ticker_search)
                        parent = ticker_find.parent.parent
                        price = parent.find('td', class_='data-col2 Ta(end) Pstart(20px)')

                        # Функция отправки письма. Если использовать другую функцию
                        # (send_mail_minimum или send_mail_maximum), то получим подписку только на min_price или max_price.
                        # Сейчас подписка на два параметра сразу.
                        App.send_mail_both(price, tl_element, max_price, min_price)
        except:
            print('Подписка удалена')


App.run()
