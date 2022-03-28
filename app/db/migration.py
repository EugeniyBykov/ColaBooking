from app import db
from db.models import MeetingRoom, User, Company, BookingShift

def init_db():
    db.create_all()
    initDefaultCompanies()
    initDefaultMeetingRooms()
    initUsers()

def initDefaultCompanies():
    PepsiCompany = Company(name="Pepsi")
    db.session.add(PepsiCompany)
    CocaCompany = Company(name="Coca")
    db.session.add(CocaCompany)
    db.session.commit()

def initDefaultMeetingRooms():
    i = 1
    while i <= 10:
        if i < 10:
            PepsiRoom = MeetingRoom(name='P0' + str(i), company_id=1)
            CocaRoom = MeetingRoom(name='C0' + str(i), company_id=2)
        else:
            PepsiRoom = MeetingRoom(name='P' + str(i), company_id=1)
            CocaRoom = MeetingRoom(name='C' + str(i), company_id=2)

        db.session.add(PepsiRoom)
        db.session.add(CocaRoom)
        i += 1

    db.session.commit()

def initUsers():
    pepsiUser = User(
        name="pepsiUser",
        psw="pbkdf2:sha256:260000$N7nxqJkZKQTQFbdS$50af9427639af1af04269ba78234dc65080959cea39aa4b894d8aec8af4f4b53",
        company_id = 1
    )
    db.session.add(pepsiUser)
    cocaUser = User(
        name="cocaUser",
        psw="pbkdf2:sha256:260000$qD3aDyAUQpvws7uH$e67a22a802b67f738bef0019e2f03a299fc0089c30d1265598a2b7c65c6e7b63",
        company_id = 1
    )
    db.session.add(cocaUser)

    db.session.commit()