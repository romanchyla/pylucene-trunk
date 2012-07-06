# ====================================================================
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ====================================================================

import os

from lucene import \
    Document, Field, IndexWriter, StandardAnalyzer, IntField, \
    SimpleDateFormat, Version, SimpleFSDirectory, File, DateTools, \
    IndexWriterConfig, LogMergePolicy

# date culled from LuceneInAction.zip archive from Manning site
samplesModified = SimpleDateFormat('yyyy-MM-dd').parse('2004-12-02')


class TestDataDocumentHandler(object):

    def createIndex(cls, dataDir, indexDir, useCompound):

        indexDir = SimpleFSDirectory(File(indexDir))
        writer = IndexWriter(indexDir, IndexWriterConfig(Version.LUCENE_CURRENT,
                             StandardAnalyzer(Version.LUCENE_CURRENT)))
        config = writer.getConfig()
        mp = config.getMergePolicy()
        
        if (LogMergePolicy.instance_(mp)):
            mp.setUseCompoundFile(useCompound)

        for dir, dirnames, filenames in os.walk(dataDir):
            for filename in filenames:
                if filename.endswith('.properties'):
                    cls.indexFile(writer, os.path.join(dir, filename), dataDir)

        writer.commit()
        writer.close()

    def indexFile(cls, writer, path, baseDir):
        
        input = file(path)
        props = {}
        while True:
            line = input.readline().strip()
            if not line:
                break
            name, value = line.split('=', 1)
            props[name] = value.decode('unicode-escape')
        input.close()

        doc = Document()

        # category comes from relative path below the base directory
        category = os.path.dirname(path)[len(baseDir):]
        if os.path.sep != '/':
            category = category.replace(os.path.sep, '/')

        isbn = props['isbn']
        title = props['title']
        author = props['author']
        url = props['url']
        subject = props['subject']
        pubmonth = props['pubmonth']

        print title.encode('utf8')
        print author.encode('utf-8')
        print subject.encode('utf-8')
        print category.encode('utf-8')
        print "---------"

        ft_analyzed = FieldType(TextField.TYPE_STORED)
        ft_analyzed.setIndexed(True)
        ft_analyzed.setStored(True)
        ft_analyzed.setTokenized(True)
        ft_analyzed.setStoreTermVectorOffsets(True)
        ft_analyzed.setStoreTermVectorPositions(True)
        ft_analyzed.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS_AND_OFFSETS)
        
        ft_not_analyzed = FieldType(StringField.TYPE_STORED);
        ft.setOmitNorms(False);
        
        doc.add(Field("isbn", isbn,
                      ft_not_analyzed))
        doc.add(Field("category", category,
                      ft_not_analyzed))
        doc.add(Field("title", title,
                      ft))  #Field.Store.YES, Field.Index.ANALYZED,
                            #Field.TermVector.WITH_POSITIONS_OFFSETS
        doc.add(Field("title2", title.lower(),
                      Field.Store.YES, Field.Index.NOT_ANALYZED_NO_NORMS,
                      Field.TermVector.WITH_POSITIONS_OFFSETS))

        # split multiple authors into unique field instances
        authors = author.split(',')
        for a in authors:
            doc.add(Field("author", a,
                          Field.Store.YES, Field.Index.NOT_ANALYZED,
                          Field.TermVector.WITH_POSITIONS_OFFSETS))

        doc.add(Field("url", url,
                      Field.Store.YES,
                      Field.Index.NOT_ANALYZED_NO_NORMS))
        doc.add(Field("subject", subject,
                      Field.Store.NO, Field.Index.ANALYZED,
                      Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(IntField("pubmonth", int(pubmonth), Field.Store.YES))

        d = DateTools.stringToDate(pubmonth)
        d = int(d.getTime() / (1000 * 3600 * 24.0))
        doc.add(IntField("pubmonthAsDay", d, Field.Store.NO))

        doc.add(Field("contents", ' '.join([title, subject, author, category]),
                      Field.Store.NO, Field.Index.ANALYZED,
                      Field.TermVector.WITH_POSITIONS_OFFSETS))

        doc.add(Field("path", path,
                      Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("modified", DateTools.dateToString(samplesModified),
                      Field.Store.YES, Field.Index.NOT_ANALYZED))

        writer.addDocument(doc)

    createIndex = classmethod(createIndex)
    indexFile = classmethod(indexFile)
