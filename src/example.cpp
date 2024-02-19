#include <emscripten.h>
#include <stdlib.h>

extern "C" {
    EMSCRIPTEN_KEEPALIVE
    void* F32Malloc(int length) {
        return malloc(length * sizeof(float));
    }

    EMSCRIPTEN_KEEPALIVE
    void F32Free(float* ptr) {
        free(ptr);
    }

    EMSCRIPTEN_KEEPALIVE
    void* I32Malloc(int length) {
        return malloc(length * sizeof(int));
    }

    EMSCRIPTEN_KEEPALIVE
    void I32Free(int* ptr) {
        free(ptr);
    }

    // 배열의 모든 요소에 1을 더하는 함수
    EMSCRIPTEN_KEEPALIVE
    void AddOneElementAA(float* arr, int length) {
        for (int i = 0; i < length; ++i) {
            arr[i] += 1.0f;
        }
    }
}
