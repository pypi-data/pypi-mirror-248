_U='already exists'
_T='status'
_S='database_name'
_R='table_catalog'
_Q='table_type'
_P='table_name'
_O='table_schema'
_N='^\\s*SHOW\\s+.*OBJECTS'
_M='FUNCTION'
_L='schema_name'
_K='text'
_J='TABLE'
_I='length'
_H='nullable'
_G='scale'
_F='precision'
_E='kind'
_D=None
_C='type'
_B=True
_A='name'
import calendar,datetime,json,re
from abc import ABC,abstractmethod
from localstack.utils.objects import get_all_subclasses
from sqlglot import exp,parse_one
from snowflake_local.engine.models import Query
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.server.conversions import to_pyarrow_table_bytes_b64
from snowflake_local.server.models import QueryResponse
class QueryResultPostprocessor(ABC):
	def should_apply(A,query,result):return _B
	@abstractmethod
	def apply(self,query,result):0
class FixShowSchemasResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*SHOW\\s+.*SCHEMAS',query.original_query,flags=re.I))
	def apply(A,query,result):_replace_dict_value(result.data.rowtype,_A,_L,_A)
class FixShowObjectsResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match(_N,query.original_query,flags=re.I))
	def apply(B,query,result):A=result;_replace_dict_value(A.data.rowtype,_A,_O,_L);_replace_dict_value(A.data.rowtype,_A,_P,_A);_replace_dict_value(A.data.rowtype,_A,_Q,_E);_replace_dict_value(A.data.rowtype,_A,_R,_S)
class FixShowTablesResult(QueryResultPostprocessor):
	def should_apply(B,query,result):
		A=query.original_query
		if re.match('^\\s*SHOW\\s+.*(TABLES|OBJECTS)',A,flags=re.I):return _B
		if re.search('\\s+FROM\\s+information_schema\\s*\\.\\s*schemata\\s+',A,flags=re.I):return _B
		return False
	def apply(H,query,result):
		B=result;from snowflake_local.engine.postgres.db_engine_postgres import State;B.data.rowtype.insert(0,{_A:'created_on',_F:0,_G:3,_C:'timestamp_ltz',_H:_B,_I:_D});_replace_dict_value(B.data.rowtype,_A,_O,_L);_replace_dict_value(B.data.rowtype,_A,_P,_A);_replace_dict_value(B.data.rowtype,_A,_Q,_E);_replace_dict_value(B.data.rowtype,_A,_R,_S);B.data.rowtype.insert(1,B.data.rowtype.pop(3));C=re.match(_N,query.original_query,flags=re.I)
		if C:B.data.rowtype.insert(2,{_A:_E,_F:_D,_G:_D,_C:_K,_H:_B,_I:_D})
		for A in B.data.rowset:
			A.insert(0,'0')
			if len(A)<4:continue
			A.insert(1,A.pop(3));A[1]=A[1].upper();A[2]=A[2].upper();A[3]=A[3].upper();D=State.identifier_overrides.find_match(A[2],schema=A[3],obj_name=A[1])
			if D:
				E,F,G=D
				if G:A[1]=G
				elif F:A[3]=F
				elif E:A[2]=E
			if C:A.insert(2,_J)
class FixCreateEntityResult(QueryResultPostprocessor):
	def should_apply(A,query,result):B=A._get_created_entity_type(query.original_query);return B in(_J,_M)
	def apply(E,query,result):
		D=result;B=query;C=E._get_created_entity_type(B.original_query);F={_J:'Table',_M:'Function'};G=F.get(C)
		if C==_J:A=_get_table_from_creation_query(B.original_query);A=A and A.upper()
		elif C==_M:H=_parse_snowflake_query(B.original_query);I=H.this;A=str(I.this).upper()
		else:A='test'
		D.data.rowset.append([f"{G} {A} successfully created."]);D.data.rowtype.append({_A:_T,_C:_K,_I:-1,_F:0,_G:0,_H:_B})
	def _get_created_entity_type(B,query):
		A=_parse_snowflake_query(query)
		if isinstance(A,exp.Create):return A.args.get(_E)
class FixDropTableResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_table_from_drop_query(query.original_query))
	def apply(C,query,result):A=result;B=_get_table_from_drop_query(query.original_query);A.data.rowset.append([f"{B} successfully dropped."]);A.data.rowtype.append({_A:_T,_C:_K,_I:-1,_F:0,_G:0,_H:_B})
class HandleDropDatabase(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(_get_database_from_drop_query(query.original_query))
	def apply(C,query,result):A=query;B=_get_database_from_drop_query(A.original_query);State.initialized_dbs=[A for A in State.initialized_dbs if A.lower()!=B.lower()];A.session.database=_D;A.session.schema=_D
class FixAlreadyExistsErrorResponse(QueryResultPostprocessor):
	def should_apply(B,query,result):A=result;return not A.success and _U in(A.message or'')
	def apply(C,query,result):
		A=result
		def B(match):return f"SQL compilation error:\nObject '{match.group(1).upper()}' already exists."
		A.message=re.sub('.*database \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*relation \\"(\\S+)\\".+',B,A.message);A.message=re.sub('.*function \\"(\\S+)\\".+',B,A.message)
class FixInsertQueryResult(QueryResultPostprocessor):
	def should_apply(A,query,result):return bool(re.match('^\\s*INSERT\\s+.+',query.original_query,flags=re.I))
	def apply(B,query,result):A=result;A.data.rowset=[[len(A.data.rowset)]];A.data.rowtype=[{_A:'count',_C:'integer',_I:-1,_F:0,_G:0,_H:_B}]
class UpdateSessionAfterCreatingDatabase(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+DATABASE(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.database=C.group(2);A.session.schema=_D
class UpdateSessionAfterCreatingSchema(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+SCHEMA(\\s+IF\\s+NOT\\s+EXISTS)?\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):A=query;C=B.REGEX.match(A.original_query);A.session.schema=C.group(2)
class AdjustQueryResultFormat(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('.+FROM\\s+@',query.original_query,flags=re.I);A.data.queryResultFormat='arrow'if B else'json'
		if B:A.data.rowsetBase64=to_pyarrow_table_bytes_b64(A);A.data.rowset=[];A.data.rowtype=[]
class AdjustColumnTypes(QueryResultPostprocessor):
	TYPE_MAPPINGS={'UNKNOWN':'TEXT','VARCHAR':'TEXT'}
	def apply(C,query,result):
		for A in result.data.rowtype:
			D=A.get(_C,'');B=C.TYPE_MAPPINGS.get(D)
			if B:A[_C]=B
class ReturnDescribeTableError(QueryResultPostprocessor):
	def apply(C,query,result):
		A=result;B=re.match('desc(?:ribe)?\\s+.+',query.original_query,flags=re.I)
		if B and not A.data.rowset:A.success=False
class IgnoreErrorForExistingEntity(QueryResultPostprocessor):
	REGEX=re.compile('^\\s*CREATE.*\\s+(\\S+)(\\s+IF\\s+NOT\\s+EXISTS)\\s+(\\S+)',flags=re.I)
	def should_apply(A,query,result):return bool(A.REGEX.match(query.original_query))
	def apply(B,query,result):
		A=result
		if not A.success and _U in(A.message or''):A.success=_B;A.data.rowtype=[];A.data.rowset=[]
class AddDefaultResultIfEmpty(QueryResultPostprocessor):
	def should_apply(B,query,result):
		A=_parse_snowflake_query(query.original_query)
		if isinstance(A,exp.AlterTable):return _B
		return isinstance(A,exp.Command)and str(A.this).upper()=='ALTER'
	def apply(B,query,result):
		A=result
		if not A.data.rowtype:A.data.rowtype=[{_A:'?column?',_C:_K,_I:-1,_F:0,_G:0,_H:_B}]
		A.data.rowset=[('Statement executed successfully.',)]
class EncodeComplexTypesInResults(QueryResultPostprocessor):
	def apply(D,query,result):
		for A in result.data.rowset:
			for(C,B)in enumerate(A):
				if isinstance(B,(dict,list)):A[C]=json.dumps(B)
class ConvertTimestampResults(QueryResultPostprocessor):
	def apply(L,query,result):
		D=result
		for(E,C)in enumerate(D.data.rowtype):
			B=str(C.get(_C)).upper();F='TIMESTAMP','TIMESTAMP WITHOUT TIME ZONE';G='TIMESTAMP WITH TIME ZONE',;H='DATE',
			if B in F:C[_C]='TIMESTAMP_NTZ'
			if B in G:C[_C]='TIMESTAMP_TZ'
			I=B in H
			if B in F+G+H:
				for J in D.data.rowset:
					A=J[E]
					if I:K=calendar.timegm(A.timetuple());A=datetime.datetime.utcfromtimestamp(K)
					if isinstance(A,datetime.datetime):A=A.replace(tzinfo=datetime.timezone.utc)
					A=int(A.timestamp())
					if I:A=A/24/60/60
					J[E]=str(int(A))
def apply_post_processors(query,result):
	B=result;A=query
	for D in get_all_subclasses(QueryResultPostprocessor):
		C=D()
		if C.should_apply(A,result=B):C.apply(A,result=B)
def _replace_dict_value(values,attr_key,attr_value,attr_value_replace):
	A=attr_key;B=[B for B in values if B[A]==attr_value]
	if B:B[0][A]=attr_value_replace
def _get_table_from_creation_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Create)or A.args.get(_E)!=_J:return
	B=A.this;C=B.this;D=C.this;E=getattr(D,'this',_D);return E
def _get_table_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_E)!=_J:return
	B=A.this;C=B.this;D=C.this;return D
def _get_database_from_drop_query(query):
	A=_parse_snowflake_query(query)
	if not isinstance(A,exp.Drop)or A.args.get(_E)!='DATABASE':return
	B=A.this;C=B.this;D=C.this;return D
def _parse_snowflake_query(query):
	try:return parse_one(query,read='snowflake')
	except Exception:return