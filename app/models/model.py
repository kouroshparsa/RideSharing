# coding: utf-8
from sqlalchemy import ARRAY, Boolean, CHAR, Column,\
    Date, DateTime, Enum, ForeignKey, Index, Integer,\
    LargeBinary, Numeric, SmallInteger, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geography

from app.database import Base
metadata = Base.metadata


class Driver(Base):
    __tablename__ = 'driver'

    id = Column(Integer, primary_key=True, server_default=text("nextval('actor_actor_id_seq'::regclass)"))
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    status = Column(Integer, nullable=False)
    is_verified = Column(Text, nullable=False)
    date_of_birth = Column(Date(), nullable=False)
    location = Column(Geography('POINT', 4326))
    pass_hash = Column(Text, nullable=False)
    vehicle_type = Column(Integer, nullable=False)
    rating = Column(Numeric(3, 1), nullable=False)

class Rider(Base):
    __tablename__ = 'rider'

    id = Column(Integer, primary_key=True, server_default=text("nextval('actor_actor_id_seq'::regclass)"))
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    date_of_birth = Column(Date(), nullable=False)
    pass_hash = Column(Text, nullable=False)
    rating = Column(Numeric(3, 1), nullable=False)


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

class Earning(Base):
    __tablename__ = 'earning'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    driver_id = Column(ForeignKey('driver.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))


class FailedPayment(Base):
    __tablename__ = 'failed_payment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime(True), nullable=False, server_default=text("now()"))


class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    origin = Column(Geography('POINT', 4326))
    destination = Column(Geography('POINT', 4326))
    booking_id = Column(Text, nullable=False)
    trip_time = Column(DateTime(True), nullable=False, server_default=text("now()"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    driver_id = Column(ForeignKey('payment.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)

