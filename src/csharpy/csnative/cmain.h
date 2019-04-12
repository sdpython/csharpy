#pragma once

#include <stdexcept>
#include "stdafx.h"


struct BridgeExecutionError : std::exception
{
    BridgeExecutionError(const char *message);
    virtual char const *what() const noexcept;

private:
    std::string msg_;
};


enum PyErrorCode
{
	PyErrorCode_NoError = 0,
	PyErrorCode_Failure = 1
};


class CLASS_ALIGN ManagedClassExample
{
    public:
        
        std::vector<double> _data;
    
    public: // C# shared

        ManagedClassExample(int verbosity = 0);

        static MANAGED_CALLBACK(void) SetData(ManagedClassExample *penv, std::vector<double> &data);
        static MANAGED_CALLBACK(void) GetData(ManagedClassExample *penv, std::vector<double> &data);

    public: // Python shared
    
        PyErrorCode _errCode;
        std::string _errMessage;
        PyErrorCode GetErrorCode() { return _errCode; }
        std::string GetErrorMessage() { return _errMessage; }   
}
