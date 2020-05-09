# from abc import ABC
from classes.state import State


class AbstractConstructionGoods:

    def __init__(self, producer_name='none', price_in_uah=0, color='black', weight_in_kilograms=0,
                 length_in_centimeters=0, width_in_centimeters=0, state=State.NEW):
        self.producer_name = producer_name
        self.price_in_uah = price_in_uah
        self.color = color
        self.weight_in_kilograms = weight_in_kilograms
        self.length_in_centimeters = length_in_centimeters
        self.width_in_centimeters = width_in_centimeters
        self.state = state

    def __del__(self):
        return
