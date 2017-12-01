import nbformat
import nbconvert
from nbconvert.preprocessors import ExecutePreprocessor
import json

class KetosNotebookProcessor(nbconvert.preprocessors.ExecutePreprocessor):

    # @override
    def preprocess_cell(self, cell, resources, cell_index):
        """
        Executes a single code cell. See base.py for details.
        To execute all cells see :meth:`preprocess`.

        Checks cell.metadata for 'execute' key. If set, and maps to False,
          the cell is not executed.
        """
        cell_source = cell.source
        first_line = self.ketos_parseCellFirstLine(cell_source)
        if not self.toExecute in first_line :
            # Don't execute this cell in output
            return cell, resources

        return super().preprocess_cell(cell, resources, cell_index)


    def setCellsToExecute(self, sToExecute):
        self.toExecute = sToExecute


    def ketos_parseCellFirstLine(self, cell_source):
        
        if len(cell_source) == 0:
            return []

        first_line = cell_source.splitlines()[0]

        parsed_first_line = []

        if len(first_line) > 0 and first_line[0] == '#':
            first_line = first_line[1:]
            stripped_first_line = first_line.replace(" ","")
            parsed_first_line = stripped_first_line.split(',')

        return parsed_first_line

    def ketos_set_notebook(self, nb_filename, nb_dir):
        nb_filepath = nb_dir + nb_filename
        with open(nb_filepath) as f:
            nb = nbformat.read(f, as_version=4)
            self.nb = nb

    def ketos_executeNotebookCells(self, cells_to_execute = 'ketos_predict'):
        self.setCellsToExecute(cells_to_execute)
        nb = self.nb
        self.preprocess(nb, {'metadata': {'path': nb_dir}})
        self.nb = nb

    def ketos_get_nb_output(self):
        prediction = ''
        cells = self.nb.cells
        for cell in cells:
            if('ketos_predict_output' in ep.ketos_parseCellFirstLine(cell.source)):
                prediction = cell.outputs[0].text
                return self.ketos_helper_clean_output(prediction)
                

    def ketos_helper_clean_output(self, output):
        return output.split('"')[1]

    def ketos_insert_data_url_source(self, source, data_url):
    
        data_insertion = 'ketos_predict_data = ("' + data_url + '")' 
        source_lines = source.splitlines()
        
        for index in range(0 , len(source_lines)):
            s_line = source_lines[index]
            data_string = 'ketos_predict_data'
            if s_line.find(data_string) != -1:
                source_lines[index] = data_insertion

        return '\n'.join(source_lines)

    def ketos_insert_data_url(self, data_url):
        for cell in self.nb.cells:
            if 'ketos_predict' in self.ketos_parseCellFirstLine(cell.source):
                new_source = self.ketos_insert_data_url_source(cell.source, data_url)
                cell.source = new_source
    

#ep = KetosNotebookProcessor(timeout=600, kernel_name='ir')
#ep.ketos_executeNotebookCells(nb_filename, nb_dir)
#prediction = ep.ketos_get_nb_output()
#print(prediction)



nb_filename = 'test_model.ipynb'
nb_dir = '/Users/juliangruendner/phd/code/mlService_dockerApi/jupyterNotebookTest/'
nb_filepath = nb_dir + nb_filename

ep = KetosNotebookProcessor(timeout=600, kernel_name='ir')
ep.ketos_set_notebook(nb_filename, nb_dir)
ep.ketos_insert_data_url('http://localhost:9000/mytest/url/awesome')
ep.ketos_executeNotebookCells()

prediction = ep.ketos_get_nb_output()
print(prediction)
