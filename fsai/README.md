```bash
.venv/bin/pip3 install -r requirements_http.txt
pip install -r ./fsai/requirements.in
cd src/python
uv pip install -e .

python -m piper.http_server --model /media/joshua/UbuntuNonOS/Github/piper/fsai/onnx/en_US-lessac-high.onnx

```
