/* ====================================================================
 *   Licensed under the Apache License, Version 2.0 (the "License");
 *   you may not use this file except in compliance with the License.
 *   You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *   Unless required by applicable law or agreed to in writing, software
 *   distributed under the License is distributed on an "AS IS" BASIS,
 *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *   See the License for the specific language governing permissions and
 *   limitations under the License.
 * ====================================================================
 */

package org.apache.pylucene.queryparser.classic;

import java.util.List;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.search.Query;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.queryparser.classic.CharStream;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.util.Version;


public class PythonQueryParser extends QueryParser {

    private long pythonObject;

    public PythonQueryParser(Version version, String field, Analyzer analyzer)
    {
        super(version, field, analyzer);
    }

    public PythonQueryParser(CharStream stream)
    {
        super(stream);
    }

    public void pythonExtension(long pythonObject)
    {
        this.pythonObject = pythonObject;
    }
    public long pythonExtension()
    {
        return this.pythonObject;
    }

    public void finalize()
        throws Throwable
    {
        pythonDecRef();
    }

    public native void pythonDecRef();
    public native Query getBooleanQuery(List clauses, boolean disableCoord);
    public native Query getFuzzyQuery(String field, String termText,
                                      float minSimilarity);
    public native Query getPrefixQuery(String field, String termText);
    public native Query getRangeQuery(String field,
                                      String part1, String part2,
                                      boolean inclusive);
    public native Query getWildcardQuery(String field, String termText);

    public native Query getFieldQuery_quoted(String field, String queryText,
                                             boolean quoted);
    public native Query getFieldQuery_slop(String field, String queryText,
                                           int slop);

    public Query getFieldQuery_quoted_super(String field, String queryText,
                                            boolean quoted)
        throws ParseException
    {
        return super.getFieldQuery(field, queryText, quoted);
    }

    public Query getFieldQuery_slop_super(String field, String queryText,
                                          int slop)
        throws ParseException
    {
        return super.getFieldQuery(field, queryText, slop);
    }

    public Query getFieldQuery(String field, String queryText, boolean quoted)
    {
        return getFieldQuery_quoted(field, queryText, quoted);
    }

    public Query getFieldQuery(String field, String queryText, int slop)
    {
        return getFieldQuery_slop(field, queryText, slop);
    }
}
