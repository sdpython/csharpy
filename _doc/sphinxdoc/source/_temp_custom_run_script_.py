from conf import *


loc = locals().copy()
try:
    data = {'__file__': __file__}
except NameError:
    data = {}
import pickle
for k, v in loc.items():
    if v is None or isinstance(v, (str, int, float, tuple, list, dict, set)):
        try:
            pickle.dumps(v)
        except Exception:
            # not pickable
            continue
        data[k] = v

if len(data) == 0:
    import pprint
    raise RuntimeError("data cannot be empty.\n{}".format(pprint.pformat(loc)))

pkl = pickle.dumps(data)

with open('C:/xavierdupre/__home_/GitHub/csharpy/_doc/sphinxdoc/source/_temp_custom_run_script_.py.pkl', 'wb') as f: f.write(pkl)