import numpy as np
import csv
import os
import codecs


class PgfPlotter:
    def __init__(self,
                 data: np.ndarray,
                 export_name: str,
                 axis_options: dict = None):

        self.__data = None
        self.set_data(data)
        self.__headers = ['x'] + [f'y{i + 1}' for i in range(self.__data.shape[0] - 1)]

        self.__DEFAULT_AXIS_OPTN = {'width': '0.7*\linewidth',
                                    'height': '0.45*\linewidth',
                                    'xlabel': '$x$',
                                    'ylabel': '$y$',
                                    'grid': 'major',
                                    'grid style': '{dashed, gray!30}',
                                    }
        if axis_options is None:
            self.__options = self.__DEFAULT_AXIS_OPTN
        else:
            self.set_axis_options(axis_options)

        self.__name = export_name
        if not os.path.exists('export'):
            os.mkdir('export')
        self.__export_dir = 'export'
        self.__csv_name = f'{self.__name}.csv'
        self.__caption = 'What a great graph !'
        self.__label = f'fig:{self.__name}'
        self.__legend = None

        self.__code = ['\\begin{figure}[H]\n'
                       '\\centering\n'
                       '\t\\begin{tikzpicture}\n'
                       ]

    # Public methods

    def set_data(self, data):
        if data.shape[0] < 2:
            raise ValueError(f'Data should consist of at least 2 rows. Found {data.shape[0]}')
        self.__data = data

    def set_export_name(self, name):
        self.__name = name

    def set_axis_options(self, options):
        self.__options = options
        for k in self.__DEFAULT_AXIS_OPTN.keys():
            if k not in self.__options:
                self.__options[k] = self.__DEFAULT_AXIS_OPTN[k]

    def caption(self, caption):
        self.__caption = caption

    def label(self, label):
        self.__label = f'fig:{label}'

    def add_axis_optn(self, key, value):
        self.__options[key] = value

    def legend(self, items):
        self.__legend = items

    def export_latex(self):
        self.__write_csv()
        self.__add_axis()
        self.__code.append('\t\\end{tikzpicture}\n'
                           f'\\caption{{{self.__caption}}} \n'
                           f'\\label{{{self.__label}}}\n'
                           '\\end{figure}\n')

        with codecs.open(f'export/{self.__name}.tex', 'w', 'utf-8') as export:
            export.write("".join(self.__code))

    # Private methods

    def __write_csv(self):
        with open(f'{self.__export_dir}/{self.__csv_name}', mode='w', newline='') as data_file:
            data_writer = csv.writer(data_file, delimiter=';')
            data_writer.writerow(self.__headers)
            data_writer.writerows(self.__data.transpose())

    def __add_plot(self, x, y, mode='line', options=None, optn_mode='+'):
        plot_string = ['\t\t\t\\addplot', optn_mode, '[']
        if mode == 'line':
            if options is None:
                options = {'mark': 'none'}
            else:
                options['mark'] = 'none'
        elif mode == 'scatter':
            plot_string.append('only marks, ')
        plot_string.append(', '.join([f'{k}={v}' for k, v in options.items()]))
        plot_string.append(f'] table[x={x}, y={y}, col sep=semicolon] {{{self.__csv_name}}};\n')
        self.__code.append("".join(plot_string))

    def __add_all_plots(self):
        for i in range(self.__data.shape[0] - 1):
            self.__add_plot('x', self.__headers[i + 1])

    def __add_legend(self):
        legend_str = ['\t\t\t\legend{', ', '.join(self.__legend), '};\n']
        self.__code.append("".join(legend_str))

    def __add_axis(self):
        optn_string = '\n\t\t\t'.join([f'{k} = {v},' for k, v in self.__options.items()])
        axis = "".join([
            '\t\t\\begin{axis} [\n\t\t\t',
            optn_string,
            '\n\t\t\t]\n',
        ])
        self.__code.append(axis)
        self.__add_all_plots()
        if self.__legend is not None:
            self.__add_legend()
        self.__code.append('\t\t\\end{axis}\n')
