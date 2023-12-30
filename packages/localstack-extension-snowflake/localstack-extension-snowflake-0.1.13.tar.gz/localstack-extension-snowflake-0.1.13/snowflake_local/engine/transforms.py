_Q='OBJECT_CONSTRUCT'
_P='javascript'
_O='DATABASE'
_N='is_string'
_M='SCHEMA'
_L='expression'
_K=False
_J='alias'
_I='postgres'
_H='TABLE'
_G='properties'
_F='TEXT'
_E='expressions'
_D=None
_C='kind'
_B=True
_A='this'
import json,logging,re,textwrap
from typing import Callable
from aenum import extend_enum
from localstack.utils.files import chmod_r,new_tmp_file,save_file
from localstack.utils.numbers import is_number
from localstack.utils.strings import short_uid
from sqlglot import TokenType,exp,parse_one,tokens
from sqlglot.dialects import Postgres,Snowflake
from snowflake_local.engine.db_engine import DBEngine,get_db_engine
from snowflake_local.engine.models import Query
from snowflake_local.engine.session import APP_STATE
LOG=logging.getLogger(__name__)
TYPE_MAPPINGS={'VARIANT':_F,'OBJECT':_F,'STRING':_F,'UNKNOWN':_F}
ACCOUNT_ID='TESTACC123'
class QueryTransforms:
	def apply(C,query):
		A=query;B=parse_one(A.query,read='snowflake')
		for D in C.get_transformers():B=B.transform(D,query=A)
		A.query=B.sql(dialect=_I);return A
	def get_transformers(A):return[remove_transient_keyword,remove_if_not_exists,remove_create_or_replace,replace_unknown_types,replace_unknown_user_config_params,replace_create_schema,replace_identifier_function,insert_create_table_placeholder,replace_json_field_access,replace_db_references,replace_current_warehouse,replace_current_account,update_function_language_identifier,convert_function_args_to_lowercase,create_tmp_table_for_result_scan,remove_table_cluster_by,insert_session_id]
class QueryTransformsPostgres(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[pg_replace_describe_table,pg_replace_show_schemas_or_tables,pg_replace_show_objects,pg_replace_questionmark_placeholder,pg_replace_object_construct,pg_rename_reserved_keyword_functions,pg_return_inserted_items,pg_remove_table_func_wrapper,pg_convert_array_agg_params,pg_convert_array_function_arg_types,pg_add_alias_to_subquery,pg_convert_timestamp_types,pg_track_case_sensitive_identifiers,pg_cast_params_for_string_agg,pg_cast_params_for_to_date,pg_get_available_schemas]
class QueryTransformsDuckDB(QueryTransforms):
	def get_transformers(A):return super().get_transformers()+[ddb_replace_create_database,pg_replace_show_schemas_or_tables,pg_replace_show_objects]
def remove_transient_keyword(expression,**E):
	A=expression
	if not _is_create_table_expression(A):return A
	B=A.copy()
	if B.args[_G]:
		C=B.args[_G].expressions;D=exp.TransientProperty()
		if D in C:C.remove(D)
	return B
def remove_if_not_exists(expression,**D):
	C='exists';A=expression
	if not isinstance(A,exp.Create):return A
	B=A.copy()
	if B.args.get(C):B.args[C]=_K
	return B
def remove_create_or_replace(expression,query):
	I='replace';D=query;A=expression
	if not isinstance(A,exp.Create):return A
	E=try_get_db_engine()
	if A.args.get(I):
		B=A.copy();B.args[I]=_K;F=str(B.args.get(_C)).upper()
		if E and F in(_H,'FUNCTION'):
			G=str(B.this.this);C=Query(query=f"DROP {F} IF EXISTS {G}");C.session=D.session;C.database=D.database;H=G.split('.')
			if len(H)>=3:C.database=H[0]
			E.execute_query(C)
		return B
	return A
def replace_unknown_types(expression,**E):
	B=expression
	for(D,C)in TYPE_MAPPINGS.items():
		C=getattr(exp.DataType.Type,C.upper());A=B
		if isinstance(A,exp.Alias):A=A.this
		if isinstance(A,exp.Cast)and A.to==exp.DataType.build(D):A.args['to']=exp.DataType.build(C)
		if isinstance(B,exp.ColumnDef):
			if B.args.get(_C)==exp.DataType.build(D):B.args[_C]=exp.DataType.build(C)
	return B
def replace_unknown_user_config_params(expression,**E):
	A=expression
	if isinstance(A,exp.Command)and str(A.this).upper()=='ALTER':
		C=str(A.expression).strip();D='\\s*USER\\s+\\w+\\s+SET\\s+\\w+\\s*=\\s*[\'\\"]?(.*?)[\'\\"]?\\s*$';B=re.match(D,C,flags=re.I)
		if B:return parse_one(f"SELECT '{B.group(1)}'")
	return A
def replace_create_schema(expression,query):
	A=expression
	if not isinstance(A,exp.Create):return A
	A=A.copy();B=A.args.get(_C)
	if str(B).upper()==_M:query.database=A.this.db;A.this.args['db']=_D
	return A
def insert_create_table_placeholder(expression,query):
	A=expression
	if not _is_create_table_expression(A):return A
	if isinstance(A.this.this,exp.Placeholder)or str(A.this.this)=='?':A=A.copy();A.this.args[_A]=query.params.pop(0)
	return A
def replace_identifier_function(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='IDENTIFIER'and A.expressions:B=A.expressions[0].copy();B.args[_N]=_K;return B
	return A
def replace_json_field_access(expression,**K):
	A=expression
	if not A.parent_select:return A
	if A.find_ancestor(exp.From):return A
	if not isinstance(A,(exp.Dot,exp.Bracket)):return A
	H=A.find(exp.Bracket)
	if isinstance(A.parent,exp.Select)and not H:return A.copy()
	F=_D;C=A;G=[]
	while hasattr(C,_A):
		if isinstance(C,(exp.Column,exp.Identifier)):F=C;break
		I=C.name or C.output_name;G.insert(0,I);C=C.this
	if not F:return A
	B=''
	for D in G:
		if is_number(D):B+=f"[{D}]"
		else:B+=f".{D}"
	B=B.strip('.')
	if not B.startswith('.'):B=f".{B}"
	if not B.startswith('$'):B=f"${B}"
	class J(exp.Binary,exp.Func):_sql_names=['get_path']
	E=J();E.args[_A]=C;E.args[_L]=f"'{B}'";return E
def replace_db_references(expression,query):
	E='catalog';C=query;A=expression;D=A.args.get(E)
	if isinstance(A,exp.Table)and A.args.get('db')and D:C.database=D.this;A.args[E]=_D
	if isinstance(A,exp.UserDefinedFunction):
		B=str(A.this).split('.')
		if len(B)==3:A.this.args[_A]=B[1];C.database=B[0]
	return A
def replace_current_warehouse(expression,query):
	C=query;A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='CURRENT_WAREHOUSE':B=exp.Literal();B.args[_A]=C.session and C.session.warehouse or'TEST';B.args[_N]=_B;return B
	return A
def replace_current_account(expression,**D):
	A=expression;C=['CURRENT_ACCOUNT','CURRENT_ACCOUNT_NAME']
	if isinstance(A,exp.Func)and str(A.this).upper()in C:B=exp.Literal();B.args[_A]=ACCOUNT_ID;B.args[_N]=_B;return B
	return A
def update_function_language_identifier(expression,**Q):
	L='python';A=expression;M={_P:'plv8',L:'plpython3u'}
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		E=A.args[_G];C=E.expressions;B=[A for A in C if isinstance(A,exp.LanguageProperty)]
		if not B:F=exp.LanguageProperty();F.args[_A]='SQL';C.append(F);return A
		G=str(B[0].this).lower();N=G==L
		for(O,H)in M.items():
			if G!=O:continue
			if isinstance(B[0].this,exp.Identifier):B[0].this.args[_A]=H
			else:B[0].args[_A]=H
		I=[];J=[A for A in C if str(A.this).lower()=='handler']
		for K in C:
			if isinstance(K,(exp.LanguageProperty,exp.ReturnsProperty)):I.append(K)
		E.args[_E]=I
		if N and J:P=J[0].args['value'].this;D=textwrap.dedent(A.expression.this);D=D+f"\nreturn {P}(*args)";A.expression.args[_A]=D
	return A
def convert_function_args_to_lowercase(expression,**H):
	A=expression
	if isinstance(A,exp.Create)and isinstance(A.this,exp.UserDefinedFunction):
		D=A.args[_G].expressions;B=[A for A in D if isinstance(A,exp.LanguageProperty)];B=str(B[0].this).lower()if B else _D
		if B not in(_P,'plv8'):return A
		E=[A for A in A.this.expressions if isinstance(A,exp.ColumnDef)]
		for F in E:
			if not A.expression:continue
			C=str(F.this);G=A.expression.this;A.expression.args[_A]=G.replace(C.upper(),C.lower())
	return A
def create_tmp_table_for_result_scan(expression,**K):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()=='RESULT_SCAN':
		E=A.expressions[0];F=E.this;B=APP_STATE.queries.get(F)
		if not B:LOG.info("Unable to find state for query ID '%s'",F);return A
		C=new_tmp_file();G=json.dumps(B.result.rows);save_file(C,G);chmod_r(C,511);E.args[_A]=C
		def H(idx,col):B=col;A=B.type_name.upper();A=TYPE_MAPPINGS.get(A)or A;return f"{f'_col{idx+1}'if B.name=='?column?'else B.name} {A}"
		D=exp.Alias();D.args[_A]=A;I=B.result.columns;J=', '.join([H(A,B)for(A,B)in enumerate(I)]);D.args[_J]=f"({J})";return D
	return A
def remove_table_cluster_by(expression,**F):
	A=expression
	if _is_create_table_expression(A):C=A.args[_G]or[];D=[type(A)for A in C if not isinstance(A,exp.Cluster)];A.args[_G]=D
	elif isinstance(A,exp.Command)and A.this=='ALTER':
		E='(.+)\\s*CLUSTER\\s+BY([\\w\\s,]+)(.*)';B=re.sub(E,'\\1\\3',A.expression,flags=re.I);A.args[_L]=B
		if re.match('\\s*TABLE\\s+\\w+',B,flags=re.I):return parse_one('SELECT NULL',read=_I)
	return A
def insert_session_id(expression,query):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='current_session':return exp.Literal(this=query.session.session_id,is_string=_B)
	return A
def pg_replace_describe_table(expression,**G):
	A=expression
	if not isinstance(A,exp.Describe):return A
	C=A.args.get(_C)
	if str(C).upper()==_H:B=A.this.name;D=f"'{B}'"if B else'?';E=f"SELECT * FROM information_schema.columns WHERE table_name={D}";F=parse_one(E,read=_I);return F
	return A
def pg_replace_show_schemas_or_tables(expression,**H):
	D='tables';A=expression
	if not isinstance(A,exp.Command):return A
	E=str(A.this).upper();B=str(A.args.get(_L)).strip().lower();B=B.removeprefix('terse').strip();C=_D
	if B.startswith(D):C=D
	if B.startswith('schemas'):C='schemata'
	if E=='SHOW'and C:F=f"SELECT * FROM information_schema.{C}";G=parse_one(F,read=_I);return G
	return A
def pg_replace_show_objects(expression,**H):
	A=expression
	if not isinstance(A,exp.Command):return A
	E=str(A.this).upper();B=str(A.args.get(_L)).strip().lower();B=B.removeprefix('terse').strip()
	if E=='SHOW'and B.startswith('objects'):
		C='SELECT * FROM information_schema.tables';F='^\\s*objects\\s+(\\S+)\\.(\\S+)(.*)';D=re.match(F,B)
		if D:C+=f" WHERE table_schema = '{D.group(2)}'"
		G=parse_one(C,read=_I);return G
	return A
def pg_replace_questionmark_placeholder(expression,**B):
	A=expression
	if isinstance(A,exp.Placeholder):return exp.Literal(this='%s',is_string=_K)
	return A
def pg_replace_object_construct(expression,**G):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).upper()==_Q:
		class D(exp.Func):_sql_names=['TO_JSON_STR'];arg_types={_A:_B,_E:_B}
		B=A.args[_E]
		for C in range(1,len(B),2):E=B[C];B[C]=F=D();F.args[_E]=E
	return A
def pg_rename_reserved_keyword_functions(expression,**E):
	A=expression
	if isinstance(A,exp.Func)and isinstance(A.this,str):
		B={'current_role':'get_current_role'}
		for(C,D)in B.items():
			if str(A.this).lower()==C:A.args[_A]=D
	return A
def pg_return_inserted_items(expression,**B):
	A=expression
	if isinstance(A,exp.Insert):A.args['returning']=' RETURNING 1'
	return A
def pg_remove_table_func_wrapper(expression,**B):
	A=expression
	if isinstance(A,exp.Table)and str(A.this.this).upper()==_H:return A.this.expressions[0]
	return A
def pg_convert_array_agg_params(expression,**F):
	E='from';B=expression
	if isinstance(B,exp.Select):
		C=[A for A in B.expressions if isinstance(A,exp.WithinGroup)];A=_D
		if C:
			if isinstance(C[0].this,exp.ArrayAgg):C[0].args[_A]='ARRAY_AGG_ORDERED()';A=B.args.get(E)
		else:
			D=[A for A in B.expressions if isinstance(A,exp.ArrayAgg)]
			if D:
				A=B.args.get(E)
				if isinstance(A.this,exp.Values)and not A.this.args.get(_J):D[0].args[_A]='_tmp_col1'
		if A and isinstance(A.this,exp.Values)and not A.this.args.get(_J):A.this.args[_J]='_tmp_table(_tmp_col1)'
	return B
def pg_convert_array_function_arg_types(expression,**J):
	F='array_cat';A=expression
	class D(exp.Func):_sql_names=['TO_VARIANT'];arg_types={_A:_B,_E:_B}
	G='array_append',F
	if isinstance(A,exp.Func):
		E=str(A.this).lower()
		if isinstance(A,exp.ArrayConcat):E=F
		for H in G:
			if E!=H:continue
			for(I,B)in enumerate(A.expressions):A.expressions[I]=C=D();C.args[_E]=B
			if isinstance(A,exp.ArrayConcat):B=A.this;A.args[_A]=C=D();C.args[_E]=B
	return A
def pg_add_alias_to_subquery(expression,**B):
	A=expression
	if isinstance(A,exp.Subquery):
		if not A.alias and A.parent_select:A.args[_J]=f"_tmp{short_uid()}"
	return A
def pg_convert_timestamp_types(expression,**D):
	A=expression
	if isinstance(A,exp.ColumnDef):
		B=str(A.args.get(_C,'')).upper()
		if B=='TIMESTAMP':A.args[_C]=C=exp.Identifier();C.args[_A]='TIMESTAMP WITHOUT TIME ZONE'
	return A
def pg_track_case_sensitive_identifiers(expression,query):
	B=expression;from snowflake_local.engine.postgres.db_state import State
	if isinstance(B,exp.Create):
		C=str(B.args.get(_C)).upper()
		if C in(_O,_M,_H):
			A=B
			while isinstance(A.this,exp.Expression):A=A.this
			if A.args.get('quoted'):D=A.this if C==_O else query.database;E=A.this if C==_M else _D;F=A.this if C==_H else _D;G=D,E,F;State.identifier_overrides.entries.append(G)
	return B
def pg_cast_params_for_string_agg(expression,**H):
	F='separator';A=expression
	if isinstance(A,exp.GroupConcat):
		C=A.this;B=A;E=''
		if isinstance(C,exp.Distinct):C=A.this.expressions[0];B=A.this.expressions
		if not isinstance(C,exp.Cast):
			D=exp.Cast();D.args[_A]=C;D.args['to']=exp.DataType.build(_F)
			if isinstance(B,list):
				B[0]=D
				if len(B)>1:G=B.pop(1);E=str(G.this)
			else:B.args[_A]=D
		if A.args.get(F)is _D:A.args[F]=exp.Literal(this=E,is_string=_B)
	return A
def pg_cast_params_for_to_date(expression,**C):
	A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='to_date':
		A=A.copy();B=exp.Cast();B.args[_A]=A.expressions[0];B.args['to']=exp.DataType.build(_F);A.expressions[0]=B
		if len(A.expressions)<=1:LOG.info('Auto-detection of date format in TO_DATE(..) not yet supported');A.expressions.append(exp.Literal(this='YYYY/MM/DD',is_string=_B))
	return A
def pg_get_available_schemas(expression,query):
	B=query;A=expression
	if isinstance(A,exp.Func)and str(A.this).lower()=='current_schemas':
		C=try_get_db_engine()
		if C:from snowflake_local.engine.postgres.db_engine_postgres import DEFAULT_DATABASE as D;E=Query(query='SELECT schema_name FROM information_schema.schemata',database=B.database);F=B.database or D;G=C.execute_query(E);H=[f"{F}.{A[0]}".upper()for A in G.rows];return exp.Literal(this=json.dumps(H),is_string=_B)
	return A
def ddb_replace_create_database(expression,**D):
	A=expression
	if isinstance(A,exp.Create)and str(A.args.get(_C)).upper()==_O:assert(C:=A.find(exp.Identifier)),f"No identifier in {A.sql}";B=C.this;return exp.Command(this='ATTACH',expression=exp.Literal(this=f"DATABASE ':memory:' AS {B}",is_string=_B),create_db_name=B)
	return A
def _is_create_table_expression(expression,**C):A=expression;return isinstance(A,exp.Create)and(B:=A.args.get(_C))and isinstance(B,str)and B.upper()==_H
def try_get_db_engine():
	try:return get_db_engine()
	except ImportError:return
def _patch_sqlglot():
	Snowflake.Parser.FUNCTIONS.pop(_Q,_D)
	for A in('ANYARRAY','ANYELEMENT'):
		extend_enum(TokenType,A,A);extend_enum(exp.DataType.Type,A,A);D=getattr(exp.DataType.Type,A);B=getattr(exp.DataType.Type,A);tokens.Tokenizer.KEYWORDS[A]=B
		for C in(Postgres,Snowflake):C.Parser.TYPE_TOKENS.add(B);C.Parser.ID_VAR_TOKENS.add(B);C.Parser.FUNC_TOKENS.add(B);C.Generator.TYPE_MAPPING[D]=A;C.Tokenizer.KEYWORDS[A]=B
_patch_sqlglot()