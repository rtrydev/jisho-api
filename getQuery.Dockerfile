FROM public.ecr.aws/lambda/python:3.12
ARG FUNCTION_DIR="/var/task"

RUN mkdir -p ${FUNCTION_DIR}

COPY requirements.txt ${FUNCTION_DIR}
RUN pip install -r requirements.txt

COPY jap_eng_dict.json ${FUNCTION_DIR}
COPY jap_eng_examples.json ${FUNCTION_DIR}
COPY src ${FUNCTION_DIR}/src

CMD [ "src.handlers.get_query.handler" ]