from selenium import webdriver
from bs4 import BeautifulSoup
from pandas import DataFrame, concat
from time import sleep

ile_przewijan = 50

# Ustawianie opcji przeglądarki chrome
driver = webdriver.Chrome(
    'C:\\Users\\Kacper\\PycharmProjects\\Bitcoin_price_3m\\venv\\Lib\\site-packages\\selenium\\webdriver\\chrome\\chromedriver.exe')

# wyświetlenie strony w przeglądarce
driver.get('https://bitcoin.pl/')

# tablice na przechowywanie dataFrame'ów
df = ['null'] * ile_przewijan
# połączone dataFrame'y
combined_df = []

for z in range(ile_przewijan):

    # łączy BS4 z webdriver'em
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    sleep(1)

    # szukanie ciał artykółów
    body = soup.find('div', attrs={'class': 'jeg_posts jeg_load_more_flag'})
    table = body.find_all('div', {'class': 'jeg_postblock_content'})

    # tworzy szkielet dataFrame
    columns = ['data', 'tytul']
    df[z] = DataFrame(index=range(0, (len(table))), columns=columns)

    # wypełnia dataFrame
    row = 0
    for line in table:
        # data
        df[z].iloc[row, 0] = line.find('div', attrs={'class': 'jeg_meta_date'}).text

        # tytuł
        df[z].iloc[row, 1] = line.find('h3', attrs={'class': 'jeg_post_title'}).text.lstrip().rstrip()

        row += 1
    combined_df.append(df[z])

    # szukanie miejsca do którego ma być przewijana strona
    element = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div[1]/div/div[5]/div/div[1]/div/div/div[2]')

    # przewijanie strony
    element.location_once_scrolled_into_view

    # klikanie nastepnej strony
    nastepna = driver.find_element_by_xpath(
        '/html/body/div[2]/div[6]/div/div[1]/div/div[5]/div/div[1]/div/div/div[2]/div[2]/a[2]').click()
    sleep(3)

# łączenie wszystkich dataFrame'ów w jeden duży
combined_df = concat(combined_df)

# print(combined_df)

# podaj gdzie zapisać plik csv:
combined_df.to_csv(r'C:\Users\Kacper\Desktop\DATA Science\Nowy folder' + '\\Bitcoin_pl_scrap_WEBDRIVER.csv', encoding='utf-8-sig',
                   index=False)

driver.close()
