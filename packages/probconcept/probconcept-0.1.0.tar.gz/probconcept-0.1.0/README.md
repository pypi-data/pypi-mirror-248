# probconcept
**Readme in progress.**

This python package was originally published in my Surface Velocity Tools 
(SurfVelTools) application:

Engel, F. L., 2023, Surface Velocity Tools (SurfVelTools), U.S. Geological
Survey software release,
[https://doi.org/10.5066/P9I5JABK](https://doi.org/10.5066/P9I5JABK).

I am working to publish the internal probconcept module separately so that
it can be installed for various other uses.

[Documentation](https://probability-concept-flow.readthedocs.io/en/latest/)

## Usage
The basic curve fitting is handled by the `ProbConcept` class. All methods for creating the fit and producing results
that can be plotted are contained within the class. See the documentation in the class for more information.

At a minimum, to fit a curve to your velocity data and derive an output, you will need to import the class with
something like:

```python
from probconcept import ProbConcept as pc
```

From here, supply `numpy` arrays (1D vectors) for depth-velocity pairs of measurements made of the velocity profile 
in the y-axis (see more info about what the y-axis is below).  An optional numpy array of the same shape
as the input depth-velocity pairs containing the uncertainty of the velocity can be supplied and modeled in the fit.

```python
pc_fit = pc.ProbConceptFit()
pc_fit.populate_velocity_profile_data(meas_depths, meas_velocities, meas_uncertainty)
```

If known, you can also supply a measured total depth, and/or measured max velocity and distance from the surface of the
max velocity (h). These are optional arguments. The `ProbConcept` class will attempt to solve for these unknowns without
user input if not supplied.

```python
pc_fit = pc.ProbConceptFit()
pc_fit.populate_velocity_profile_data(meas_depths, meas_velocities, meas_uncertainty,
                                      meas_total_depth, meas_max_velocity, h)
```



## Theory and Explanation
Work in progress...