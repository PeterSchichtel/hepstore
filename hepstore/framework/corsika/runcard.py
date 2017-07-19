#!/usr/bin/enc python

def run( fcard, number=0, event_number=1, shower_number=1 ):
    fcard.write("RUNNR     %i                           run number                        \n" % number        )
    fcard.write("EVTNR     %i                           number of first shower event      \n" % event_number  )
    fcard.write("NSHOW     %i                           number of showers to generate     \n" % shower_number )
    pass

def primary( fcard, stackin=None, pid=14, e_start=1.0e+06, e_stop=1.0e+07, e_slope=-2.7 ):
    if stackin==None:
        fcard.write("PRMPAR    %i                         particle type of prim. particle   \n" % pid              )
        fcard.write("ESLOPE    %.1f                       slope of primary energy spectrum  \n" % e_slope          )
        fcard.write("ERANGE    %9.2e  %9.2e               energy range of primary particle  \n" % (e_start,e_stop) )
        pass
    else:
        fcard.write("INFILE    %s                                                              \n" % stackin       )
        pass
    pass

def geometry( fcard, theta_start=0.0, theta_stop=0.0, phi_start=-360., phi_stop=360., height=1.8e+06, chi=None ):
    fcard.write("THETAP    %.1f  %.1f                  range of zenith angle (degree)     \n" % (theta_start,theta_stop) )
    fcard.write("PHIP      %.1f  %.1f                  range of azimuth angle (degree)    \n" % (phi_start  ,phi_stop  ) )
    if chi:
        fcard.write("FIXCHI  %.1f                      starting altitude (g/cm**2) (* shouldnt be active with FIXHEI *) \n" % chi )
        pass
    else:
        fcard.write("FIXHEI    %9.2e   0                                                  \n" % height)
        pass
    pass

def seed( fcard, seed_1=10, seed_2=20, seed_3=30 ):
    fcard.write("SEED    %i   0   0                    seed for 1. random number sequence \n" % seed_1 )
    fcard.write("SEED    %i   0   0                    seed for 2. random number sequence \n" % seed_2 )
    fcard.write("SEED    %i   0   0                                                       \n" % seed_3 )
    pass

def observation_level( fcard, l0=1.0e+04, l1=1.0e+05, l2=1.5e+05, l3=2.0e+05, l4=2.5e+05, l5=5.0e+05, l6=7.5e+05, l7=10.0e+05, l8=12.5e+05, l9=15.0e+05 ):
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l0 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l1 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l2 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l3 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l4 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l5 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l6 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l7 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l8 )
    fcard.write("OBSLEV  %9.2e                       observation level (in cm) \n" % l9 )
    pass

def switches( fcard ):
    fcard.write("MAGNET  20.53   43.67                  magnetic field centr. Europe          \n")
    fcard.write("HADFLG  0  0  0  0  0  2               flags hadr.interact.&fragmentation    \n")
    fcard.write("ECUTS   0.3  0.2  0.003  0.003         energy cuts for particles             \n")
    fcard.write("THIN    1.E-4 1.E30 0.E0               thinning of particle output file      \n")
    fcard.write("*CASCADE T T T                                                               \n")
    fcard.write("MUADDI  T                              additional info for muons             \n")
    fcard.write("MUMULT  T                              muon multiple scattering angle        \n")
    fcard.write("ELMFLG  T   T                          em. interaction flags (NKG,EGS)       \n")
    fcard.write("STEPFC  1.0                            mult. scattering step length fact.    \n")
    fcard.write("RADNKG  200.E2                         outer radius for NKG lat.dens.distr.  \n")
    fcard.write("ARRANG  0.                             rotation of array to north            \n")
    fcard.write("LONGI   T   10.  F  T                  longit.distr. & step size & fit & out \n")
    fcard.write("ECTMAP  1.2345E9                       cut on gamma factor for printout      \n")
    fcard.write("MAXPRT  1                              max. number of printed events         \n")
    fcard.write("DIRECT  ' '                            output directory                      \n")
    pass


