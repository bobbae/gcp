# Copyright (c) 2019 Ekaba Bisong

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

FROM gcr.io/ml-pipeline/ml-pipeline-dataflow-tft:latest

RUN mkdir /crypto

COPY dataflow_transform.py service_account.json /crypto/

RUN pip install --upgrade google-api-python-client
RUN gcloud -q components install beta
RUN gcloud auth activate-service-account --key-file=./crypto/service_account.json
RUN gcloud config set project oceanic-sky-230504

ENV GOOGLE_APPLICATION_CREDENTIALS=./crypto/service_account.json

ENTRYPOINT ["python", "/crypto/dataflow_transform.py"]