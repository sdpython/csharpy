#include <pybind11/pybind11.h>
#include <pybind11/operators.h>

namespace py = pybind11;


PYBIND11_MODULE(weighted_number, m) {
	m.doc() = "Exposes C# functions";
}
