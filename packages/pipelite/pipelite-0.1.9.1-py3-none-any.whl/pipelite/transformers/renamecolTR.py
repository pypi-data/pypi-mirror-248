__author__ = "datacorner.fr"
__email__ = "admin@datacorner.fr"
__license__ = "MIT"

import pipelite.constants as C
from pipelite.baseobjs.BOTransformer import BOTransformer
from pipelite.plDatasets import plDatasets
import re

CFGFILES_DSOBJECT = "renamecolTR.json"
PARAM_COLUMN = "column-name"
PARAM_NEW = "new-name"

class renamecolTR(BOTransformer):

    def __init__(self, config, log):
        super().__init__(config, log)
        self.columnName = C.EMPTY
        self.newName = C.EMPTY

    def initialize(self, params) -> bool:
        """ Initialize and makes some checks (params) for that transformer
        Args:
            params (json): parameters
        Returns:
            bool: False if error
        """
        try:
            self.columnName = params.getParameter(PARAM_COLUMN)
            self.newName = params.getParameter(PARAM_NEW)
            return True
        except Exception as e:
            self.log.error("{}".format(str(e)))
            return False
        
    @property
    def parametersValidationFile(self):
        return self.getResourceFile(package=C.RESOURCE_PKGFOLDER_TRANSFORMERS, 
                                    file=CFGFILES_DSOBJECT)
    
    def process(self, dsTransformerInputs) -> plDatasets:
        """ rename the column in all datasets configured for this transformation
        Args:
            inputDataFrames (etlDatasets): multiple dataset in a collection
        Returns:
            etlDatasets: modified dataset
        """
        i=0
        for dsItem in dsTransformerInputs:  # go through each dataset in entry
            dsItem.renameColumn(self.columnName,self.newName)
            dsItem.id = self.dsOutputs[i]
            i+=1
        return dsTransformerInputs