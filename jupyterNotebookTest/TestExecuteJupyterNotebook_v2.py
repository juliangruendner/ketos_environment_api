import nbformat
import nbconvert
from nbconvert.preprocessors import ExecutePreprocessor

class MyExecutePreprocessor(nbconvert.preprocessors.ExecutePreprocessor):

    toExecute = 'execute'

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

        print("executing cell with name" + cell_source.splitlines()[0] )
        return super().preprocess_cell(cell, resources, cell_index)


    def setCellsToExecute(self, sToExecute):
        self.toExecute = sToExecute


    def ketos_parseCellFirstLine(self, cell_source):
        
        if len(cell_source) == 0:
            return []

        first_line = cell_source.splitlines()[0]

        parsed_first_line = []

        if len(first_line) > 0 and first_line[0] == '#':
            print(first_line[0])
            first_line = first_line[1:]
            stripped_first_line = first_line.replace(" ","")
            parsed_first_line = stripped_first_line.split(',')

        return parsed_first_line

    def ketos_executeNotebookCells(self,nb,cells_to_execute = 'ketos_predict' ):
        ep.setCellsToExecute(cells_to_execute)
        ep.preprocess(nb, {'metadata': {'path': nb_dir}})
        self.nb = nb

    def ketos_get_nb_output(self, nb):
        prediction = ''
        cells = nb.cells
        for cell in cells:
            if('ketos_predict_output' in ep.ketos_parseCellFirstLine(cell.source)):
                prediction = cell.outputs[0].text
                return prediction




nb_filename = 'test_model.ipynb'
nb_dir = '/Users/juliangruendner/phd/code/mlService_dockerApi/jupyterNotebookTest/'

ep = MyExecutePreprocessor(timeout=600, kernel_name='ir')
nb_filepath = nb_dir + nb_filename

with open(nb_filepath) as f:
    nb = nbformat.read(f, as_version=4)
    nb = ep.ketos_executeNotebookCells(nb)
    prediction = ep.ketos_get_nb_output(nb)
    

    
