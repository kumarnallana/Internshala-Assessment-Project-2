import sys
sys.modules['google._upb'] = None
sys.modules['google._upb._message'] = None
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
