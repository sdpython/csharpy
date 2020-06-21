
#ifndef __cplusplus
  #error C++ is required
#else
    #if _MSC_VER
        #include <iostream>
        #if __cplusplus < 201703L
        #define _SILENCE_EXPERIMENTAL_FILESYSTEM_DEPRECATION_WARNING
        #include <experimental/filesystem>
        namespace fs = std::experimental::filesystem;
        #else
        #include <filesystem>
        namespace fs = std::filesystem;
        #endif

        #define PATHTYPE fs::path
        #define PATHJOIN(a,b) a / b
        #define PATHIJOIN(a,b) a /= b
        #define PATHEXISTS(path) fs::exists(path)
        #define PATHTOSTRING(path_clr, fpath)   \
            auto native = fpath.native();       \
            path_clr = std::string(native.begin(), native.end());
        #define PATHITER(path) fs::directory_iterator(path)
    #else
        bool fs_exists(const std::string &path);
        std::vector<std::string> fs_listdir(const std::string& s);

        #define PATHTYPE std::string
        #define PATHJOIN(a,b) a + std::string("/") + b
        #define PATHIJOIN(a,b) a += std::string("/") + b
        #define PATHEXISTS(path) fs_exists(path)
        #define PATHTOSTRING(a,b) a=b;
        #define PATHITER(p) fs_listdir(p)
    #endif
#endif
