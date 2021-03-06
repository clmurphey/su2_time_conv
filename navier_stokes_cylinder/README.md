# Time Convergence Study for Time-Dependent Flow 
The idea here is to see how SU2's different time stepping schemes converge at different time step sizes in unsteady simulations.

This directory includes `time_convergence.py`, a Python script based on `computer_order_of_accuracy.py` [here](https://github.com/su2code/VandV/blob/ad27cdf9391c9077f3ef14949e29c01be428b0d9/mms/fvm_navierstokes/compute_order_of_accuracy.py). This script loops over various different time marching schemes (e.g., `TIME_MARCHING = TIME_STEPPING`, `TIME_MARCHING = DUAL-TIME_STEPPING-1ST_ORDER`, `TIME_MARCHING = DUAL-TIME_STEPPING-2ND_ORDER`) for each of SU2's Navier Stokes Solvers (e.g., `FEM_NAVIER_STOKES` and `NAVIER_STOKES`) using different numerical methods (e.g., DG, JST, ROE+LIM, ROE, ROW+WLS).  Each case is evaluated at a different `TIME_STEP` size [1e-6 : 1e-10]. 

- Some parameters: 
	- Mesh: currently uses a quad mesh generated by `create_grid_quad.py` copied over from the `fvm_navier_stokes` VandV example.
	- TIME_ITER : 15
	- Time Discretization: employs the default for each Numerical method (e.g., RUNGE-KUTTA_EXPLICIT for DG and EULER_IMPLICIT for FVM)
	- Fluid properties are uniform across the 4 configuration files: 
		- lam_mms_dg_unst.cfg : FEM unsteady Navier Stokes Flow on Unit Quad using Discontinuous Galerkin
		- lam_mms_jst_unst.cfg : FVM unsteady Navier Stokes Flow on Unit Quad using JST
		- lam_mms_roe_lim_unst.cfg : FVM unsteady Navier Stokes Flow on Unit Quad using ROE + LIM
		- lam_mms_roe_unst.cfg : FVM unsteady Navier Stokes Flow on Unit Quad using ROE 
		- lam_mms_roe_wls.unst.cfg : FVM unsteady Navier Stokes Flow on Unit Quad using WLS