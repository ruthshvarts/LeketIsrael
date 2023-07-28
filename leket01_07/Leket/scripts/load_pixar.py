
from LeketIsraelApp.models import leket_DB_24_06
import csv

def run():
    with open('leket_db_24_06.csv', encoding="cp1255") as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        leket_DB_24_06.objects.all().delete()

        for row in reader:
            print(row)

            # genre, _ = Genre.objects.get_or_create(name=row[-1])

            leket_db_new = leket_DB_24_06(group=row[0],
                                        type=row[1],
                                        area=row[2],
                                        leket_location=row[3],
                                        amount_kg=row[4],
                                        missionID=row[5],
                                        farmerID=row[6],
                                        date=row[7],
                                        napa_name = row[9],
                                        aklim_area=row[11],
                                        TMY_station=row[12],
                                        station=row[14],
                                        max_temp = row[16],
                                        min_temp = row[17],
                                        ground_temp=row[18],
                                        shmita=row[19],
                                        chagim=row[20])
            leket_db_new.save()