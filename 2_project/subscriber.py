import json


class Subscriber:
    subscribers_list = []
    subscriber_data = []

    @staticmethod
    def getSubscribers():
        # чтение файла со значениями и запись их в список
        with open("subscribers.json", "r") as file:
            Subscriber.subscriber_data = json.load(file)
        return Subscriber.subscriber_data

    @staticmethod
    def addSubscriber(info):
        Subscriber.subscribers_list.append(info)
        print(Subscriber.subscribers_list)

        # Запись в файл запроса
        file = open("subscribers.json", "w")
        for subscr_info in Subscriber.subscribers_list:
            file.write(json.dumps(subscr_info))
        file.close()

    @staticmethod
    def delSubcriber(delete_data):
        with open("subscribers.json", "r+") as file:
            file_data = json.load(file)
            print(file_data)
            print(delete_data)

            if file_data == delete_data:
                file.seek(0)
                file.truncate()
            else:
                if delete_data['ticker'] in file_data['ticker']:
                    del_ticker = delete_data['ticker']
                    f_ticker = file_data['ticker']
                    if del_ticker in f_ticker:
                        z = f_ticker.index(del_ticker)
                        del f_ticker[z]

                if delete_data['max_price'] in file_data['max_price']:
                    del_ticker = delete_data['max_price']
                    f_ticker = file_data['max_price']
                    if del_ticker in f_ticker:
                        z = f_ticker.index(del_ticker)
                        del f_ticker[z]

                if delete_data['min_price'] in file_data['min_price']:
                    del_ticker = delete_data['min_price']
                    f_ticker = file_data['min_price']
                    if del_ticker in f_ticker:
                        z = f_ticker.index(del_ticker)
                        del f_ticker[z]
                file.seek(0)
                file.truncate()
                file.write(json.dumps(file_data))


