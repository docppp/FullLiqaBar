from xml.etree import ElementTree


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
    def __init__(self, name, qty):
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

    def __repr__(self):
        return f"('{self.name}' {self.listOfIngrNames()})"

    @classmethod
    def fromXmlString(cls, xml_string):
        return RecipeParser.fromXmlString(xml_string)
    
    def toXmlString(self):
        return RecipeParser.toXmlString(self)

    def toHtmlString(self):
        return RecipeParser.toHtmlString(self)

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
    def fromXmlString(cls, xml_string):
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
    def toXmlString(cls, recipe):
        root = ElementTree.Element('Recipe')
        name = ElementTree.SubElement(root, 'Name')
        name.text = recipe.name
        ingredients = ElementTree.SubElement(root, 'Ingredients')
        for ingr in recipe.listOfIngr():
            attr = {'quantity': str(ingr.qty), 'unit': ingr.unit}
            ElementTree.SubElement(ingredients, ingr.ingrType(), attr).text = ingr.name
        ElementTree.indent(root, space="    ")
        return ElementTree.tostring(root, encoding='unicode') + "\n"

    @classmethod
    def toHtmlString(cls, recipe):
        html = '<strong>' + recipe.name + '</strong>\n'
        html += '<table style="width: 100%;"><tr>\n'

        html += '\t<td style="width: 33.3333%; vertical-align: top;"> Alkohole <ul>\n'
        for ingr in recipe.alcohols:
            html += f'\t\t<li>{ingr.name}: {ingr.qty} {ingr.unit}</li>\n'
        if not recipe.alcohols:
            html += "\t\t------\n"
        html += '\t</ul></td>\n'

        html += '\t<td style="width: 33.3333%; vertical-align: top;"> Wypełniacze <ul>\n'
        for ingr in recipe.fillers:
            html += f'\t\t<li>{ingr.name}: {ingr.qty} {ingr.unit}</li>\n'
        if not recipe.fillers:
            html += "\t\t------\n"
        html += '\t</ul></td>\n'

        html += '\t<td style="width: 33.3333%; vertical-align: top;"> Dodatki <ul>\n'
        for ingr in recipe.addons:
            html += f'\t\t<li>{ingr.name}: {ingr.qty} {ingr.unit}</li>\n'
        if not recipe.addons:
            html += "\t\t------\n"
        html += '\t</ul></td>\n'

        html += '</tr></table>\n'
        return html
