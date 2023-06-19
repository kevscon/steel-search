import os, csv, json
import pandas as pd
from flask import request

directory = os.getcwd() + '/app/app/steel_shapes'

output_filepath = os.getcwd() + '/app/app/steel_shapes/aisc_shape_properties.xlsx'
with open(directory + '/data/column_list.csv') as infile:
    properties_to_output = list(csv.reader(infile))[0]
with open(directory + '/data/table_header_dict.json', 'r') as infile:
    table_header_dict = json.load(infile)

def process_form():
    shape_df = pd.read_csv(directory + '/data/aisc-shapes-database-v15.0.csv')

    # shape_section = request.form['shape_section']
    shape_label = request.form['shape-label']

    from app.app.steel_shapes.classes import ShapeProperties
    property_class = ShapeProperties(shape_df)
    property_class.select_shape_data(shape_label)
    property_class.export_properties(output_filepath)
    property_class.format_shape_data(properties_to_output)
    output_dict = property_class.output_shape_data(table_header_dict)
    output_dict['shape_image'] = property_class.shape_section

    return output_dict

def filter_designations(shape_section):
    with open(os.getcwd() + '/app/app/steel_shapes/data/shape_dict.json', 'r') as infile:
        shape_dict = json.load(infile)
    shape_designations = list(shape_dict[shape_section].keys())
    return shape_designations

def filter_labels(shape_section, shape_designation):
    with open(os.getcwd() + '/app/app/steel_shapes/data/shape_dict.json', 'r') as infile:
        shape_dict = json.load(infile)
    return shape_dict[shape_section][shape_designation]

def process_historic_form():
    shape_df = pd.read_csv(os.getcwd() + '/app/app/steel_shapes/data/aisc-shapes-database-v15.0h.csv', dtype=str)

    edition = request.form['edition']
    shape_type = request.form['shape_type']
    shape_label = request.form['shape_label']

    from app.app.steel_shapes.classes import HistoricShapeProperties
    property_class = HistoricShapeProperties(shape_df, [edition])
    property_class.select_shape_data(shape_label, label_column='Designation')
    property_class.export_properties(output_filepath)
    properties_to_output[0] = 'Designation'
    properties_to_output.insert(0, 'Edition')
    property_class.format_shape_data(properties_to_output)
    output_dict = property_class.output_shape_data(table_header_dict)
    output_dict['shape_image'] = shape_type

    return output_dict

def filter_historic_sections(edition, shape_type):
    shape_df = pd.read_csv(os.getcwd() + '/app/app/steel_shapes/data/aisc-shapes-database-v15.0h.csv', dtype=str)
    with open(os.getcwd() + '/app/app/steel_shapes/data/shape_type_dict.json', 'r') as infile:
        shape_type_dict = json.load(infile)
    edition_df = shape_df[shape_df['Edition'] ==  edition]
    section_options = shape_type_dict[shape_type]
    section_df = edition_df[edition_df['Type'].isin(section_options)]
    shape_sections = list(section_df['Type'].unique())
    return shape_sections

def filter_historic_labels(edition, shape_section):
    shape_df = pd.read_csv(os.getcwd() + '/app/app/steel_shapes/data/aisc-shapes-database-v15.0h.csv', dtype=str)
    edition_df = shape_df[shape_df['Edition'] ==  edition]
    shape_labels = list(edition_df[edition_df['Type'] == shape_section]['Designation'].unique())
    return shape_labels
