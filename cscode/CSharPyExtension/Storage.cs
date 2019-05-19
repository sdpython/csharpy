using System;
using System.Collections.Generic;
using System.Reflection;


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

        public enum ReferenceKind
        {
            object_ = 1,
            delegate_ = 2,
            methodInfo_ = 3
        };

        public class Reference
        {
            public ReferenceKind kind;
            public object ptr;
            public Delegate del;
            public int count;

            public override string ToString()
            {
                switch (kind)
                {
                    case ReferenceKind.delegate_:
                        return string.Format("count={0} kind={1}", count, "delegate");
                    case ReferenceKind.object_:
                        return string.Format("count={0} kind={1} type={2}", count, "object", ptr.GetType());
                    case ReferenceKind.methodInfo_:
                        return string.Format("count={0} kind={1} type={2}", count, "method", ptr.GetType());
                    default:
                        throw new KeyNotFoundException("Unknwon kind.");
                }
            }

            public Reference(object p, int c)
            {
                kind = ReferenceKind.object_;
                ptr = p;
                count = c;
                del = null;
            }

            public Reference(MethodInfo p, int c)
            {
                kind = ReferenceKind.methodInfo_;
                ptr = (object)p;
                count = c;
                del = null;
            }

            public Reference(Delegate d, int c)
            {
                kind = ReferenceKind.delegate_;
                del = d;
                count = c;
                ptr = null;
            }

            public object Object
            {
                get
                {
                    if (kind != ReferenceKind.object_)
                        throw new InvalidOperationException("This reference is not an object.");
                    return ptr;
                }
            }

            public MethodInfo MethodInfo
            {
                get
                {
                    if (kind != ReferenceKind.methodInfo_)
                        throw new InvalidOperationException("This reference is not an MethodInfo.");
                    return (MethodInfo)ptr;
                }
            }

            public object Del
            {
                get
                {
                    if (kind != ReferenceKind.delegate_)
                        throw new InvalidOperationException("This reference is not a delegate function.");
                    return del;
                }
            }
        }

        private Dictionary<Int64, Reference> _references;
        private Int64 _last;

        private ObjectStorage()
        {
            _references = new Dictionary<Int64, Reference>();
            _last = 0;
        }

        public Reference Get(Int64 i)
        {
            Reference res;
            lock (_references)
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
                _references[_last] = new Reference(ptr, 1);
                res = _last;
                _last++;
            }
            return res;
        }

        public Int64 AddIncref(MethodInfo methodInfo)
        {
            Int64 res;
            lock (_references)
            {
                _references[_last] = new Reference(methodInfo, 1);
                res = _last;
                _last++;
            }
            return res;
        }

        public Int64 AddIncref(Delegate del)
        {
            Int64 res;
            lock (_references)
            {
                _references[_last] = new Reference(del, 1);
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
