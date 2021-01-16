
DECLARE_FCT_NAME(CallVoid)

void CallVoid(int64_ fct, bool catchOutput)
{
    DataStructure data;
    data.inputs = NULL;
    data.outputs = NULL;
    data.exc = &fct;
    cs_CallVoid(&data, catchOutput);
}

///

DECLARE_FCT_NAME(CallDoubleDouble)

double CallDoubleDouble(int64_ fct, bool catchOutput, double x) {
    double res;
    DataStructure data;
    data.inputs = &x;
    data.outputs = &res;
    data.exc = &fct;
    cs_CallDoubleDouble(&data, catchOutput);
    return res;
}

///

typedef struct CallArrayInt32StringOutput {
    public:
        void * p;
        int nb;
} CallArrayInt32StringOutput;

DECLARE_FCT_NAME(CallArrayInt32String)

std::vector<int> CallArrayInt32String(int64_ fct, bool catchOutput, const std::string& text) {
    DataStructure data;
    data.inputs = (void*)text.c_str();
    CallArrayInt32StringOutput output;
    data.outputs = &output;
    data.exc = &fct;
    cs_CallArrayInt32String(&data, catchOutput);
    if (output.p == NULL)
        return std::vector<int>();
    std::vector<int> res(output.nb);
    memcpy(&(res[0]), output.p, output.nb * sizeof(int));
    delete[] output.p;
    return res;
}

///

typedef struct CallArrayDoubleArrayDoubleIO {
    public:
        void * p;
        int nb;
} CallArrayDoubleArrayDoubleIO;

DECLARE_FCT_NAME(CallArrayDoubleArrayDouble)

std::vector<double> CallArrayDoubleArrayDouble(int64_ fct, bool catchOutput,
                                               const std::vector<double>& vec) {
    DataStructure data;
    CallArrayDoubleArrayDoubleIO input, output;
    data.inputs = (void*)&input;
    data.outputs = (void*)&output;
    data.exc = &fct;

    input.nb = (int)vec.size();
    input.p = (void*)&(vec[0]);

    cs_CallArrayDoubleArrayDouble(&data, catchOutput);
    
    if (output.p == NULL)
        return std::vector<double>();
    std::vector<double> res(output.nb);    
    memcpy(&(res[0]), output.p, output.nb * sizeof(double));
    delete[] output.p;
    return res;
}

