__author__ = "datacorner.fr"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

from pipelite.baseobjs.BODataSource import BODataSource 
import pipelite.constants as C
import os
from pipelite.plDataset import plDataset


# json validation Configuration 
CFGFILES_DSOBJECT = "csvFileDS.json"
CFGPARAMS_SEPARATOR = "separator"
CFGPARAMS_PATH = "path"
CFGPARAMS_FILENAME = "filename"
CFGPARAMS_ENCODING = "encoding"

class csvFileDS(BODataSource):

    def __init__(self, config, log):
        super().__init__(config, log)
        self.separator = C.DEFCSVSEP
        self.filename = C.EMPTY
        self.encoding = C.ENCODING

    @property
    def parametersValidationFile(self):
        return self.getResourceFile(package=C.RESOURCE_PKGFOLDER_DATASOURCES, 
                                    file=CFGFILES_DSOBJECT)

    def initialize(self, cfg) -> bool:
        """ initialize and check all the needed configuration parameters
            A CSV Extractor/Loader must have:
                * A filename
                * A separator
                * A path name
                * An Encoding type
                params['separator']
        Args:
            cfg (objConfig) : params for the data source.
                example: {'separator': ',', 'filename': 'test2.csv', 'path': '/tests/data/', 'encoding': 'utf-8'}
        Returns:
            bool: False if error
        """
        try:
            self.separator = cfg.getParameter(CFGPARAMS_SEPARATOR, C.EMPTY)
            self.filename = os.path.join(cfg.getParameter(CFGPARAMS_PATH, C.EMPTY), 
                                         cfg.getParameter(CFGPARAMS_FILENAME, C.EMPTY))
            self.encoding = cfg.getParameter(CFGPARAMS_ENCODING, C.EMPTY)
            # Checks ...
            if (self.objtype == C.PLJSONCFG_EXTRACTOR):
                if (not os.path.isfile(self.filename)):
                    raise Exception("The file {} does not exist or is not accessible.".format(self.filename))
            return True
        except Exception as e:
            self.log.error("{}".format(e))
            return False
    
    def read(self) -> plDataset:
        """ Returns all the data in a DataFrame format
        Returns:
            pd.DataFrame(): dataset read
        """
        try:
            self.log.info("Extract the Dataset from the file: {}".format(self.filename))
            dsExtract = plDataset(self.config, self.log)
            dsExtract.read_csv(filename=self.filename, 
                                 encoding=self.encoding, 
                                 separator=self.separator)
            return dsExtract
        except Exception as e:
            self.log.error("Error while reading the file: {}".format(e))
            return super().extract()

    def write(self, dataset) -> bool:
        """ write the dataset in the datasource
        Returns:
            int: Number of data rows loaded
        """
        try:
            self.log.info("Load the Dataset into the file: {}".format(self.filename))
            dataset.write_csv(filename=self.filename, 
                                  encoding=self.encoding,
                                  separator=self.separator)
            return True
        except Exception as e:
            self.log.error("Error while writing the file: {}".format(e))
            return False