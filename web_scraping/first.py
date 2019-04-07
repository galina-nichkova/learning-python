from bs4 import BeautifulSoup
import requests
import pandas as pd

def create_page_content(page_link):
    page_response = requests.get(page_link, timeout=5)
    page_content = BeautifulSoup(page_response.content, "html.parser")



# fetch ids of all single entries
def fetch_entry_ids(page_content):
    '''Find unique ids of entries in the bs4.BeautifulSoup class object
    and pass them into a newly created list

    Keyword arguments:
    page_content -- bs4.BeautifulSoup class object created with html parser
                    from a content of a url get call

    Returns: list'''
    data_ids = page_content.find_all('li', attrs={'class': 'result-list__listing '})
    i = 0
    data_ids_list = []
    while i < len(data_ids):
        data_ids_list.append(data_ids[i]['data-id'])
        i = i + 1
    print(data_ids_list)
    return data_ids_list


# put selected information per entry into a dictionary
def collect_data(page_content, data_ids_list):
    '''Parse address, price, and living space of each entry and pass them
    along with the unique entry id into a newly created list of dictionaries

    Returns: list'''
    all_data = []
    for i, n in data_ids_list:
        address = page_content.find('button',
                                    attrs={'title': 'Auf der Karte anzeigen', 'data-result-id': '{}'.format(n)})
        price = page_content.find('li', attrs={'data-id':'{}'.format(n)}).find('dt', string='Kaltmiete').find_previous_sibling('dd').string
        living_space = page_content.find('li', attrs={'data-id':'{}'.format(n)}).find('dt', string='Wohnfläche').find_previous_sibling('dd').string

        dict = {'id': n, 'address': address, 'price': price, 'living_space': living_space}
        all_data.append(dict)

    out_df = pd.DataFrame(all_data)
    out_df.to_csv(output_file, encoding='utf-8', index=False, header=False)
    return all_data


