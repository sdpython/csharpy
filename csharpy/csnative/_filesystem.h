#ifndef __cplusplus
  #error C++ is required
#else
    #include <iostream>
    #if __cplusplus < 201703L
    #include <experimental/filesystem>
    namespace fs = std::experimental::filesystem;
    #else
    #include <filesystem>
    namespace fs = std::filesystem;
    #endif
#endif
