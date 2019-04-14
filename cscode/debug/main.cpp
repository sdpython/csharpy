#if _MSC_VER

#include <string>
#include <filesystem>

#if __cplusplus < 201402L
namespace fs = std::experimental::filesystem;
#else
namespace fs = std::filesystem;
#endif


void retrieve_dotnetcore_path(std::string &path_clr)
{
    // This function assumes dotnetcore2 is installed.
    //py::scoped_interpreter guard{};
    std::string value = "c:\\Python372_x64\\lib\\site-packages\\dotnetcore2\\bin";
    fs::path path = value;
    path /= std::string("shared");
    path /= std::string("Microsoft.NETCore.App");
    fs::path full_path;
    fs::path look;
    std::string dll("Microsoft.CSharp.dll");
    for (const auto & entry : fs::directory_iterator(path)) {
        full_path = entry.path();
        look = full_path / dll;
        if (fs::exists(look)) {
            auto native = full_path.native();
            path_clr = std::string(native.begin(), native.end());
            return;
        }
    }
}


#include "csmain.hpp"

DECLARE_FCT_NAME(RandomString)


int main()
{
    cs_start("", "C:\\xavierdupre\\__home_\\GitHub\\csharpy\\cscode\\bin\\x64.Debug\\CSharPyExtension\\netstandard2.0");
    double sq = SquareNumber(3);
    std::cout << "square " << sq << "\n";
    DataStructure data;
    int res = cs_RandomString(&data);
    char * pp = (char*)data.outputs;
    std::cout << " Res " << res << " Got '" << pp << "'\n";
    delete data.outputs;
    cs_end();
    return 0;
}

#endif
