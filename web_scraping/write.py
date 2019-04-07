from bs4 import BeautifulSoup
import requests
#import pandas as pd


def parse_all_data(page_link):
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")

    data_ids = page_content.find_all('li', attrs={'class': 'result-list__listing '})
    i = 0
    data_ids_list = []
    while i < len(data_ids):
        data_ids_list.append(data_ids[i]['data-id'])
        i = i + 1
    print(data_ids_list)

    all_data = []
    for n in data_ids_list:
        address = page_content.find('button',
                                    attrs={'title': 'Auf der Karte anzeigen', 'data-result-id': '{}'.format(n)}).string
        price = page_content.find('li', attrs={'data-id':'{}'.format(n)}).find('dt', string='Kaltmiete').find_previous_sibling('dd').string
        living_space = page_content.find('li', attrs={'data-id':'{}'.format(n)}).find('dt', string='Wohnfläche').find_previous_sibling('dd').string

        dict = {'id': n, 'address': address, 'price': price, 'living_space': living_space}
        all_data.append(dict)

    return all_data

    #out_df = pd.DataFrame(all_data)
    #out_df.to_csv("output.csv", encoding='utf-8', index=False, header=False)
    #print(all_data)

if __name__ == '__main__':
    page_link = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/Prenzlauer-Berg-Prenzlauer-Berg/2,00-/-/EURO--800,00?enteredFrom=one_step_search'
    parse_all_data(page_link)