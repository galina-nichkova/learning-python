import os
from bs4 import BeautifulSoup
import requests
from requests.exceptions import HTTPError
import sqlite3
import argparse


def get_page_content(page_link):
    #page_link = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/Prenzlauer-Berg-Prenzlauer-Berg
    # /2,00-/-/EURO--800,00?enteredFrom=one_step_search'
    page_response = requests.get(page_link, timeout=5)
    if page_response.status_code != 200:
        raise HTTPError('Received unexpected page response, status code {}.'.format(page_response.status_code))
    else:
        page_content = BeautifulSoup(page_response.content, "html.parser")
        return page_content


def get_data_ids(page_content):
    if page_content is None:
        raise TypeError('Page content is None.')
    else:
        data_ids = page_content.find_all('li', attrs={'class': 'result-list__listing'})
        i = 0
        data_ids_list = []
        while i < len(data_ids):
            data_ids_list.append(data_ids[i]['data-id'])
            i = i + 1
        return data_ids_list


def get_final_list(data_ids_list, page_content):
    if len(data_ids_list) == 0:
        raise ValueError('No data ids in the input.')

    if page_content is None:
        raise TypeError('Page content is None.')

    all_data = []
    for n in data_ids_list:
        address = (page_content
                   .find('button', attrs={'title': 'Auf der Karte anzeigen', 'data-result-id': '{}'
                   .format(n)}).div.string)
        price = (page_content
                     .find('li', attrs={'data-id':'{}'.format(n)})
                     .find('dt', string='Kaltmiete')
                     .find_previous_sibling('dd')
                     .string)
        living_space = (page_content
                        .find('li', attrs={'data-id':'{}'.format(n)})
                        .find('dt', string='Wohnfläche')
                        .find_previous_sibling('dd').string)

        result_dict = {'id': n, 'address': address, 'price': price, 'living_space': living_space}
        all_data.append(result_dict)
    return all_data


def write_to_database(all_data):
    working_dr = os.getcwd()
    db_file = os.path.join(working_dr, 'rent_offers.db')
    if os.path.isfile(db_file):
        os.remove(db_file)

    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute('create table if not exists rent_offers(id TEXT, address TEXT, price TEXT, living_space TEXT)')
    for data in all_data:
        values = "'" + data.get('id') + "', '" + data.get('address') + "', '" + \
                 data.get('price') + "', '" + data.get('living_space') + "'"
        insert_statement = 'insert into rent_offers values({})'.format(values)
        print(insert_statement)
        c.execute(insert_statement)
        conn.commit()
    conn.close()
    return 'Done.'


def main():
    default_link = 'https://www.immobilienscout24.de/Suche/S-T/Wohnung-Miete/Berlin/Berlin/Prenzlauer-Berg-' \
                   'Prenzlauer-Berg/2,00-/-/EURO--800,00?enteredFrom=one_step_search'
    parser = argparse.ArgumentParser()
    parser.add_argument("--page_link", help="Please enter the link of the page you want to parse. If not specified, "
                                            "a default link will be used.")
    page_link = parser.parse_args()
    content = get_page_content(page_link=default_link)
    data_ids = get_data_ids(content)
    final_dictionary = get_final_list(data_ids, content)
    write_to_database(final_dictionary)


if __name__ == '__main__':
    main()
