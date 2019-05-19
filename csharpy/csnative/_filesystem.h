#ifndef __cplusplus
  #error C++ is required
#else
    #if __cplusplus < 201703L
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
    #else
    #include <filesystem>
    namespace fs = std::filesystem;
    #endif
#endif
