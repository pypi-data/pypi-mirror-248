﻿//实现基本的简单的CV
#ifndef CV_POSITION_CUH
#define CV_POSITION_CUH

#include "collective_variable.cuh"
 
struct CV_POSITION : public COLLECTIVE_VARIABLE_PROTOTYPE
{	
	int* atom;
	void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
	void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

struct CV_BOX_LENGTH : public COLLECTIVE_VARIABLE_PROTOTYPE
{
	void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
	void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

struct CV_DISTANCE : public COLLECTIVE_VARIABLE_PROTOTYPE
{
	int* atom;
	void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
	void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

struct CV_ANGLE : public COLLECTIVE_VARIABLE_PROTOTYPE
{
	int* atom;
	void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
	void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

struct CV_DIHEDRAL : public COLLECTIVE_VARIABLE_PROTOTYPE
{
	int* atom;
	void Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name);
	void Compute(int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length, int need, int step);
};

#endif //


