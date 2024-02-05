import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def fetch_nba_data():


    url = "https://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=5&LeagueID=00&Location=&MeasureType=Four%20Factors&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2023-24&SeasonSegment=&SeasonType=Regular%20Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision="
    
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Host": "stats.nba.com",
        "Origin": "https://www.nba.com",
        "Pragma": "no-cache",
        "Referer": "https://www.nba.com/",
        "Sec-Ch-Ua": '"Not A Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

  
    # headers = {
    #     "User-Agent": "Mozilla/5.0",
    #     "Accept": "application/json",
    #     "Referer": "https://www.nba.com/",
    # }
    print(url)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        # response = requests.get(url, headers=headers, timeout=10)
        print(response.status_code)
    except Exception as e:
        print(f"An error occurred: {e}")

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def format_nba_data(data):
    # Extract headers and rows from the JSON response
    headers = data['resultSets'][0]['headers']
    rows = data['resultSets'][0]['rowSet']
    
    # Define the final formatted data list
    formatted_data = []
    
    # Iterate through each row to format and collect data
    for row in rows:
        formatted_row = dict(zip(headers, row))
        # Transform the row data into your specific format
        formatted_data.append([
            formatted_row['TEAM_NAME'], formatted_row['GP'], formatted_row['W'],
            formatted_row['L'], formatted_row['W_PCT'], formatted_row['MIN'],
            formatted_row['EFG_PCT'], formatted_row['FTA_RATE'], formatted_row['TM_TOV_PCT'],
            formatted_row['OREB_PCT'], formatted_row['OPP_EFG_PCT'], formatted_row['OPP_FTA_RATE'],
            formatted_row['OPP_TOV_PCT'], formatted_row['OPP_OREB_PCT']
        ])
    
    return formatted_data

def update_google_sheet(data, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.clear()  # Clear the existing data

    # Define the header based on your specified format
    header = ["TEAM", "GP", "W", "L", "WIN%", "MIN", "EFG%", "FTA RATE", "TOV%", "OREB%", "OPP EFG%", "OPP FTA RATE", "OPP TOV%", "OPP OREB%"]
    sheet.append_row(header)

    # Append each row of formatted data to the sheet
    for row in data:
        sheet.append_row(row)

if __name__ == "__main__":
    raw_data = fetch_nba_data()
    if raw_data:
        formatted_data = format_nba_data(raw_data)
        print(formatted_data)
        update_google_sheet(formatted_data, 'NBA')
