from xml.etree import ElementTree
from ingredientsErr import IngredientsError


class Ingredient:
    @classmethod
    def ingrType(cls):
        return cls.__name__

    availableUnits = ['ml', 'szt', 'g']

    name = None
    qty = None
    unit = None

    def __init__(self, name, qty, unit):
        self.name = name
        self.qty = qty
        self.unit = unit

    def __repr__(self):
        return f'{self.ingrType()}({self.name}, {self.qty}{self.unit})'


class Alcohol(Ingredient):
    def __init__(self, name, qty,):
        super().__init__(name, qty, 'ml')


class Filler(Ingredient):
    def __init__(self, name, qty):
        super().__init__(name, qty, 'ml')


class Addon(Ingredient):
    def __init__(self, name, qty, unit):
        super().__init__(name, qty, unit)


class Recipe:

    def __init__(self, name, alcohols, fillers, addons):
        self.name = name
        self.alcohols = alcohols
        self.fillers = fillers
        self.addons = addons

    @classmethod
    def fromXmlString(cls, xml_string):
        return RecipeParser.fromString(xml_string)
    
    def toXmlString(self):
        return RecipeParser.toString(self)

    def listOfIngr(self):
        ingr = self.alcohols + self.fillers + self.addons
        return ingr

    def listOfIngrNames(self):
        ingr_names = []
        for x in self.listOfIngr():
            ingr_names.append(x.name)
        return ingr_names


class RecipeParser:

    @classmethod
    def fromString(cls, xml_string):
        root = ElementTree.fromstring(xml_string)
        name = root.find('Name').text
        ingredients = root.find('Ingredients')
        ingr_list = []
        for ingr in ingredients:
            ingr_list.append({
                'Alcohol': Alcohol(ingr.text, ingr.get('quantity')),
                'Filler': Filler(ingr.text, ingr.get('quantity')),
                'Addon': Addon(ingr.text, ingr.get('quantity'), ingr.get('unit'))
                }[ingr.tag])
        alcohols = [x for x in ingr_list if x.ingrType() == 'Alcohol']
        fillers = [x for x in ingr_list if x.ingrType() == 'Filler']
        addons = [x for x in ingr_list if x.ingrType() == 'Addon']
        return Recipe(name, alcohols, fillers, addons)

    @classmethod
    def toString(cls, recipe):
        root = ElementTree.Element('Recipe')
        name = ElementTree.SubElement(root, 'Name')
        name.text = recipe.name
        ingredients = ElementTree.SubElement(root, 'Ingredients')
        for ingr in recipe.listOfIngr():
            attr = {'quantity': str(ingr.qty), 'unit': ingr.unit}
            ElementTree.SubElement(ingredients, ingr.ingrType(), attr).text = ingr.name
        ElementTree.indent(root)
        return ElementTree.tostring(root, encoding='unicode')

