import pandas as pd
from geopy.geocoders import Nominatim



INPUT_FILE = "miesjca_postojowe_1.csv"
OUTPUT_FILE = "miejsca_postojowe_final.csv"


geolocator = Nominatim(user_agent="geokoding")


def create_full_address(row):
    adres = str(row.get('Adres')).strip()
    return f"{adres}, Warszawa, Polska"



def get_coordinates(address):
    location = geolocator.geocode(address, timeout=10)
    if location:
        return location.latitude, location.longitude
    else:
        return 0, 0



def main():
    df = pd.read_csv(INPUT_FILE, header=0)
    df['Adres'] = df['Adres'].fillna('').astype(str).str.strip()
    df['lat'] = None
    df['lon'] = None

    for idx, row in df.iterrows():
        lat, lon = get_coordinates(addr)
        df.at[idx, 'lat'] = lat
        df.at[idx, 'lon'] = lon
        print(idx + 1)
    df.to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()