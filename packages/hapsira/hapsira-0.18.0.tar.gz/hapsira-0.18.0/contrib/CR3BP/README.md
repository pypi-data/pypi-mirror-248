# Circular Restricted Three-Body Problem (CR3BP) Package

## Currently Implemented Functionality
- natural dynamics propagation
- dynamics + State-Transition-Matrix propagation
- compute characteristic values of CR3BP
- a test file with 4 differnt orbit types propagated and STM
   - Lunar Gateway station NRHO
   - Distant Retrograde Orbit
   - Butterfly Orbit
   - Vertical Lyapanov Orbit

## Functionality Left To Implement
- CR3BP rotating to inertial frame convertion
- inertial to CR3BP rotating frame convertion
- convertion to and from Ephemeris frame with SPICE API
- differential correction methods (single/multiple shooting)
- compute periodic orbits with initial guess
- analytical approximate solutions (first order/third order) for orbits like Halo and Lyapanov
- analytical computation of eigenvalues / eigenvectors of Monodromy matrix and stability of orbits
- stable and unstable manifold estimation

## Functionality I Required Help With
- Integration of code with astropy constants and units without breaking JIT Compilation
- Integration of ploting with existing hapsira interactive plotter (currently in the test file I use matplotlib and mplot3d)

## About Me
I am Kevin, a Space Engineering graduate from Politecnico di Milano. I love working with mission design, flight dynamics and simulations. Most of my work was done with MATLAB and I have some experience with C++, but I am quite a noob with Python. So in case you find any error in my implementation, discussion of new functionality to add and improvement to my code, feel free to contact me through my email.
- email : kevincharls.work@gmail.com
