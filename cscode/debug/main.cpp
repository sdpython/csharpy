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
    std::string value = "";
    fs::path path = value;
    path /= std::string("shared");
    path /= std::string("Microsoft.NETCore.App");
    fs::path full_path;
    fs::path look;
    std::string dll("Microsoft.CSharp.dll");
    for (const auto & entry : fs::directory_iterator(path)) {
        full_path = path / entry.path();
        look = full_path / dll;
        if (fs::exists(look)) {
            auto native = full_path.native();
            path_clr = std::string(native.begin(), native.end());
            return;
        }
    }
}

void main()
{

}