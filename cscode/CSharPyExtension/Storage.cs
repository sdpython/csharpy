using System;
using System.Collections.Generic;
using System.Text;

namespace CSharPyExtension
{
    public class ObjectStorage
    {
        private static object _lck = new object();
        private static ObjectStorage _obj;
        public static ObjectStorage Inst
        {
            get
            {
                if (_obj == null)
                    lock (_lck)
                        if (_obj == null)
                            _obj = new ObjectStorage();
                return _obj;
            }
        }

        internal class Reference
        {
            public object ptr;
            public int count;
        }

        private Dictionary<Int64, Reference> _references;
        private Int64 _last;

        private ObjectStorage()
        {
            _references = new Dictionary<Int64, Reference>();
            _last = 0;
        }

        public object Get(Int64 i)
        {
            object res;
            lock(_references)
                res = _references[i];
            return res;
        }

        public void Incref(Int64 i)
        {
            lock (_references)
                _references[i].count += 1;
        }

        public int Nref(Int64 i)
        {
            int res;
            lock (_references)
                res = _references.ContainsKey(i) ? _references[i].count : (int)0;                
            return res;
        }

        public void Decref(Int64 i)
        {
            lock (_references)
            {
                _references[i].count -= 1;
                if (_references[i].count < 0)
                    _references.Remove(i);
            }
        }

        public Int64 AddIncref(object ptr)
        {
            Int64 res;
            lock (_references)
            {
                _references[_last] = new Reference() { count = 1, ptr = ptr };
                res = _last;
                _last++;
            }
            return res;
        }
    }

    public unsafe static partial class CsBridge
    {
        public static unsafe int ObjectDecref(DataStructure* data)
        {
            Int64 oid = *(Int64*)data->inputs;
            ObjectStorage.Inst.Decref(oid);
            return 0;
        }

        public static unsafe int ObjectIncref(DataStructure* data)
        {
            Int64 oid = *(Int64*)data->inputs;
            ObjectStorage.Inst.Incref(oid);
            return 0;
        }
    }
}
