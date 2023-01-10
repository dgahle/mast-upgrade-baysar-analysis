# Simple C II Analysis

The emission of a C II line ($\epsilon$) can be modelled by the following equations. 

$$ \epsilon = \frac{1}{4\pi} \int c_z TEC(n_e, T_e, \tau_z)\ dl $$

$$  TEC_{z, ij}(n_e, T_e, \tau_z) = n_e^2 \(f_z PEC_{ij}^{exc} + f_{z+1} PEC_{ij}^{rec}\) $$

Where $c_z$ is the impurity (carbon) concentration, $TEC$ is the _Total Emission Coefficient_, $n_e$ is the electron 
density, $T_e$ is the electron temperature, $\tau_z$ is the impurity residence time (a proxy for impurity transport), 
$f_{z, z+1}$ is the fractional abundance of the $z$ and $z+1$ charge states, and PEC_{ij}^{exc, rec} is the _Photon 
Emission Coefficient_ for the electronic transition from level $i$ to $j$ for excitation and recombination respectively.     

A simple analysis to infer the carbon concentration, $c_z$, from a single C II line can be done by making a series of 
assumptions:

1. Impurity transport is negligible 

