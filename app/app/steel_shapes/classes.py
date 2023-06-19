import fractions
import numpy as np

def format_num(num, decimal_len=3):
    try:
        num_str = str(num)
        num_float = float(sum(fractions.Fraction(s) for s in num_str.split()))
        num_formatted = ("{:." + str(decimal_len) + "f}").format(num_float).rstrip('0').rstrip('.')
        return num_formatted
    except:
        return num

class ShapeProperties:

    def __init__(self, shape_df):
        self.shape_df = shape_df

    def select_shape_data(self, shape_label, label_column='EDI_Std_Nomenclature'):
        self.selected_shapes = self.shape_df[self.shape_df[label_column] == shape_label]
        self.shape_section = self.selected_shapes['Type'].values[0]

    def select_section_data(self, shape_sections):
        self.selected_rows = self.shape_df[self.shape_df['Type'].isin(shape_sections)]

    def filter_by_value(self, **kwargs):
        filtered_rows = self.selected_rows.copy()

        for shape_property, value_limits in kwargs.items():
            property_values = filtered_rows[shape_property].astype(float)
            min_value = value_limits[0]
            max_value = value_limits[1]

            if min_value and max_value:
                filtered_rows = filtered_rows[(property_values >= float(min_value)) & (property_values <= float(max_value))]
            elif min_value:
                filtered_rows = filtered_rows[property_values >= float(min_value)]
            elif max_value:
                filtered_rows = filtered_rows[property_values <= float(max_value)]
            else:
                pass

        self.selected_shapes = filtered_rows

    def format_shape_data(self, properties_to_output):
        selected_columns = self.selected_shapes.reindex(columns=properties_to_output)
        selected_columns.replace(to_replace='0', value='–', inplace=True)
        filtered_columns = selected_columns.replace(to_replace='–', value=np.nan).dropna(axis=1, how='all').fillna('–')
        self.headers = filtered_columns.columns
        self.output_data = filtered_columns.applymap(format_num)

    def output_shape_data(self, table_header_dict):
        output_dict = {}
        output_dict['selected_properties'] = self.output_data.values
        output_dict['property_headers'] = [table_header_dict[header][1] for header in self.headers]
        output_dict['unit_headers'] = [table_header_dict[header][2] for header in self.headers]
        return output_dict

    def export_properties(self, output_filepath):
        output_df = self.selected_shapes
        output_df.to_excel(output_filepath, index=False)

class HistoricShapeProperties(ShapeProperties):

    def __init__(self, shape_df, editions):
        self.shape_df = shape_df[shape_df['Edition'].isin(editions)]
