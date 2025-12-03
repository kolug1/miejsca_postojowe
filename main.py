import pandas as pd
from geopy.geocoders import Nominatim



INPUT_FILE = "miejsca_postojowe_edit5.csv"
OUTPUT_FILE = "miejsca_postojowe_Z_WSPOLRZEDNYMI_FINAL.csv"


geolocator = Nominatim(user_agent="geokodowanie_parkingu_warszawa_v1")


def create_full_address(row):
    ulica = row.get('nazwa_ulicy', '').strip()
    numer = row.get('numer', '').strip()
    dzielnica = row.get('dzielnica', '').strip()
    adres_pelny = f"{ulica} {numer}".strip()
    if dzielnica:
        adres_pelny += f", {dzielnica}"
    return f"{adres_pelny}, Warszawa, Polska"



def get_coordinates(address):
    location = geolocator.geocode(address, timeout=10)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None



def main():
    df = pd.read_csv(INPUT_FILE, sep=';', header=0)
    df['nazwa_ulicy'] = df['nazwa_ulicy'].fillna('')
    df['numer'] = df['numer'].fillna('')
    if 'dzielnica' in df.columns:
        df['dzielnica'] = df['dzielnica'].fillna('')
    else:
        df['dzielnica'] = ''
    df['pelny_adres'] = df.apply(create_full_address, axis=1)
    df['lat'] = None
    df['lon'] = None
    for index, row in df.iterrows():
        numer_adresu = row['numer'].strip()
        lat = None
        lon = None
        if not numer_adresu:
            lat = "BLAD - brak numeru"
            lon = "BLAD - brak numeru"
        else:
            address = row['pelny_adres']
            lat_val, lon_val = get_coordinates(address)
            if lat_val is None or lon_val is None:
                lat = "BLAD - brak wspolrzednych"
                lon = "BLAD - brak wspolrzednych"
            else:
                lat = lat_val
                lon = lon_val
        df.loc[index, 'lat'] = lat
        df.loc[index, 'lon'] = lon
        print(index + 1)
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()