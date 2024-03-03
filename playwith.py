import connect_mongo
from models import Contact

if __name__ == "__main__":
    Contact(
        fullname="Grzesiu Wombat",
        email="wombat@wombat.plp",
    ).save()
    Contact(
        fullname="Grzesiu Wombat",
        email="wombat@wombat.plp",
        phone="4453776323",
        contact_via="sms",
    ).save()
