import os, json
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import Optional, DataRequired, Regexp, ValidationError
# from wtforms import , FieldList, FormField

class SearchForm(FlaskForm):

    shape_section = SelectField(
        'Select Shape Section:',
        choices = [('-1', '--select section--'), ('W', 'W'), ('M', 'M'),
        ('S', 'S'), ('HP', 'HP'), ('C', 'C'), ('MC', 'MC'), ('L', 'L'),
        ('WT', 'WT'), ('MT', 'MT'), ('ST', 'ST'), ('2L', '2L'),
        ('HSS (rectangular)', 'HSS (rectangular)'),
        ('HSS (round)', 'HSS (round)'), ('PIPE', 'PIPE')]
       )

    shape_designation = SelectField(
        'Select Shape Designation:',
        choices = [('-1', '--select designation--')]
       )

    shape_label = SelectField(
        'Select Shape Label:',
        choices = [('-1', '--select label--')]
       )

    submit = SubmitField('Show Properties')


# def make_form(field_factory, name="DictForm"):
#     items = dict(name="", **field_factory())
#     dict_form = type(name, (FlaskForm,), items)
#     return dict_form
#
# with open(os.getcwd() + '/app/app/steel_shapes/data/filter_dict_list.json', 'r') as infile:
#     filter_dict_list = json.load(infile)
#
# field_dict = {}
# for filter_dict in filter_dict_list:
#     field_dict[filter_dict['name']] = StringField(fiter_dict['label'])
# for key, val in filter_dict.items():
#     field_dict[key] = StringField(val)

# FilterForm = make_form(field_factory=lambda: field_dict)


class FilterForm(FlaskForm):

    weight_min = StringField(validators=[Optional()])
    weight_max = StringField(validators=[Optional()])

    depth_min = StringField(validators=[Optional(), Regexp('(\d+[\/\d. ]*|\d)', message="Minimum Depth: Enter only decimal or fraction input")])
    depth_max = StringField(validators=[Optional(), Regexp('(\d+[\/\d. ]*|\d)', message="Maximum Depth: Enter only decimal or fraction input")])

    y_bar_min = StringField(validators=[Optional(), Regexp('(\d+[\/\d. ]*|\d)', message="Minimum y bar: Decimal or fraction input only")])
    y_bar_max = StringField(validators=[Optional(), Regexp('(\d+[\/\d. ]*|\d)', message="Maximum y bar: Decimal or fraction input only")])

    submit = SubmitField('Show Properties')


class HistoricSearchForm(FlaskForm):

    edition = SelectField(
        'Select Steel Manual Edition:',
        choices = [('-1', '--select edition--'),
        ('14th', '14th, 2010'),
        ('13th', '13th, 2005'),
        ('LRFD3', 'LRFD3, 2001'),
        ('LRFD2', 'LRFD2, 1994'),
        ('ASD9', 'ASD9, 1989'),
        ('LRFD1', 'LRFD1, 1986'),
        ('ASD8', 'ASD8, 1980'),
        ('ASD7', 'ASD7, 1970'),
        ('ASD6', 'ASD6, 1964'),
        ('ASD5', 'ASD5, 1962'),
        ('Historic', 'Historic, < 1962')]
       )

    shape_type = SelectField(
        'Select Shape Type:',
        choices = [('-1', '--select type--'),
        ('angles', 'angles'), ('beams', 'beams'),
        ('joists', 'joists'), ('piles', 'piles'),
        ('channels', 'channels'), ('tubes', 'tubes'),
        ('columns', 'columns'), ('misc.', 'misc.'),
        ('tees', 'tees'), ('pipes', 'pipes'), ('z', 'z')]
       )

    shape_section = SelectField(
        'Select Shape Section:',
        choices = [('-1', '--select section--')]
       )

    shape_label = SelectField(
        'Select Shape Label:',
        choices = [('-1', '--select label--')]
       )

    submit = SubmitField('Show Properties')
