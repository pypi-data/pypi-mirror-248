#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "simhash-cpp/include/simhash.h"
namespace py = pybind11;

PYBIND11_MODULE(_simhash, m) {
    m.def("num_differing_bits", &Simhash::num_differing_bits, "Compute the number of bits that are flipped between two numbers");
    m.def("compute", &Simhash::compute, "Compute the number of bits that are flipped between two numbers");
    m.def("find_all", &Simhash::find_all, "Find the set of all matches within the provided vector of hashes");
}
