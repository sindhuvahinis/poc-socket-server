from protocol.request import Request

from util.serializing import djl_encode, output_encode
from util.deserializing import input_decode, djl_decode
from util.packaging_util import get_class_name


def _exec_pre_processor(request, input):
    processor_class = get_class_name(request.python_file, request.function_name)
    preprocessor = processor_class()
    data = getattr(preprocessor, request.function_name)(input)
    print(f'preprocess data {data}')
    return data


def _exec_post_processor(request, nd_list):
    processor_class = get_class_name(request.python_file, request.function_name)
    preprocessor = processor_class()
    data = getattr(preprocessor, request.function_name)(nd_list)
    print(f'postprocess data {data}')
    return data


def run_processor(request: Request) -> bytearray:
    if request.process_type_code == 0:
        input = input_decode(request.content)
        response_data = _exec_pre_processor(request, input)
        return djl_encode(response_data)
    elif request.process_type_code == 1:
        nd_list = djl_decode(request.content)
        response_data = _exec_post_processor(request, nd_list)
        return output_encode(response_data)
    else:
        raise ValueError("Error in request process type code.")
