_A=None
import datetime,json
from typing import Any,Callable
from localstack.utils.files import rm_rf
from localstack.utils.json import extract_jsonpath,json_safe
from localstack.utils.numbers import is_number
from localstack.utils.strings import to_str
AGG_COMPARABLE_TYPE=float|datetime.datetime
VARIANT=str
def load_data(file_ref,file_format):
	from snowflake_local.files.storage import FILE_STORAGE as D,FileRef as E;F=E.parse(file_ref);A=D.load_file(F);A=json.loads(to_str(A));G=A if isinstance(A,list)else[A];B=[]
	for C in G:
		if isinstance(C,dict):B.append({'_col1':json.dumps(C)})
		else:B.append(C)
	return B
def result_scan(file_path):
	A=file_path
	with open(A)as B:C=json.loads(B.read())
	try:rm_rf(A)
	except Exception:pass
	return C
def object_construct(*A,**E):
	B={}
	for C in range(0,len(A),2):D=A[C+1];B[A[C]]=json.loads(D)
	return json.dumps(B)
def to_json_str(obj):return json.dumps(obj)
def get_path(obj,path):
	C=obj;B=path
	if not B.startswith('.'):B=f".{B}"
	if not B.startswith('$'):B=f"${B}"
	if C is not _A and not isinstance(C,(list,dict)):C=_unwrap_variant_type(C,expected_type=(list,dict))
	A=extract_jsonpath(C,B)
	if A==[]:return''
	if is_number(A)and not isinstance(A,bool)and int(A)==A:A=int(A)
	A=json.dumps(A);return A
def to_variant(obj):
	try:return json.dumps(obj)
	except Exception:return str(obj)
def parse_json(obj):json.loads(obj);return obj
def to_char(obj):return str(obj)
def cancel_all_queries(session):return'canceled'
def arg_min_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1<val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def arg_max_aggregate(_result,_input1,_input2):
	def A(val1,val2):return val1>val2
	return _arg_min_max_aggregate(_result,_input1,_input2,comparator=A)
def _arg_min_max_aggregate(_result,_input1,_input2,comparator):
	B=_input2;A=_result
	if B is _A:return A
	C=json.dumps(json_safe(_input1));D=json.dumps(json_safe(B))
	if A[1]is _A:return[C,D]
	E=json.loads(A[1])
	if comparator(B,E):return[C,D]
	return A
def arg_min_max_finalize(_result):
	A=_result
	if isinstance(A[0],str):return json.loads(A[0])
	return A[0]
def array_agg_aggregate(_result,_input1):
	C=_input1;B=_result
	if C is _A:return B
	A=json.loads(B or'[]');A.append(C);A=json.dumps(A);return A
def array_append(_array,_item):
	B=_item;A=_array
	if A is _A:A='[]'
	A=_unwrap_variant_type(A,expected_type=list)
	if not isinstance(A,list):raise Exception(f"Expected array as first parameter, got: {A}")
	B=_unwrap_variant_type(B);A.append(B);return json.dumps(A)
def array_concat(_array1,_array2):
	B=_array2;A=_array1;A=_unwrap_variant_type(A,expected_type=list);B=_unwrap_variant_type(B,expected_type=list)
	if not isinstance(A,list):raise Exception(f"Expected array as first parameter, got: {A}")
	if not isinstance(B,list):raise Exception(f"Expected array as second parameter, got: {B}")
	C=A+B;return json.dumps(C)
def _unwrap_variant_type(variant_obj_str,expected_type=_A):
	B=expected_type;A=json.loads(variant_obj_str)
	if B:
		if not isinstance(A,B)and isinstance(A,str):
			try:
				C=json.loads(A)
				if isinstance(C,B):A=C
			except Exception:pass
	return A