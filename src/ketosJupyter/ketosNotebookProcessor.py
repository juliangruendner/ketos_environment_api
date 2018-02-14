import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import json

class KetosNotebookProcessor(ExecutePreprocessor):

    # @override
    def preprocess_cell(self, cell, resources, cell_index):
        cell_source = cell.source
        first_line = self.ketos_parse_cell_first_line(cell_source)

        if self.toExecute not in first_line:
            return cell, resources

        return super().preprocess_cell(cell, resources, cell_index)

    def ketos_set_cells_to_execute(self, sToExecute):
        self.toExecute = sToExecute

    def ketos_parse_cell_first_line(self, cell_source):

        if len(cell_source) == 0:
            return []

        first_line = cell_source.splitlines()[0]
        parsed_first_line = []

        if len(first_line) > 0 and first_line[0] == '#':
            first_line = first_line[1:]
            stripped_first_line = first_line.replace(" ", "")
            parsed_first_line = stripped_first_line.split(',')

        return parsed_first_line

    def ketos_set_notebook(self, nb_filepath):
        with open(nb_filepath) as f:
            nb = nbformat.read(f, as_version=4)
            self.nb = nb

    def ketos_execute_notebook_cells(self, nb_dir, cells_to_execute='ketos_predict'):
        self.ketos_set_cells_to_execute(cells_to_execute)
        nb = self.nb
        self.preprocess(nb, {'metadata': {'path': nb_dir}})
        self.nb = nb

    def ketos_get_nb_output(self):
        prediction = ''
        cells = self.nb.cells
        for cell in cells:
            if('ketos_predict_output' in self.ketos_parse_cell_first_line(cell.source)):
                prediction = cell.outputs[0].text
                return self.ketos_helper_clean_output(prediction)

    def ketos_helper_clean_output(self, output):
        json_string = output[output.find("{") - 1:]
        return json.loads(json_string)

    def ketos_insert_data_url_source(self, source, data_url):

        data_insertion = 'ketos_predict_data = ("' + data_url + '")'
        source_lines = source.splitlines()

        for index in range(0, len(source_lines)):
            s_line = source_lines[index]
            data_string = 'ketos_predict_data'
            if s_line.find(data_string) != -1:
                source_lines[index] = data_insertion
                break

        return '\n'.join(source_lines)

    def ketos_insert_data_url(self, data_url):

        for cell in self.nb.cells:
            if 'ketos_predict' in self.ketos_parse_cell_first_line(cell.source):
                new_source = self.ketos_insert_data_url_source(cell.source, data_url)
                cell.source = new_source
