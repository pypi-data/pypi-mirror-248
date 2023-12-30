﻿//CV COMBINATION
#ifndef CV_COMBINE_CUH
#define CV_COMBINE_CUH

#include "collective_variable.cuh"
#include "nvrtc.h"

struct CV_COMBINE : public COLLECTIVE_VARIABLE_PROTOTYPE
{
    CV_LIST cv_lists;
    JIT_Function first_step;
    JIT_Function second_step;
    float** d_cv_values;
    VECTOR** cv_crd_grads;
    VECTOR** cv_box_grads;
    float** df_dcv;
    void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
    void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

#endif


