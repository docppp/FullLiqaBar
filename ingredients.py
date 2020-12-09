
from ingredientsErr import IngredientsError


class Ingredient:
    @classmethod
    def className(cls):
        return cls.__name__

    availableUnits = ['ml', 'szt', 'g']

    name = None
    qty = None
    unit = None

    def __init__(self, name, qty, unit):
        if type(name) is not str:
            err = f'Name of {self.className()} is type {type(name)}. Should be {str}.'
            raise TypeError(err)

        if not (type(qty) is int or type(qty) is float):
            err = f'Qty of {self.className()} is type {type(qty)}. Should be {int} or {float}.'
            raise TypeError(err)

        if type(unit) is not str:
            err = f'Unit of {self.className()} is type {type(qty)}. Should be {int}.'
            raise TypeError(err)

        if unit not in self.availableUnits:
            err = f'Unit {unit} not recognized. Should be one of: {self.availableUnits}'
            raise IngredientsError(err)

        self.name = name
        self.qty = qty
        self.unit = unit


class Alcohol(Ingredient):
    def __init__(self, name, qty,):
        super().__init__(name, qty, 'ml')


class Filler(Ingredient):
    def __init__(self, name, qty):
        super().__init__(name, qty, 'ml')


class Addon(Ingredient):
    def __init__(self, name, qty, unit):
        super().__init__(name, qty, unit)


# class XmlParser:
#
#     @staticmethod
#     def xmlStringFromIng(ingredient):
#         xml_string = f"<{(ingredient.className())} " \
#                      f"qty='{ingredient.qty}' " \
#                      f"unit='{ingredient.unit}'>" \
#                      f"{ingredient.name}" \
#                      f"</{(ingredient.className())}>"
#         return xml_string
#
#     @staticmethod
#     def getClassFromTag(xml_string):
#         tag_start = xml_string.find("<") + 1
#         tag_end = xml_string.find(" ")
#         return xml_string[tag_start:tag_end]
#
#     @staticmethod
#     def getQtyFromTag(xml_string):
#         attr_start = xml_string.find(" qty='") + 6
#         attr_end = xml_string.find("' unit='")
#         return xml_string[attr_start:attr_end]
#
#     @staticmethod
#     def getUnitFromTag(xml_string):
#         attr_start = xml_string.find(" unit='") + 7
#         attr_end = xml_string.find("'>")
#         return xml_string[attr_start:attr_end]
#
#     @staticmethod
#     def getNameFromTag(xml_string):
#         name_start = xml_string.find("'>") + 2
#         name_end = xml_string.find("</")
#         return xml_string[name_start:name_end]
#
#     @staticmethod
#     def ingrFromXmlString(xml_string):
#         class_name = XmlParser.getClassFromTag(xml_string)
#         print(class_name)
#         qty = XmlParser.getQtyFromTag(xml_string)
#         print(qty)
#         unit = XmlParser.getUnitFromTag(xml_string)
#         print(unit)
#         name = XmlParser.getNameFromTag(xml_string)
#         print(name)


class XmlParser:

    ingr = None
    xml_string = None

    def __init__(self, feed=None):
        if isinstance(feed, Ingredient):
            self.ingr = feed
            self.xml_string = self.__xmlStringFromIng()
        if type(feed) is str:
            try:
                self.xml_string = feed
                self.ingr = self.__ingrFromXmlString()
            except Exception:
                err = f"Cannot convert string '{self.xml_string}' to Ingredient"
                raise IngredientsError(err)

    def __xmlStringFromIng(self):
        return f"<{(self.ingr.className())} " \
                     f"qty='{self.ingr.qty}' " \
                     f"unit='{self.ingr.unit}'>" \
                     f"{self.ingr.name}" \
                     f"</{(self.ingr.className())}>"

    def __ingrFromXmlString(self):
        class_name = self.__getClassFromTag(self.xml_string)
        qty = int(self.__getQtyFromTag(self.xml_string))
        unit = self.__getUnitFromTag(self.xml_string)
        name = self.__getNameFromTag(self.xml_string)
        return {
            'Alcohol': Alcohol(name, qty),
            'Filler': Filler(name, qty),
            'Addon': Addon(name, qty, unit)
        }[class_name]

    @staticmethod
    def __getClassFromTag(xml_string):
        tag_start = xml_string.find("<") + 1
        tag_end = xml_string.find(" ")
        return xml_string[tag_start:tag_end]

    @staticmethod
    def __getQtyFromTag(xml_string):
        attr_start = xml_string.find(" qty='") + 6
        attr_end = xml_string.find("' unit='")
        return xml_string[attr_start:attr_end]

    @staticmethod
    def __getUnitFromTag(xml_string):
        attr_start = xml_string.find(" unit='") + 7
        attr_end = xml_string.find("'>")
        return xml_string[attr_start:attr_end]

    @staticmethod
    def __getNameFromTag(xml_string):
        name_start = xml_string.find("'>") + 2
        name_end = xml_string.find("</")
        return xml_string[name_start:name_end]
