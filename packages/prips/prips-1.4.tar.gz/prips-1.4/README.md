# PRIPS: Python Runtime Interface Plugin of SPONGE

SPONGE的python的运行时接口插件

该插件将SPONGE视为一个python解释器，运行python脚本

# 依赖

该插件依赖于cupy。请自行安装好适配你CUDA版本的cupy。

## 为什么需要cupy？

SPONGE的GPU代码需要适配GPU的python端的库，许多库都能满足，如`cupy`、`jax`、`torch`以及`mindspore`。而`cupy`是上述里唯一一个支持“野”指针的库，也即`cupy.cuda.UnownedMemory`，使得它能直接调用SPONGE的内存地址作为自变量，而不需要显式地同步。另外`cupy`作为一个中介，它的数组也可以比较方便地转化为其他库的数组。

# 安装

安装方法：

1. pypi安装

```
pip install prips
```

2. 本地安装
前往gitee库下载解压或克隆源码

```
git clone https://gitee.com/gao_hyp_xyj_admin/sponge_pyplugin.git
```

打开下载并解压或克隆后的文件夹，在有`pyproject.py`的文件夹内呼出合适的shell终端，如windows下的powershell或linux下的shell

```
pip install .
```

# 使用

## SPONGE命令

目前本插件适用的版本为：1.4，也即SPONGE的1.4正式版本

首先在命令行中输入：

```
python -c "import prips"
```

然后正常情况下会输出

```
  PRIPS: Python Runtime Interface Plugin of SPONGE

Version: 1.4a0
Path: xxx\prips\_prips.so

Usage:
    1. Copy the path printed above
    2. Paste it to the value of the command "plugin" of SPONGE
```

在SPONGE的mdin.txt文件夹中加入：

```
plugin =  xxx\prips\_prips.so #上方的Path
py = xxxx\example.py #你需要使用的python脚本地址
```

此处的` xxxx\example.py`仅为示例，请修改为你对应的地址。

## SPONGE获取python信息

SPONGE读取python信息使用的方式是读取函数名。
首先，SPONGE会直接逐行运行一遍该python脚本，由此可进行初始化。
然后，SPONGE会读取python脚本里的`After_Initial()`、`Calculate_Force()`和`Mdout_Print()`，分别在其他模块初始完毕、力计算和打印信息的时候调用。例如下面是一个简单的`Example.py`
```python
def Mdout_Print():
    print("Hellow SPONGE World!")
```

## python获取SPONGE信息

python由模块`Sponge`获取SPONGE信息。模块`Sponge`是SPONGE作为解释器时的内置模块，在外部用python调用是没有的。

`Sponge`模块内若干个子模块，其中`controller`（程序控制）、`cv_controller`（CV定义）、`md_info`（MD信息）是较为重要的模块。这些子模块的定义与C++版本的定义相同。可以使用`help()`寻求帮助，或阅读下面的API介绍。
```
import Sponge
help(Sponge.controller)
help(Sponge.cv_controller)
help(Sponge.md_info)
```

# 简单例子

以下是一个简单的steer MD的例子，对第一个原子的y方向加上一个力。
```python
import Sponge
my_force_factor = 1
if Sponge.controller.Command_Exist("my_force_factor"):
    my_force_factor = float(Sponge.controller.Command("my_force_factor"))
Sponge.controller.Step_Print_Initial("My_Force_Potential", "%2f")

def Calculate_Force():
    Sponge.md_info.frc[0][1] += my_force_factor

def Mdout_Print():
    Sponge.controller.Step_Print("My_Force_Potential", -my_force_factor * Sponge.md_info.crd[0][1])
```

# API介绍

- [Sponge](#sponge)

   - [Sponge.spongeError](#spongespongeerror)

   - [Sponge.COLLECTIVE_VARIABLE_NEED](#spongecollective_variable_need)

   - [Sponge.controller](#spongecontroller)

   - [Sponge.cv_controller](#spongecv_controller)

   - [Sponge.md_info](#spongemd_info)

       - [Sponge.md_info.sys](#spongemd_infosys)

   - [Sponge.NEIGHBOR_LIST](#spongeneighbor_list)

### Sponge
```
Help on built-in module Sponge:

NAME
    Sponge

DATA
    controller = < IO and CUDA controller of SPONGE >
    cv_controller = < cv controller of SPONGE>
    fname = r'D:\prips\api_generator.py'
    md_info = < MD information container of SPONGE >

FILE
    (built-in)


```
### Sponge.spongeError
```
    Sponge.spongeError.spongeSuccess = 0
    Sponge.spongeError.spongeErrorNotImplemented = 1001
    Sponge.spongeError.spongeErrorBadFileFormat = 1002
    Sponge.spongeError.spongeErrorConflictingCommand = 1003
    Sponge.spongeError.spongeErrorMissingCommand = 1004
    Sponge.spongeError.spongeErrorTypeErrorCommand = 1005
    Sponge.spongeError.spongeErrorValueErrorCommand = 1006
    Sponge.spongeError.spongeErrorSimulationBreakDown = 1007
    Sponge.spongeError.spongeErrorMallocFailed = 1008
    Sponge.spongeError.spongeErrorOverflow = 1009
    Sponge.spongeError.spongeErrorOpenFileFailed = 1010

```
### Sponge.COLLECTIVE_VARIABLE_NEED
```
    Sponge.COLLECTIVE_VARIABLE_NEED.CV_NEED_GPU_VALUE = 1
    Sponge.COLLECTIVE_VARIABLE_NEED.CV_NEED_CRD_GRADS = 2
    Sponge.COLLECTIVE_VARIABLE_NEED.CV_NEED_CPU_VALUE = 4
    Sponge.COLLECTIVE_VARIABLE_NEED.CV_NEED_BOX_GRADS = 8

```
### Sponge.controller
```
Help on CONTROLLER in module __main__ object:

class CONTROLLER(builtins.object)
 |  this **class** is the module to control the input, output and cuda in SPONGE
 |
 |  Methods defined here:
 |
 |  Command(self, arg1, arg2=None)
 |      Get the simplified value of the command in SPONGE.
 |      If Only arg1 is given, the command to get the value is "arg1".
 |      If arg1 and arg2 is given, the command to get the value is "arg1_arg2".
 |
 |      :param arg1: the command or the command prefix
 |      :param arg2: the command suffix
 |      :return: a string, the simplified value of the command
 |
 |  Command_Exist(self, arg1, arg2=None)
 |      Check the command whether exist in SPONGE.
 |      If Only arg1 is given, the command to check is "arg1".
 |      If arg1 and arg2 is given, the command to check is "arg1_arg2".
 |
 |      :param arg1: the command or the command prefix
 |      :param arg2: the command suffix
 |      :return: True if the command exist, else False
 |
 |  Original_Command(self, arg1, arg2=None)
 |      Get the original value of the command in SPONGE.
 |      If Only arg1 is given, the command to get the value is "arg1".
 |      If arg1 and arg2 is given, the command to get the value is "arg1_arg2".
 |
 |      :param arg1: the command or the command prefix
 |      :param arg2: the command suffix
 |      :return: a string, the original value of the command
 |
 |  Step_Print(self, head, content)
 |      Print a step print item. A step print item is an item to print in the screen and in the mdout file.
 |
 |      :param head: the name of the item
 |      :param content: the content of the step print item
 |
 |  Step_Print_Initial(self, head, format)
 |      Initialize a step print item. A step print item is an item to print in the screen and in the mdout file.
 |
 |      :param head: the name of the item
 |      :param format: the format of the step print item
 |
 |  Throw_SPONGE_Error(self, error, error_by, error_hint)
 |      Raise error to the screen and the mdinfo file, then exit
 |
 |  Warn(self, warning)
 |      Print the warning to the screen and the mdinfo file
 |
 |  __init__(self)
 |
 |  __repr__(self)
 |
 |  printf(self, *values, sep=' ', end='\n')
 |      Print the values to the screen and the mdinfo file
 |
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |
 |  working_device
 |      The working device id
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)

```
### Sponge.cv_controller
```
Help on COLLECTIVE_VARIABLE_CONTROLLER in module __main__ object:

class COLLECTIVE_VARIABLE_CONTROLLER(CONTROLLER)
 |  Method resolution order:
 |      COLLECTIVE_VARIABLE_CONTROLLER
 |      CONTROLLER
 |      builtins.object
 |
 |  Methods defined here:
 |
 |  Ask_For_CV(self, name, N, verbose_level=0)
 |
 |  Command(self, arg1, arg2=None)
 |
 |  Command_Exist(self, arg1, arg2=None)
 |
 |  Get_CV(self, cv_name)
 |
 |  Original_Command(self, arg1, arg2=None)
 |
 |  __repr__(self)
 |
 |  ----------------------------------------------------------------------
 |  Methods inherited from CONTROLLER:
 |
 |  Step_Print(self, head, content)
 |      Print a step print item. A step print item is an item to print in the screen and in the mdout file.
 |
 |      :param head: the name of the item
 |      :param content: the content of the step print item
 |
 |  Step_Print_Initial(self, head, format)
 |      Initialize a step print item. A step print item is an item to print in the screen and in the mdout file.
 |
 |      :param head: the name of the item
 |      :param format: the format of the step print item
 |
 |  Throw_SPONGE_Error(self, error, error_by, error_hint)
 |      Raise error to the screen and the mdinfo file, then exit
 |
 |  Warn(self, warning)
 |      Print the warning to the screen and the mdinfo file
 |
 |  __init__(self)
 |
 |  printf(self, *values, sep=' ', end='\n')
 |      Print the values to the screen and the mdinfo file
 |
 |  ----------------------------------------------------------------------
 |  Readonly properties inherited from CONTROLLER:
 |
 |  working_device
 |      The working device id
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors inherited from CONTROLLER:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)

```
### Sponge.md_info
```
Help on MD_INFORMATION in module __main__ object:

class MD_INFORMATION(builtins.object)
 |  Contains the information for MD simulations
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |
 |  __repr__(self)
 |
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |
 |  atom_numbers
 |      the total number of atoms
 |
 |  d_mass
 |      the mass of the atoms
 |
 |  sys
 |      the system information
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)
 |
 |  crd
 |      the position coordinates of the atoms
 |
 |  d_atom_energy
 |      the energy of the atoms
 |
 |  d_atom_virial
 |      the virial of the atoms
 |
 |  d_charge
 |      the charge of the atoms (In the unit of SPONGE, a unit charge is 18.2223)
 |
 |  frc
 |      the force of the atoms
 |
 |  vel
 |      the velocity of the atoms

```
### Sponge.md_info.sys
```
Help on system_information in module __main__ object:

class system_information(builtins.object)
 |  the system information of MD information
 |
 |  Readonly properties defined here:
 |
 |  box_length
 |      the length of the box
 |
 |  steps
 |      the current step of the simulation
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)

```
### Sponge.NEIGHBOR_LIST
```
Help on class NEIGHBOR_LIST in module __main__:

class NEIGHBOR_LIST(builtins.object)
 |  Neighbor List of SPONGE.
 |  This class should be initialized at After_Initial, because neighbor_list is not initialized when initializing prips
 |
 |  Methods defined here:
 |
 |  __init__(self)
 |
 |  ----------------------------------------------------------------------
 |  Readonly properties defined here:
 |
 |  atom_numbers
 |      the number of neighbors for every atom
 |
 |  atom_serials
 |      the serial of neighbors for every atom
 |
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |
 |  __dict__
 |      dictionary for instance variables (if defined)
 |
 |  __weakref__
 |      list of weak references to the object (if defined)

```
