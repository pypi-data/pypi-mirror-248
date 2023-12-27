import logging
import warnings

import lmfit
import numpy as np
import pybroom as br
from lmfit import Model
from scipy.stats.distributions import chi2, t


class ProbConceptFit(object):
    """Class to compute the probability concept parameters

    Attributes
    ----------
    depths : ndarray
        Measured depths.
    velocities : ndarray
        Measured velocities.
    uncertainties : ndarray
        Measured uncertainties.
    max_depth : float
        The maximum depth of water at the velocity profile.
    max_velocity : float
        The maximum velocity in the velocity profile.
    surface_velocity : float
        The velocity at the water surface.
    depth_flag : bool
        Indicates if the max_depth is larger than the largest depth supplied in depths.
    surface_flag : bool
        Indicates if the maximum velocity occurs at the surface.
    use_measured_uncertainties_flag : bool
        Indicates whether to use measured uncertainties in the analysis.
    use_surface_velocity_flag : bool
        Indicates whether to use surface velocity in the analysis.
    max_velocity_index : integer
        Logical index into depths/velocities indicating max velocity.
    h : float
        Distance from the water surface to the maximum velocity.
    h_D : float
        Relative distance from the water surface to the maximum velocity (h/D).
    usurf_umax : float
        Ratio of surface velocity to maximum velocity (Usurf/Umax).
    m : float
        Parameter from the probability concept, related to phi.
    m_stderr : float
        Standard error of the m parameter.
    phi : float
        Parameter describing the relationship between the velocity profile and maximum velocity.
    phi_stderr : float
        Standard error of the phi parameter.
    gamma : float
        Parameter describing the uncertainty in velocity.
    gamma_stderr : float
        Standard error of the gamma parameter.

    fit_coefficients : ndarray
        Coefficients returned by scipy.curve_fit.
    fit_max_velocity : float
        Maximum velocity fitted by nonlinear regression.
    fit_pcov : ndarray
        Covariance matrix returned by scipy.curve_fit.
    fit_regression_error : float
        Standard error of the regression analysis.
    fit_standard_deviations : ndarray
        Standard deviations of the regression analysis.
    fit_rmse : float
        Root mean square error of the regression.
    fit_r2 : float
        R-squared of the regression.
    fit_x : ndarray
        Output velocities which can be used to plot the fit results.
    fit_y : ndarray
        Output depths which can be used to plot the fit results.
    fit_y_95_ci_lower : ndarray
        Lower bound of the 95% confidence interval of the fit.
    fit_y_95_ci_upper : ndarray
        Upper bound of the 95% confidence interval of the fit.
    fit_y_regression_error_lower : ndarray
        Lower bound of the regression error of the fit (standard error applied to model).
    fit_y_regression_error_upper : ndarray
        Lower bound of the regression error of the fit (standard error applied to model).
    fit_95_uncertainty : ndarray
        Estimated 95% uncertainty of the fitted model parameters (velocity, M, D, h).
    """

    def __init__(self):
        self.depths = np.zeros(shape=(1,))
        self.velocities = np.zeros(shape=(1,))
        self.uncertainties = np.zeros(shape=(1,))
        self.max_depth = np.nan
        self.max_velocity = np.nan
        self.surface_velocity = np.nan
        self.depth_flag = False
        self.surface_flag = True
        self.use_measured_uncertainties_flag = True
        self.use_surface_velocity_flag = False
        self.max_velocity_index = None
        self.h = np.nan
        self.h_D = np.nan
        self.usurf_umax = np.nan
        self.m = np.nan
        self.m_stderr = np.nan
        self.phi_stderr = np.nan
        self.phi = np.nan
        self.gamma = np.nan
        self.gamma_stderr = np.nan

        # Initialize model, parameters and set solvable constraints/bounds
        self.model = Model(self.pc_function)
        self.parameters = None
        self.parameters = self.model.make_params()
        # add with tuples: (NAME VALUE VARY MIN  MAX  EXPR  BRUTE_STEP)
        self.parameters.add_many(
            ("max_velocity", None, True, 0.0, np.inf, None, None),
            ("m", None, True, 0.0001, 10.0, None, None),
            ("depth", None, False, 0.0, np.inf, None, None),
            ("h", None, False, 0.0, np.inf, None, None),
        )
        self.fit_results = None
        self.fit_result_uncertainty_1_sigma = None
        self.fit_result_uncertainty_2_sigma = None
        self.fit_chisqprob_pval = None
        self.fit_velocities = np.zeros(shape=(50,))
        self.fit_depths = np.zeros(shape=(50,))
        self.fit_velocities_95_ci_lower = np.zeros(shape=(50,))
        self.fit_velocities_95_ci_upper = np.zeros(shape=(50,))
        self.fit_95_uncertainty = np.zeros(shape=(4,))

        # Initialize model results dataframe
        self.fit_results_df = None

    def populate_velocity_profile_data(
        self,
        depths=None,
        velocities=None,
        uncertainties=None,
        max_depth=None,
        h=None,
        max_velocity=None,
        use_uncertainty=True,
    ):
        """Populated the velocity profile data for the lmfit model

        Parameters
        ----------
        depths : ndarray
        velocities : ndarray
        uncertainties : ndarray
        max_depth : ndarray
        max_velocity : ndarray
        h : ndarray
        use_uncertainty : bool
        """

        self.velocities = velocities
        self.depths = depths
        self.uncertainties = uncertainties
        self.use_measured_uncertainties_flag = use_uncertainty
        self.set_max_depth(max_depth)
        self.set_max_velocity(max_velocity)
        self.set_h(h)
        self.update_parameter("max_velocity", value=self.max_velocity)
        self.update_parameter("depth", value=self.max_depth)
        self.update_parameter("h", value=self.h)
        logging.info("Initial parameters:")
        logging.info(self.parameters.pretty_print())  # type: ignore[union-attr]

        # Compute the fit
        self.compute_fit()
        self.compute_statistics()
        self.compute_model()
        logging.info(lmfit.fit_report(self.fit_results))

    def update_parameter(self, parameter, **kwargs):
        """Update the model parameters. Expects parameter keyword pairs corresponding to lmfit set method.

        Parameters
        ----------
        parameter : str
        """
        for key, value in kwargs.items():
            if key == "value":
                self.parameters[parameter].set(value=value)  # type: ignore[index]
            elif key == "vary":
                self.parameters[parameter].set(vary=value)  # type: ignore[index]
            elif key == "min":
                self.parameters[parameter].set(min=value)  # type: ignore[index]
            elif key == "max":
                self.parameters[parameter].set(max=value)  # type: ignore[index]
            elif key == "expr":
                self.parameters[parameter].set(expr=value)  # type: ignore[index]
            elif key == "brute_step":
                self.parameters[parameter].set(brute_step=value)  # type: ignore[index]
            else:
                raise Exception

    def set_max_depth(self, max_depth=None):
        """Set the mac depth

        Parameters
        ----------
        max_depth : object
        """
        if max_depth is None:
            self.max_depth = np.max(self.depths)
            self.depth_flag = False
        else:
            self.max_depth = max_depth
            if max_depth >= np.max(self.depths):
                self.depth_flag = True
            else:
                self.depth_flag = False

    def set_max_velocity(self, max_velocity=None):
        """Set the max velocity

        Parameters
        ----------
        max_velocity : object
        """
        if max_velocity is None:
            self.max_velocity = np.max(self.velocities)
            self.max_velocity_index = self.velocities.argmax()
        else:
            self.max_velocity = max_velocity
            self.max_velocity_index = (np.abs(self.velocities - max_velocity)).argmin()
        if self.max_velocity_index != 0:
            self.surface_flag = False
        else:
            self.surface_flag = True

    def set_h(self, h=None):
        """Set the dpeth from water surface to u_max

        Parameters
        ----------
        h : object
        """
        if h is None:
            self.h = self.max_depth - self.depths[self.max_velocity_index]
        else:
            self.h = h

    @staticmethod
    def pc_function(depth_i, max_velocity, m, depth, h):
        """The probability concept equation for case of max velocity below the surface

        This is Case 1 from Chiu and Tung, 2002 [10.1061/(ASCE)0733-9429(2002)128:4(390)].

        Solves equation 4 of the T&M

        Parameters
        ----------
        depth_i : symbolic
            independent variable. depth at each point in velocity profile supplied.
        max_velocity : symbolic
            maximum velocity in the profile
        m : symbolic
            parameter M from probability concept
        depth : symbolic
            total depth
        h : symbolic
            distance from the water surface to umax
        """
        # max_velocity / m * np.log(1 + ((np.exp(m) - 1) * depth_i) / (depth - h) * np.exp(1 - depth_i / (depth - h)))
        return (
            max_velocity
            / m
            * np.log(
                1 + ((np.exp(m) - 1) * depth_i / (depth - h) * np.exp(1 - depth_i / (depth - h)))
            )
        )

    @staticmethod
    def pc_function_surface(depth_i, max_velocity, m, depth):
        """The probability concept equation for case of max velocity at the surface

        This is Case 2 from Chiu and Tung, 2002 [10.1061/(ASCE)0733-9429(2002)128:4(390)].

        Solve equation 3 of the T&M

        Parameters
        ----------
        depth_i : symbolic
            independent variable. depth at each point in velocity profile supplied.
        max_velocity : symbolic
            maximum velocity in the profile
        m : symbolic
            parameter M from probability concept
        depth : symbolic
            total depth
        """
        return (
            max_velocity
            / m
            * np.log(1 + ((np.exp(m) - 1) * depth_i / depth * np.exp(1 - depth_i / depth)))
        )

    @staticmethod
    def pc_function_case3(depth_i, max_velocity, m, depth, h):
        """The probability concept equation for case of max velocity at the surface, specialized case 3

        This is Case 3 from Chiu and Tung, 2002 [10.1061/(ASCE)0733-9429(2002)128:4(390)].

        Parameters
        ----------
        depth_i : symbolic
            independent variable. depth at each point in velocity profile supplied.
        max_velocity : symbolic
            maximum velocity in the profile
        m : symbolic
            parameter M from probability concept
        depth : symbolic
            total depth
        h : symbolic
            distance from the water surface to umax
        """
        return (
            max_velocity
            / m
            * np.log(
                1 + ((np.exp(m) - 1) * depth_i / depth * np.exp((depth - depth_i) / (depth - h)))
            )
        )

    @staticmethod
    def usurf_to_umax(usurf, m, h, depth):
        """Converts surface velocity into max velocity given depth below surface where umax occurs

        Solves equation 6 of the T&M

        Parameters
        ----------
        usurf: float
        m: float
        h: float
        depth: float

        Returns
        -------
        float
        """
        return (
            usurf
            * m
            * (np.log(1 + (np.exp(m) - 1) * 1 / (1 - h / depth) * np.exp(1 - 1 / (1 - h / depth))))
            ** -1
        )

    @staticmethod
    def solve_usurf_umax_ratio(m, h, depth):
        """Solve for usurf/umax.

        Parameters
        ----------
        m: float
        h: float
        depth: float

        Returns
        -------
        float
        """
        return (
            1
            / m
            * np.log(1 + (np.exp(m) - 1) * 1 / (1 - h / depth) * np.exp(1 - 1 / (1 - h / depth)))
        )

    @staticmethod
    def _phi(m):
        """Compute phi from m

        Parameters
        ----------
        m: float

        Returns
        -------
        float

        """
        return np.exp(m) / (np.exp(m) - 1) - 1 / m

    @staticmethod
    def _gamma(m, h_D):
        """Compute gamma from m and h/D

        Parameters
        ----------
        m: float
        h_D: float

        Returns
        -------
        float
        """
        return np.log(1 + (np.exp(m) - 1) * (1 / (1 - h_D)) * np.exp(1 - 1 / (1 - h_D)))

    def compute_fit(self):
        """Compute the Probability Concept fit using lmfit and the object class attributes

        Returns
        -------

        """
        try:
            if self.use_measured_uncertainties_flag:
                self.fit_results = self.model.fit(
                    self.velocities,
                    self.parameters,
                    depth_i=self.depths,
                    weights=1 / self.uncertainties,
                )
            else:
                self.fit_results = self.model.fit(
                    self.velocities, self.parameters, depth_i=self.depths
                )
        except ValueError as err:
            self.fit_results = self.model.fit(self.velocities, self.parameters, depth_i=self.depths)
            print(
                f"There was a numerical issue with the model computation using uncertainties as weights. "
                f"Fitting model without uncertainties incorporated.\n"
                f"The error thrown by lmfit:\n    {err}"
            )
        self.m = self.fit_results.params["m"].value
        self.m_stderr = self.fit_results.params["m"].stderr

        self.h_D = self.h / self.max_depth
        self.usurf_umax = self.solve_usurf_umax_ratio(self.m, self.h, self.max_depth)

        self.phi = self._phi(self.m)
        if self.m_stderr is not None:
            self.phi_stderr = np.abs(self.phi - self._phi(self.m - self.m_stderr))
            self.gamma_stderr = np.abs(self.gamma - self._gamma(self.m - self.m_stderr, self.h_D))

        self.gamma = self._gamma(self.m, self.h_D)
        logging.info(f"gamma: {self.gamma:.3f} || std err: {self.gamma_stderr:.3f}")

        # Parse the results dataframe and reshape/modify to show what we want in
        # the velocity profile results table
        self.fit_results_df = br.tidy(
            self.fit_results
        )  # 3rd party method to clean up lmfit/scipy/optimize results dataframe
        df2 = {
            "name": "phi",
            "value": self.phi,
            "min": 0.0,
            "max": 1.0,
            "vary": True,
            "expr": np.nan,
            "stderr": self.phi_stderr,
            "init_value": np.nan,
        }
        self.fit_results_df = insert_row_in_dataframe(
            row_number=0, dataframe=self.fit_results_df, row_value=df2
        )
        self.fit_results_df["percent_error"] = np.nan
        for index, row in self.fit_results_df.iterrows():
            if not np.isnan(row["stderr"]):
                warnings.filterwarnings(
                    "ignore"
                )  # Sometimes will encounter a RuntimeWarning, does not affect program, safe to ignore
                percent_error = np.divide(row["stderr"], row["value"]) * 100
                warnings.filterwarnings("default")
            else:
                percent_error = np.nan
            self.fit_results_df.at[index, "percent_error"] = percent_error

        # Rename columns and make the fit results dataframe look as desired
        self.fit_results_df.rename(
            {
                "name": "Parameter",
                "value": "Value",
                "vary": "Param Fixed?",
                "stderr": "Std. Error",
                "percent_error": "% Error",
            },
            inplace=True,
            axis=1,
        )
        self.fit_results_df.replace(
            {
                "depth": "Total Depth",
                "max_velocity": "Max Velocity",
                "m": "M",
                "phi": "Φ",
            },
            inplace=True,
        )
        # logging.debug(self.fit_results.fit_report())
        # logging.debug('[[Surface Velocity Parameters]]')
        # logging.debug("    phi:           {:.8f} +/- {:.8f} ({:.2f}%)".format(self.phi, self.phi_stderr,
        # (self.phi_stderr/self.phi)*100))

    def compute_statistics(self):
        """Compute fit statistics

        Returns
        -------

        """
        alpha = 0.05  # 95% confidence interval
        n = len(self.velocities)  # number of data points
        p = len(self.fit_results.params)  # type: ignore[union-attr]
        dof = max(0, n - p)  # number of degrees of freedom
        tval = t.ppf(1.0 - alpha / 2.0, dof)
        if self.m_stderr is not None:
            sigma = self.m_stderr**0.5
            self.fit_95_uncertainty = sigma * tval

            # If we wanted, we can fit exactly to the input data and evaluate uncertainty
            # in one call, but since we wish to predict the fit through the data AND
            # to the boundaries (bed/surface) we have to do it manually. So this will remain
            # commented out.
            # self.fit_95_uncertainty = self.fit_results.eval_uncertainty(sigma=3)
        else:
            self.fit_95_uncertainty = np.nan

        # I am not sure if this is the correct way to compute the p-val. I am presuming that for
        # the chi-square, we only have 1 degree of freedom, since this model is only fitting M.
        self.fit_chisqprob_pval = chi2.sf(self.fit_results.chisqr, 1)  # type: ignore[union-attr]

    def compute_model(self):
        """Compute the modeled velocity profile using probability concept fit

        Returns
        -------

        """
        self.fit_depths = np.linspace(0, self.max_depth)
        self.fit_velocities = self.pc_function(
            self.fit_depths, self.max_velocity, self.m, self.max_depth, self.h
        )
        self.fit_velocities_95_ci_lower = self.pc_function(
            self.fit_depths,
            self.max_velocity,
            self.m - self.fit_95_uncertainty,
            self.max_depth,
            self.h,
        )
        self.fit_velocities_95_ci_upper = self.pc_function(
            self.fit_depths,
            self.max_velocity,
            self.m + self.fit_95_uncertainty,
            self.max_depth,
            self.h,
        )

        # Evaluate using best fit (this doesn't predict, just evals according to the
        # range of the data, therefore we don't use it. Left here, commented out
        # incase we decide we need to model uncertainty differently in the future.
        # self.fit_depths = self.depths
        # self.fit_velocities = self.fit_results.best_fit
        # self.fit_velocities_95_ci_lower = self.fit_results.best_fit - self.fit_95_uncertainty
        # self.fit_velocities_95_ci_upper = self.fit_results.best_fit + self.fit_95_uncertainty


def insert_row_in_dataframe(row_number, dataframe, row_value):
    """Insert row_value into dataframe at row_number.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Input dataframe.
    row_number : int
        Index position where the row should be inserted.
    row_value : list
        List of values to be inserted as a new row. Should have the same number of
        columns as the input dataframe.

    Returns
    -------
    pd.DataFrame
        The updated dataframe.

    Raises
    ------
    IndexError
        If row_number is greater than the number of rows in the dataframe.

    """

    if row_number > dataframe.shape[0]:
        raise IndexError(
            f"row_number ({row_number}) exceeds the number of rows in the dataframe ({dataframe.shape[0]})"
        )

    # Indexing
    start_upper = 0
    end_upper = row_number
    start_lower = row_number
    end_lower = dataframe.shape[0]

    # Create lists for the lower and upper half indices
    upper_half = [*range(start_upper, end_upper, 1)]
    lower_half = [*range(start_lower, end_lower, 1)]

    # Increment the value of lower half by 1
    lower_half = [x.__add__(1) for x in lower_half]

    # Combine the two lists and update index
    index_ = upper_half + lower_half
    dataframe.index = index_

    # Insert a row at the end and resort the index
    dataframe.loc[row_number] = row_value
    dataframe = dataframe.sort_index()

    return dataframe
