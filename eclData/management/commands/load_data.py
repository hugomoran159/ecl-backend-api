from eclData.models import City, Data, Country
from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from bs4 import BeautifulSoup
import httplib2
import re


class Command(BaseCommand):
    help = "updates city data"

    def handle(self, *args, **options):
        http = httplib2.Http()

        colnames = ["city", "country", "latitude", "longitude"]
        city_df = pd.read_csv("static/cities.csv", names=colnames, header=None)
        city_df = city_df.drop(city_df.index[0])

        df_headers = {
            "currency": [],
            "city": [],
            "meal": [],
            "mcmeal": [],
            "beer restaurant": [],
            "milk": [],
            "rice": [],
            "potato": [],
            "water": [],
            "cigarettes": [],
            "coffee": [],
            "ticket": [],
            "rent": [],
            "country": [],
            "latitude": [],
            "longitude": [],
        }
        df = pd.DataFrame(data=df_headers)
        city_data = {}

        def get_cost_living_data(props):
            city = props["city"].strip()
            if " " in city:
                city_arr = city.split(" ")
                city_arr = list(map(lambda word: word.capitalize(), city_arr))
                city = "-".join(city_arr)
            else:
                city = city.capitalize()

            url = (
                "https://www.numbeo.com/cost-of-living/in/"
                + city
                + "?displayCurrency=EUR"
            )
            status, response = http.request(url)
            soup = BeautifulSoup(response, "html.parser")
            """test_soup = soup.find_all(attrs={"id": 'displayCurrency'})"""
            all_tds = soup.find_all("td")

            city_data["currency"] = "€"
            city_data["city"] = props["city"]
            city_data["country"] = props["country"]
            city_data["latitude"] = props["latitude"]
            city_data["longitude"] = props["longitude"]

            get_meal_price(all_tds)
            get_market_prices(all_tds)
            get_transport_prices(all_tds)
            get_rent_prices(all_tds)

        def get_meal_price(tds):
            domestic_beer = False

            for ind, td in enumerate(tds):
                if "Meal, Inexpensive" in td.text:
                    city_data["meal"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "McDonalds" in td.text:
                    city_data["mcmeal"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "Domestic Beer" in td.text and domestic_beer == False:
                    domestic_beer = True
                    city_data["beer restaurant"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "Cappuccino" in td.text:
                    city_data["coffee"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

        def get_market_prices(tds):
            water_bottle = False
            cigarettes = False

            for ind, td in enumerate(tds):
                if "Milk" in td.text:
                    city_data["milk"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "Rice" in td.text:
                    city_data["rice"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "Potato" in td.text:
                    city_data["potato"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

                if "Water" in td.text:
                    if water_bottle == True:
                        city_data["water"] = [
                            tds[ind].text,
                            re.sub("[^0-9.]", "", tds[ind + 1].text),
                        ]
                    water_bottle = not water_bottle

                if "Cigarettes 20 Pack" in td.text and cigarettes == False:
                    cigarettes = True
                    city_data["cigarettes"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

        def get_transport_prices(tds):
            for ind, td in enumerate(tds):
                if "One-way Ticket" in td.text:
                    city_data["ticket"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

        def get_rent_prices(tds):
            for ind, td in enumerate(tds):
                if "Apartment (3 bedrooms) in City Centre" in td.text:
                    city_data["rent"] = [
                        tds[ind].text,
                        re.sub("[^0-9.]", "", tds[ind + 1].text),
                    ]

        for index, row in city_df.iterrows():
            get_cost_living_data(row)
            city_data = pd.DataFrame([city_data])
            df = pd.concat([df, city_data], axis=0, ignore_index=True)
            city_data = {}

        City.objects.all().delete()
        Data.objects.all().delete()

        # loop through each row in the DataFrame
        for index, row in df.iterrows():
            # create or update the Country model
            country, created = Country.objects.get_or_create(name=row["country"])

            # create or update the City model
            city, created = City.objects.update_or_create(
                name=row["city"],
                defaults={
                    "longitude": row["longitude"],
                    "latitude": row["latitude"],
                    "country": country,
                },
            )

            # loop through each column in the row
            for col in df.columns:
                # check if the column is a data column
                if col not in ["currency", "city", "country", "longitude", "latitude"]:
                    # create the Data model
                    Data.objects.create(
                        name=col,
                        description=row[col][0],
                        value=row[col][1],
                        currency=row["currency"],
                        city=city,
                    )

                    """
        def createDataNode(index, row, counter, city):
            node= Data(name=index[counter], value=row[counter][1], description=row[counter][0], currency=row[0], city=city)
            return node
        
        for index, row in df.iterrows():

            city, _ = City.objects.get_or_create(name=row[1])
            
            for counter in row:
                node = createDataNode(index, row, counter, city)
                node.save()
                
        """

            """
            mealdata = Data(name="meal", value=row[2][1], description=row[2][0], currency=row[0], city=city)
            mealdata.save()
            mcmealdata = Data(name="mcmeal", value=row[3][1], description=row[3][0], currency=row[0], city=city)
            mcmealdata.save()
            beerdata = Data(name="beer", value=row[4][1], description=row[4][0], currency=row[0], city=city)
            beerdata.save()
            milkdata = Data(name="milk", value=row[5][1], description=row[5][0], currency=row[0], city=city)
            milkdata.save()
            ricedata = Data(name="rice", value=row[6][1], description=row[6][0], currency=row[0], city=city)
            ricedata.save()
            potatosdata = Data(name="potatoes", value=row[7][1], description=row[7][0], currency=row[0], city=city)
            potatosdata.save()
            waterdata = Data(name="water", value=row[8][1], description=row[8][0], currency=row[0], city=city)
            waterdata.save()
            cigarettesdata = Data(name="cigarettes", value=row[9][1], description=row[9][0], currency=row[0], city=city)
            cigarettesdata.save()
            coffeedata = Data(name="coffee", value=row[10][1], description=row[10][0], currency=row[0], city=city)
            coffeedata.save()
            ticketdata = Data(name="ticket", value=row[11][1], description=row[11][0], currency=row[0], city=city)
            ticketdata.save()
            rentdata = Data(name="rent", value=row[12][1], description=row[12][0], currency=row[0], city=city)
            rentdata.save()
            """

        self.stdout.write("", ending="Data successfully updated")
