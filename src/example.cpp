// example.cpp
// Eigen, include안의 소스코드가 연결되는지 테스트하는 예제
// igl은 include안의 header-only 라이브러리이므로, 이를 테스트하기 위해 사용함
#include <emscripten/bind.h>
#include <Eigen/Dense>
#include "igl/offset_surface.h"

using namespace emscripten;

float lerp(float a, float b, float t)
{
    Eigen::MatrixXd V;
    Eigen::MatrixXi F;
    return (1 - t) * a + t * b;
}

EMSCRIPTEN_BINDINGS(my_module)
{
    function("lerp", &lerp);
}