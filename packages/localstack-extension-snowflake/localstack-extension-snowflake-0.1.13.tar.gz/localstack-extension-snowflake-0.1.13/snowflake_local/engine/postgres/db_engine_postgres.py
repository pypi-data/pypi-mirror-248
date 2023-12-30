_C='VARCHAR'
_B='test'
_A='TEXT'
import atexit,json,logging,re,time
from localstack import config
from localstack.utils.net import get_free_tcp_port,wait_for_port_open
from localstack_ext.services.rds.engine_postgres import get_type_name
from localstack_ext.utils.postgresql import Postgresql
from snowflake_local.engine.db_engine import DBEngine
from snowflake_local.engine.models import Query,QueryResult,TableColumn
from snowflake_local.engine.packages import postgres_plv8_package
from snowflake_local.engine.postgres.db_state import State
from snowflake_local.engine.postprocess import _get_database_from_drop_query
from snowflake_local.engine.transforms import QueryTransformsPostgres
LOG=logging.getLogger(__name__)
PG_VARIANT_TYPE=_A
PG_VARIANT_COMPATIBLE_TYPES='JSONB','FLOAT','BIGINT','BOOLEAN',_A
PG_VARIANT_TYPES_AND_ARRAYS=PG_VARIANT_COMPATIBLE_TYPES+('FLOAT[]','INTEGER[]','BOOLEAN[]','TEXT[]')
BASIC_TYPES=_A,'DECIMAL','INTEGER'
DESCRIBE_TABLE_COL_ATTRS={'name':'column_name','type':'data_type','kind':"'COLUMN'",'null?':'is_nullable','default':'column_default'}
DEFAULT_DATABASE=_B
class DBEnginePostgres(DBEngine):
	def execute_query(F,query):
		A=_execute_query(query)
		if isinstance(A,list):return QueryResult(rows=A)
		if not A._context.columns:return QueryResult()
		B=list(A);B=[tuple(A)for A in B];D=QueryResult(rows=B)
		for C in A._context.columns:E=TableColumn(name=C['name'],type_name=get_pg_type_name(C['type_oid']),type_size=C['type_size']);D.columns.append(E)
		return D
	def prepare_query(B,query):A=QueryTransformsPostgres();return A.apply(query)
	def postprocess_query_result(F,query,result):
		C=query;A=result;B=(C.original_query or C.query or'').replace('\n',' ').strip();D=re.match('^DESC(RIBE)?\\s+TABLE.+',B,flags=re.I);E=re.match('\\s+information_schema\\s*\\.\\s*columns\\s+',B,flags=re.I)
		if D or E:A=_convert_describe_table_result_columns(B,A)
		return A
def _execute_query(query):
	A=query;G=_start_postgres();E=bool(_get_database_from_drop_query(A.original_query));C=A.query;B=None
	if A.session:
		if A.session.database:B=A.session.database
		if A.session.schema and A.session.schema!='public'and not E:
			D=A.session.schema
			if'.'in D:B,D=D.split('.')
			C=f"SET search_path TO {D}, public; \n{C}"
	B=A.database or B or DEFAULT_DATABASE
	if E:B=None
	else:B=B.lower();_define_util_functions(B)
	F=A.params or[];LOG.debug('Running query (DB %s): %s - %s',B,C,F);return G.run_query(C,*F,database=B)
def _start_postgres(user=_B,password=_B,database=_B):
	if not State.server:
		A=get_free_tcp_port();State.server=Postgresql(port=A,user=user,password=password,database=database,boot_timeout=30,include_python_venv_libs=True);time.sleep(1)
		try:B=20;wait_for_port_open(A,retries=B,sleep_time=.8)
		except Exception:raise Exception('Unable to start up Postgres process (health check failed after 10 secs)')
		def C():State.server.terminate()
		atexit.register(C)
	return State.server
def _define_util_functions(database):
	B=database
	if B in State.initialized_dbs:return
	State.initialized_dbs.append(B);C=State.server;C.run_query('CREATE EXTENSION IF NOT EXISTS plpython3u',database=B);_install_plv8_extension();C.run_query('CREATE EXTENSION IF NOT EXISTS plv8',database=B);A='\n    CREATE OR REPLACE FUNCTION load_data (\n       file_ref text,\n       file_format text\n    ) RETURNS SETOF RECORD\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        from snowflake_local.engine.extension_functions import load_data\n        return load_data(file_ref, file_format)\n    $$;\n    ';C.run_query(A,database=B)
	for E in range(10):F=', '.join([f"k{A} TEXT, v{A} TEXT"for A in range(E)]);G=', '.join([f"k{A}, v{A}"for A in range(E)]);A=f"""
        CREATE OR REPLACE FUNCTION object_construct ({F}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import object_construct
            return object_construct({G})
            $$;
        """;C.run_query(A,database=B)
	for D in PG_VARIANT_TYPES_AND_ARRAYS:A=f"""
        CREATE OR REPLACE FUNCTION to_variant (obj {D}) RETURNS {PG_VARIANT_TYPE}
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_variant
            return to_variant(obj)
        $$;
        """;C.run_query(A,database=B)
	for D in PG_VARIANT_COMPATIBLE_TYPES:A=f"""
        CREATE OR REPLACE FUNCTION to_json_str (obj {D}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_json_str
            return to_json_str(obj)
        $$;
        """;C.run_query(A,database=B)
	A=f"""
    CREATE OR REPLACE FUNCTION get_path (obj {PG_VARIANT_TYPE}, path TEXT) RETURNS TEXT
    LANGUAGE plpython3u IMMUTABLE
    AS $$
        from snowflake_local.engine.extension_functions import get_path
        return get_path(obj, path)
    $$;
    """;C.run_query(A,database=B);A=f"""
    CREATE OR REPLACE FUNCTION parse_json (obj TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE
    AS $$
        from snowflake_local.engine.extension_functions import parse_json
        return parse_json(obj)
    $$;
    """;C.run_query(A,database=B)
	for D in PG_VARIANT_COMPATIBLE_TYPES:A=f"""
        CREATE OR REPLACE FUNCTION to_char (obj {D}) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import to_char
            return to_char(obj)
        $$;
        """;C.run_query(A,database=B)
	A='\n    CREATE OR REPLACE FUNCTION result_scan (results_file TEXT) RETURNS SETOF RECORD\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        from snowflake_local.engine.extension_functions import result_scan\n        return result_scan(results_file)\n    $$;\n    ';C.run_query(A,database=B);A='\n        CREATE OR REPLACE FUNCTION array_append (_array TEXT, _entry TEXT) RETURNS TEXT\n        LANGUAGE plpython3u IMMUTABLE\n        AS $$\n            from snowflake_local.engine.extension_functions import array_append\n            return array_append(_array, _entry)\n        $$;\n        ';C.run_query(A,database=B);A='\n        CREATE OR REPLACE FUNCTION array_cat (_array1 TEXT, _array2 TEXT) RETURNS TEXT\n        LANGUAGE plpython3u IMMUTABLE\n        AS $$\n            from snowflake_local.engine.extension_functions import array_concat\n            return array_concat(_array1, _array2)\n        $$;\n        ';C.run_query(A,database=B);A='\n    CREATE OR REPLACE FUNCTION "system$snowpipe_streaming_migrate_channel_offset_token" (\n        tableName TEXT, channelName TEXT, offsetToken TEXT) RETURNS TEXT\n    LANGUAGE plpython3u IMMUTABLE\n    AS $$\n        # TODO: simply returning hardcoded value for now - may need to get adjusted over time\n        return \'{"responseMessage":"Success","responseCode":50}\'\n    $$;\n    ';C.run_query(A,database=B);A=f'''
    CREATE OR REPLACE FUNCTION "system$cancel_all_queries" (session TEXT) RETURNS {PG_VARIANT_TYPE}
    LANGUAGE plpython3u IMMUTABLE
    AS $$
        from snowflake_local.engine.extension_functions import cancel_all_queries
        return cancel_all_queries(session)
    $$;
    ''';C.run_query(A,database=B);_define_hardcoded_return_value_functions(database=B);_define_aggregate_functions(database=B)
def _define_hardcoded_return_value_functions(database):
	A='PUBLIC';B=State.server;C=['ACCOUNTADMIN','ORGADMIN',A,'SECURITYADMIN','SYSADMIN','USERADMIN'];D={'current_account':'TEST001','current_account_name':'TEST002','current_available_roles':json.dumps(C),'current_client':'test-client','current_ip_address':'127.0.0.1','current_organization_name':'TESTORG','current_region':'TEST_LOCAL','get_current_role':A,'current_role_type':'ROLE','current_secondary_roles':json.dumps({'roles':'','value':''})}
	for(E,F)in D.items():G=f"\n            CREATE OR REPLACE FUNCTION {E}() RETURNS TEXT LANGUAGE plpython3u IMMUTABLE AS\n            $$ return '{F}' $$;\n            ";B.run_query(G,database=database)
def _define_aggregate_functions(database):
	J='TIMESTAMP';I='NUMERIC';C=database;D=State.server
	for A in('arg_min','arg_max'):
		for(G,E)in enumerate((I,_A,J)):
			B=f"""
            CREATE OR REPLACE FUNCTION {A}_finalize_{G} (
               _result TEXT[]
            ) RETURNS {E}
            LANGUAGE plpython3u IMMUTABLE
            AS $$
                from snowflake_local.engine.extension_functions import arg_min_max_finalize
                return arg_min_max_finalize(_result)
            $$;
            """;D.run_query(B,database=C)
			for H in(I,J):B=f"""
                CREATE OR REPLACE FUNCTION {A}_aggregate (
                   _result TEXT[],
                   _input1 {E},
                   _input2 {H}
                ) RETURNS TEXT[]
                LANGUAGE plpython3u IMMUTABLE
                AS $$
                    from snowflake_local.engine.extension_functions import {A}_aggregate
                    return {A}_aggregate(_result, _input1, _input2)
                $$;
                CREATE AGGREGATE {A}({E}, {H}) (
                    INITCOND = '{{null,null}}',
                    STYPE = TEXT[],
                    SFUNC = {A}_aggregate,
                    FINALFUNC = {A}_finalize_{G}
                );
                """;D.run_query(B,database=C)
	for F in BASIC_TYPES:B=f"""
        CREATE OR REPLACE FUNCTION array_agg_aggregate (
           _result TEXT,
           _input1 {F}
        ) RETURNS TEXT
        LANGUAGE plpython3u IMMUTABLE
        AS $$
            from snowflake_local.engine.extension_functions import array_agg_aggregate
            return array_agg_aggregate(_result, _input1)
        $$;
        CREATE AGGREGATE array_agg_ordered(ORDER BY {F}) (
            STYPE = TEXT,
            SFUNC = array_agg_aggregate
        );
        CREATE AGGREGATE array_agg({F}) (
            STYPE = TEXT,
            SFUNC = array_agg_aggregate
        );
        """;D.run_query(B,database=C)
def _convert_describe_table_result_columns(query_str,result):
	A=result;F=[A.name for A in A.columns];E=list(DESCRIBE_TABLE_COL_ATTRS);A.columns=[]
	for G in E:A.columns.append(TableColumn(name=G,type_name=_C,type_size=128))
	for(H,I)in enumerate(A.rows):
		C=[]
		for J in E:
			D=DESCRIBE_TABLE_COL_ATTRS[J]
			if D.startswith("'"):C.append(D.strip("'"))
			else:K=dict(zip(F,I));B=K[D];B={'YES':'Y','NO':'N'}.get(B)or B;C.append(B)
		A.rows[H]=tuple(C)
	return A
def _install_plv8_extension():
	if config.is_in_docker:postgres_plv8_package.install()
def get_pg_type_name(scalar_type):
	A=scalar_type;C={'19':_C,'25':_C,'1114':'TIMESTAMP WITHOUT TIME ZONE','1184':'TIMESTAMP WITH TIME ZONE'};B=C.get(str(A))
	if B:return B
	return get_type_name(A)