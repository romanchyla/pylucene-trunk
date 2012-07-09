
from unittest import TestCase
from lucene import RAMDirectory, File, IndexWriter, IndexWriterConfig, \
    LimitTokenCountAnalyzer, WhitespaceAnalyzer, Version, IndexSearcher, \
    DirectoryReader

class PyLuceneTestCase(TestCase):
    

    def __init__(self, *args):
        super(PyLuceneTestCase, self).__init__(*args)
        self.TEST_VERSION = Version.LUCENE_CURRENT

    def setUp(self):
        self.directory = RAMDirectory()

    def tearDown(self):
        self.directory.close()
        
        
    def getWriter(self, directory=None, analyzer=None, open_mode=None):
        config = IndexWriterConfig(self.TEST_VERSION,
                    analyzer or LimitTokenCountAnalyzer(WhitespaceAnalyzer(Version.LUCENE_CURRENT), 10000)
                    )
        config.setOpenMode(open_mode or IndexWriterConfig.OpenMode.CREATE)
        return IndexWriter(directory or self.directory, config)
    
        
    def getSearcher(self, directory=None, reader=None):
        if reader is not None:
            return IndexSearcher(reader)
        return self.getReader(directory=directory)

    
    def getReader(self, directory=None):
        return DirectoryReader.open(directory or self.directory)