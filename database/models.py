from sqlalchemy import Column, Integer, String, CHAR, ForeignKey, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import relationship, declarative_base

base = declarative_base()

class Student(base):
    __tablename__ = 'students'

    uuid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    regNo = Column(CHAR(9), unique=True, nullable=False)
    email = Column(String, nullable=False)
    gender = Column(CHAR(1))
    phoneNo = Column(CHAR(10))
    block = Column(String)

    registrations = relationship('Registration', back_populates='student')
    teams = relationship('MemberOf', back_populates='student')
    certificates = relationship('Certificate', back_populates='student')

class User(base):
    __tablename__ = "users"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    regNo = Column(String, unique=True, nullable=False)
    email = Column(String)

    clubs = relationship('Club', secondary="admins", back_populates="admins")

class Club(base):
    __tablename__ = "clubs"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    clubName = Column(String, nullable=False)
    adminId = Column(Integer, ForeignKey("users.uuid"))
    email = Column(String, nullable=False)
    facultyName = Column(String)
    InstagramLink = Column(String)
    LinkedInLink = Column(String)
    YoutubeLink = Column(String)

    events = relationship('Event', back_populates='club')
    admins = relationship('User', secondary="admins", back_populates="clubs")

class Event(base):
    __tablename__ = "events"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    clubId = Column(Integer, ForeignKey("clubs.uuid"))
    name = Column(String, nullable=False)
    brief = Column(String)
    contact = Column(String)
    duration = Column(Integer)
    dateAndTime = Column(DateTime)
    venue = Column(String)
    isTeam = Column(Boolean)
    noOfSeats = Column(Integer)
    minTeamMembers = Column(Integer)
    maxTeamMembers = Column(Integer)
    templateId = Column(Integer)
    logo = Column(LargeBinary)
    approvalStatus = Column(Boolean)
    validators = Column(String)

    club = relationship('Club', back_populates='events')
    registrations = relationship('Registration', back_populates='event')
    photos = relationship('Photo', back_populates='event')
    customInputs = relationship('CustomInput', back_populates='event')
    teams = relationship('Team', back_populates='event')
    certificates = relationship('Certificate', back_populates='event')

class Photo(base):
    __tablename__ = "photos"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    eventId = Column(Integer, ForeignKey('events.uuid'))
    photo = Column(LargeBinary)

    event = relationship('Event', back_populates='photos')

class Registration(base):
    __tablename__ = "registrations"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    eventId = Column(Integer, ForeignKey('events.uuid'))
    studentId = Column(Integer, ForeignKey('students.uuid'))

    event = relationship('Event', back_populates='registrations')
    student = relationship('Student', back_populates='registrations')

class CustomInput(base):
    __tablename__ = "customInputs"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    eventId = Column(Integer, ForeignKey('events.uuid'))
    question = Column(String)

    event = relationship('Event', back_populates='customInputs')
    responses = relationship('CustomResponse', back_populates='question')

class CustomResponse(base):
    __tablename__ = "customResponses"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    questionId = Column(Integer, ForeignKey('customInputs.uuid'))
    studentId = Column(Integer, ForeignKey('students.uuid'))
    response = Column(String)

    question = relationship('CustomInput', back_populates='responses')

class Admin(base):
    __tablename__ = "admins"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    clubId = Column(Integer, ForeignKey('clubs.uuid'))
    userId = Column(Integer, ForeignKey('users.uuid'))

class Team(base):
    __tablename__ = "teams"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    eventId = Column(Integer, ForeignKey('events.uuid'))
    teamCode = Column(String)
    teamLeader = Column(Integer, ForeignKey('students.uuid'))

    event = relationship('Event', back_populates='teams')
    members = relationship('MemberOf', back_populates='team')

class MemberOf(base):
    __tablename__ = "memberOf"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    studentId = Column(Integer, ForeignKey('students.uuid'))
    teamId = Column(Integer, ForeignKey('teams.uuid'))

    student = relationship('Student', back_populates='teams')
    team = relationship('Team', back_populates='members')

class Certificate(base):
    __tablename__ = "certificates"
    uuid = Column(Integer, primary_key=True, autoincrement=True)
    eventId = Column(Integer, ForeignKey('events.uuid'))
    studentId = Column(Integer, ForeignKey('students.uuid'))
    certificate = Column(LargeBinary)

    event = relationship('Event', back_populates='certificates')
    student = relationship( 'Student', back_populates='certificates')