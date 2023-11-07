from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dataclasses import dataclass, asdict
import json
from webdriver_manager.chrome import ChromeDriverManager

@dataclass
class Item:
    sport_league: str = ''
    event_date_utc: str = ''
    team1: str = ''
    team2: str = ''
    pitcher: str = ''
    period: str = ''
    line_type: str = ''
    price: str = ''
    side: str = ''
    team: str = ''
    spread: float = 0.0

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument('--lang=pt-BR')
    chrome_options.add_argument('--window-size=800,600')
    chrome_options.add_argument('--incognito')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


driver = iniciar_driver()


driver.get("https://veri.bet/simulator")


try:
    access_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div/div[1]/div/a"))
    )
    access_button.click()
    print('Entrando na página de apostas...')
except TimeoutException:
    print("Não foi possível encontrar o botão de acesso ao simulador de apostas.")
    driver.quit()
    exit()

try:
    betting_lines = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".some-table-row-selector")) # Este seletor deve ser o que seleciona cada linha da tabela de apostas
    )
except TimeoutException:
    print("Tempo esgotado esperando pelas linhas de apostas carregarem.")
    driver.quit()
    exit()


items = []
for line in betting_lines:
    sport_league = line.find_element(By.CSS_SELECTOR, '.sport-league-selector').text
    event_date_utc = line.find_element(By.CSS_SELECTOR, '.event-date-selector').text
    team1 = line.find_element(By.CSS_SELECTOR, '.team1-selector').text
    team2 = line.find_element(By.CSS_SELECTOR, '.team2-selector').text
    
    
    item = Item(
        sport_league=sport_league,
        event_date_utc=event_date_utc,
        team1=team1,
        team2=team2
        #TODO:mais campos aqui...
    )
    items.append(item)


items_json = json.dumps([asdict(item) for item in items], indent=4)
print(items_json)


with open('betting_lines.json', 'w') as f:
    f.write(items_json)


driver.quit()
