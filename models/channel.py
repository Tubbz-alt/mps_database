from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from models import Base

class DigitalChannel(Base):
  """
  DigitalChannnel class (digital_channels table)
  
  Properties:
   number: position of this channel in the card - starts at 0. The
           ApplicationCard checks if there are duplicate numbers and
           if the number does not exceed the maximum number of channels

  References:
   card_id: specifies the card that contains this channel

  Relationships:
   device_input: a DigitalChannel can be referenced by one or more
                 DeviceInputs (used by DigitalDevices)
  """
  __tablename__ = 'digital_channels'
  id = Column(Integer, primary_key=True)
  number = Column(Integer, nullable=False) #NOTE: Channel numbers need to start at 0, not 1.
  card_id = Column(Integer, ForeignKey('application_cards.id'), nullable=False)
  device_input = relationship("DeviceInput", uselist=False, backref="channel")
  
class AnalogChannel(Base):
  """
  AnalogChannel class (analog_channels table)

  Properties:
   number: position of this channel in the card - starts at 0. The
           ApplicationCard checks if there are duplicate numbers and
           if the number does not exceed the maximum number of channels

  References:
   card_id: specifies the card that contains this channel

  Relationships:
   analog_device: the AnalogDevice that uses this channel
  """
  __tablename__ = 'analog_channels'
  id = Column(Integer, primary_key=True)
  number = Column(Integer, nullable=False)
  card_id = Column(Integer, ForeignKey('application_cards.id'), nullable=False)
  analog_device = relationship("AnalogDevice", uselist=False, backref="channel")