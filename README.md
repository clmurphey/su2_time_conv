# SU2 Time Convergence Study


## Overview
> **Note**: The examples used in this study are derived from [SU2's](https://github.com/su2code/SU2) [Test Cases](https://github.com/su2code/SU2/tree/master/TestCases). 
> - The Laminar Flat Plate example comes from the [unsteady flat plate Navier Stokes example](https://github.com/su2code/SU2/blob/master/TestCases/navierstokes/flatplate/lam_flatplate_unst.cfg).
> - The Navier Stokes Cylinder example comes from [lam_cylinder.cfg](https://github.com/su2code/SU2/blob/master/TestCases/navierstokes/cylinder/lam_cylinder.cfg) and various other unsteady flow examples.

The idea here is to see how quickly SU2's different time integration schemes converge. Examples in this repository show how varying temporal parameters such as `TIME_MARCHING`, `TIME_DISCRE_FLOW`, and `TIME_STEP` affect the convergence rate of the solution to two examples problems employing different numerical methods. 

This code includes a [time_convergence_study.py](https://github.com/clmurphey/su2_time_conv/blob/main/lam_flatplate/time_convergence_study.py) script, which iterates through the various configurations tested.  Also included, is a script which automates changes to SU2's configuration files (update_ts.py). (N.B., there are two versions of `time_convergence_study.py` in this repository. Differences between the verions reflect what and how the data is plotted.)

### Tests
The example in this repository test the following fields. 
- `TIME_MARCHING` : DUAL_TIME_STEPPING-1ST_ORDER, DUAL_TIME_STEPPING-2ND-ORDER, TIME_STEPPING
- `TIME_DISCRE_FLOW` : EULER_IMPLICIT (default), EULER_EXPLICIT, RUNGE-KUTTA_EXPLICIT 
- `SOLVER` : FEM_NAVIER_STOKES, NAVIER_STOKES
- `NUM_METHOD_GRAD` : GREEN_GAUSS, WEIGHTED_LEAST_SQUARES
- `NUM_METHOD_FLOW` and `NUM_METHOD_FEM_FLOW` : DG, JST, ROE

Only able to employ Implicit methods in the laminar flat plate flow example due to periodic boundary conditions. Explicit methods caused the solution to diverge (related to [this issue](https://github.com/su2code/SU2/issues/1090)). 

### Objectives
- To better understand SU2's time integration methods and their convergence rates.
- To understand where and how SU2's time integration methods could improve.
- To grow more familiar with how SU2 works and what the respository can do currently.
- To learn more about time integration methods used with Finite Volume Methods (and Discontinuous Galerkin Methods)

### Code Requirements
- [SU2 v. 7.2.1](https://su2code.github.io/docs_v7/Installation/)
  - Must be configured with mpi enabled. 
- openmpi
- scipy
- pandas
- numpy
- matplotlib

### To Run the examples
Run `time_convergence_study.py`. The examples output Paraview `.vtu` files. 

## Examples

### Unsteady Laminar Flow - Flat Plate (with periodic boundary conditions)
*Based on [this](https://su2code.github.io/tutorials/Laminar_Flat_Plate/) problem in SU2's Tutorials*
<img src="https://user-images.githubusercontent.com/37432497/145163560-8869c788-4c6a-4226-b779-c12653db8b87.png" height="300" />


> **Parameters (see config file for more detail)**
> - Flow: Unsteady (`TIME_DOMAIN = YES`), ideal, subsonic flow with constant viscosity and conductivity
>   - Boundary Conditions: periodic
>   - Mesh: flat plate
> - Numerical : ROE numerical method, 
>   - `SOLVER` : `FEM_NAVIER_STOKES` (for DG) and `NAVIER_STOKES` 
>   - `TIME_MARCHING` : (varies) `TIME_STEPPING`, `DUAL_TIME_STEPPING-1ST_ORDER`, `DUAL_TIME_STEPPING-2ND_ORDER`
>   - `TIME_ITER` : `1` (increase for more time steps)
>   - `TIME_DISCRE_FLOW` : `EULER_IMPLICIT` 
>   - Time Convergence Field: `RMS_ENERGY`

#### Figures

### Unsteady Navier Stokes Flow over a Cylinder
<img src="https://user-images.githubusercontent.com/37432497/145163342-9eda0bae-e2b6-42cb-af65-191c81d1895d.png" height="300" />

> **Parameters (see config file for more detail)**
> - Flow: Unsteady (`TIME_DOMAIN = YES`), ideal, subsonic flow with constant viscosity and conductivity
>   - Boundary Conditions: Farfield Boundary Markers
>   - Mesh: cylinder
> - Numerical : 
>   - `SOLVER` : `FEM_NAVIER_STOKES` (for DG) and `NAVIER_STOKES` 
>   - `TIME_MARCHING` : (varies) `TIME_STEPPING`, `DUAL_TIME_STEPPING-1ST_ORDER`, `DUAL_TIME_STEPPING-2ND_ORDER`
>   - `TIME_ITER` : `1` (increase for more time steps)
>   - `TIME_DISCRE_FLOW` or `TIME_DISCRE_FEM_FLOW` : `EULER_IMPLICIT`, `EULER_EXPLICIT`, `RUNGE-KUTTA_EXPLICIT`
>   - Time Convergence Field: `TAVG_COMBO`

#### Figures


## Future Work
- Test on more unsteady example problems
- Estimate the error
- Implement MMS to verify the solutions (unsteady MMS is not yet available in SU2) 
