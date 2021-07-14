from protocol.request import Request
from protocol.response import Response

from util.serializing import djl_encode, output_encode, response_encode
from util.deserializing import input_decode, djl_decode
from util.packaging_util import get_class_name


def _exec_pre_processor(request, input):
    print(f'preprocess request {request}')
    processor_class = get_class_name(request.python_file, request.function_name)
    preprocessor = processor_class()
    data = getattr(preprocessor, request.function_name)(input)
    print(f'preprocess output after exec {data}')
    return data


def _exec_post_processor(request, nd_list):
    print(f'postprocess request {request}')
    processor_class = get_class_name(request.python_file, request.function_name)
    preprocessor = processor_class()
    data = getattr(preprocessor, request.function_name)(nd_list, "1")
    print(f'postprocess output after exec {data}')
    return data


def run_processor(request: Request) -> bytearray:
    if request.process_type_code == 0:
        input = input_decode(request.content)
        response_data = _exec_pre_processor(request, input)
        return djl_encode(response_data)
    elif request.process_type_code == 1:
        nd_list = djl_decode(request.content)
        response_data = _exec_post_processor(request, nd_list)
        arr = output_encode(response_data)
        response = Response()
        response.set_len(len(arr))
        response.set_buffer_arr(arr)
        return response_encode(response)
    else:
        raise ValueError("Error in request process type code.")
