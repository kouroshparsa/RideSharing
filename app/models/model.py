"""
This module specified the database model
"""
# coding: utf-8
from sqlalchemy import Column, Numeric, Text, text,\
    Date, DateTime, ForeignKey, Integer

from geoalchemy2 import Geography

from app.database import Base
metadata = Base.metadata


class Driver(Base):
    """ registered drivers """
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
    """ registered riders with verified payment method """
    __tablename__ = 'rider'

    id = Column(Integer, primary_key=True, server_default=text("nextval('actor_actor_id_seq'::regclass)"))
    first_name = Column(Text, nullable=False)
    last_name = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    date_of_birth = Column(Date(), nullable=False)
    pass_hash = Column(Text, nullable=False)
    rating = Column(Numeric(3, 1), nullable=False)


class Payment(Base):
    """ patments of riders including taxes """
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

class Earning(Base):
    """ earnings of drivers """
    __tablename__ = 'earning'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    driver_id = Column(ForeignKey('driver.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    date = Column(DateTime(True), nullable=False, server_default=text("now()"))


class FailedPayment(Base):
    """ recording of failed payment which were already re-tried """
    __tablename__ = 'failed_payment'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(5, 2), nullable=False)
    payment_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    message = Column(Text, nullable=False)


class Trip(Base):
    """ recording of trips where a rider was picked up """
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True, server_default=text("nextval('language_language_id_seq'::regclass)"))
    origin = Column(Geography('POINT', 4326))
    destination = Column(Geography('POINT', 4326))
    booking_id = Column(Text, nullable=False)
    trip_time = Column(DateTime(True), nullable=False, server_default=text("now()"))
    rider_id = Column(ForeignKey('rider.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    driver_id = Column(ForeignKey('payment.id', ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)

