# Fitting Functions
#### 1. Legendre Polynomials to model angular depnedency
There are numbers of different ways to generate Legendre polynomials. See the related articles in __wikipedia__ and __Wolframalpha__

$$\mathbf{1.}\; \; P_n(x) = \frac{1}{2^n n!} \frac{d^n}{dx^n} \left(x^2 -1\right)^n $$
 This above form is the most compact representation. It's called Rodrigues Formula


$$
P_n(x)= \frac{1}{2^n} \sum_{k=0}^n \binom{n}{k}^2 (x-1)^{n-k}(x+1)^k \\
P_n(x)=\sum_{k=0}^n \binom{n}{k} \binom{n+k}{k} \left( \frac{x-1}{2} \right)^k, \\
P_n(x)=\frac1{2^n}\sum_{k=0}^{[\frac n2]}(-1)^k\binom nk\binom{2n-2k}n x^{n-2k},\\
P_n(x)= 2^n \sum_{k=0}^n x^k \binom{n}{k} \binom{\frac{n+k-1}{2}}{n}
$$

But the easiest way to drive them is using Bonnet's recursive formula given below:

$$(n+1) P_{n+1}(x) = (2n+1) x P_n(x) - n P_{n-1}(x)$$

|n| $P_n(x)$|
|-|-|
|0|  1 |
 |1| X |
 |2|  $ \tfrac12 (3x^2-1)$ |
 |3| $\tfrac12 \left(5x^3-3x\right)$|
 |4| $\tfrac18 \left(35x^4-30x^2+3\right)$|

#### 2. Regular Polynomials to fit Coefficients of Legendre Polynomials

Legendre Polynomials are used to fit the angular distribution of the phase functions. Although all the phase functions for each parameter of choice can be fitted with a similar functions, the curve fitted varies slightly with the different values of the N, ni, nr and sp. See the Fig1. In this fig1 it is shown that curve has the same shape. However, a few times the curves shape changes which implies the change in sign on one or more of its coefficients in the fitted model. In figure 6 it is evident that the changes in sign of the coefficients are associated with the change in single scattering regime of these particle which can be further related to physical nature of the scattering by fractal aggregates. I discuss the relationship of these parameter regimes to physical nature of the problem in section 2. 

 Since the shape of the curve does not change significantly, with a careful analyzes it is possible to find a relationship between the coefficients of the legendre polynomials as a function of the physical paramaters of the aerosol.
