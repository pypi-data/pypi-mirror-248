from AcdhArcheAssets.uri_norm_rules import get_norm_id, get_normalized_uri
from wikidata.client import Client


class NoWikiDataUrlException(Exception):
    pass


class WikiDataPerson:
    """Class to fetch and return often used data from WikiData Person entries"""

    def get_apis_person(self):
        return {
            "name": self.name,
            "first_name": self.first_name,
            "start_date_written": self.date_of_birth,
            "end_date_written": self.date_of_death,
            "gender": self.sex_or_gender,
        }

    def __init__(self, wikidata_url):
        if "wikidata" not in wikidata_url:
            raise NoWikiDataUrlException(f"{wikidata_url} is no proper Wikidata URL")
        else:
            self.wikidata_url = get_normalized_uri(wikidata_url)
        self.wikidata_id = get_norm_id(self.wikidata_url)
        self.client = Client()
        self.entity = self.client.get(self.wikidata_id, load=True)
        self.label = str(self.entity.label)
        date_of_birth_prop = self.client.get("P569")
        date_of_death_prop = self.client.get("P570")
        sex_or_gender_prop = self.client.get("P21")
        first_name_prop = self.client.get("P735")
        name_prop = self.client.get("P734")
        try:
            self.first_name = str(self.entity[first_name_prop].label)
        except KeyError:
            self.first_name = None
        try:
            self.name = str(self.entity[name_prop].label)
        except KeyError:
            self.name = None
        try:
            self.date_of_birth = str(self.entity[date_of_birth_prop])
        except KeyError:
            self.date_of_birth = None
        try:
            self.date_of_death = str(self.entity[date_of_death_prop])
        except KeyError:
            self.date_of_death = None
        try:
            self.sex_or_gender = str(self.entity[sex_or_gender_prop].label)
        except KeyError:
            self.sex_or_gender = None
