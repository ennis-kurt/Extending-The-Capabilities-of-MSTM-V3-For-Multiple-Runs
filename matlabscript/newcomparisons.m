theta=[0:180]
theta=theta'
figure1= figure
%logp11= log10(P11)
%logs11=log10(S11avg) 
plot(theta,log10(S11avg5126398200045),theta,log10(par512_0640_200_004520_P11),'o',theta,log10(S11avg10246398200045),'k--',theta,log10(par1024_0640_200_004520_P11),'cx')
hold on
title('Phase Functions For x_m = 0.64, n_r = 2.0, n_i = 0.045')
legend('T-Matrix N = 512','Parametrization N = 512','T-Matrix N = 1024','Parameterization N = 1024')
hold off


figure2= figure
plot(theta,pol5126398200045,theta,parpol512_0640_200_004520,'o',theta,pol10246398200045,'k--',theta,parpol1024_0640_200_004520,'cx')
hold on
title('Linear Polarizations For x_m = 0.64, n_r = 2.0, n_i = 0.045' )
legend('T-Matrix N = 512','Parametrization N = 512','T-Matrix N = 1024','Parameterization N = 1024')
hold off

figure3= figure
%logp11= log10(P11)
%logs11=log10(S11avg) 
plot(theta,log10(S11avg512336020009),theta,log10(par512_0336_200_009000_P11),'o',theta,log10(S11avg512639820009),'k--',theta,log10(par512_0640_200_009000_P11),'cx')
hold on
title('Phase Functions For N = 512, n_r = 2.0, n_i = 0.09')
legend('T-Matrix x_m = 0.336','Parametrization x_m = 0.336','T-Matrixx_m = 0.64','Parameterization x_m = 0.64')
hold off


figure4= figure
plot(theta,pol512336020009,theta,parpol512_0336_200_009000,'o',theta,pol512639820009,'k--',theta,parpol512_0640_200_009000,'cx')
hold on
title('Linear Polarizations For N = 512, n_r = 2.0, n_i = 0.09' )
legend('T-Matrix x_m = 0.336','Parametrization x_m = 0.336','T-Matrixx_m = 0.64','Parameterization x_m = 0.64')
hold off


%%%%%%%%%%%%%%%%%%%%%%%%%%

% 512 064 2.0  Fig 5 & 6



figure5= figure
plot(theta,log10(S11avg51263982000226),theta,log10(par512_0640_200_002260_P11),'o',theta,log10(S11avg512639820009),'k--',theta,log10(par1024_0640_200_009000_P11),'cx')
hold on
title('Phase Functions For N = 512, x_m = 0.64, n_r = 2.0')
legend('T-Matrix n_i = 0.0226','Parametrization n_i = 0.0226','T-Matrix n_i = 0.09','Parameterization n_i = 0.09')
hold off


figure6= figure
plot(theta,pol51263982000226,theta,parpol512_0640_200_002260,'o',theta,pol512639820009,'k--',theta,parpol1024_0640_200_009000,'cx')
hold on
title('Linear Polarizations For N = 512, x_m = 0.64, n_r = 2.0' )
legend('T-Matrix n_i = 0.0226','Parametrization n_i = 0.0226','T-Matrix n_i = 0.09','Parameterization n_i = 0.09')
hold off

%%%%%%%%%%%%%%%%%%%%%%%%%%%%5

% 512 0.64 0.09

figure6= figure
plot(theta,log10(S11avg512639813009),theta,log10(par512_0640_130_009000_P11),'o',theta,log10(S11avg512639820009),'k--',theta,log10(par512_0640_200_009000_P11),'cx')
hold on
title('Phase Functions For N = 512 x_m = 0.64, n_i = 0.09')
legend('T-Matrix n_r = 1.3','Parametrization n_r = 1.3','T-Matrix n_r = 2.0','Parameterization n_r = 2.0')
hold off


figure7 = figure
plot(theta,pol512639813009,theta,parpol512_0640_130_009000,'o',theta,pol512639820009,'k--',theta,parpol512_0640_200_009000,'cx')
hold on
title('Linear Polarizations For N = 512 x_m = 0.64, n_i = 0.09' )
legend('T-Matrix n_r = 1.3','Parametrization n_r = 1.3','T-Matrix n_r = 2.0','Parameterization n_r = 2.0')
hold off


%%%%%%%%%%%%%%%%%%%%%%%%%5
% 512 0.64 0.0226



figure8= figure
plot(theta,log10(S11avg51263981300226),theta,log10(par512_0640_130_002260_P11),'o',theta,log10(S11avg51263982000226),'k--',theta,log10(par512_0640_200_002260_P11),'cx')
hold on
title('Phase Functions For N = 512 x_m = 0.64, n_i = 0.0226')
legend('T-Matrix n_r = 1.3','Parametrization n_r = 1.3','T-Matrix n_r = 2.0','Parameterization n_r = 2.0')
hold off


figure9 = figure
plot(theta,pol51263981300226,theta,parpol512_0640_130_002260,'o',theta,pol51263982000226,'k--',theta,parpol512_0640_200_002260,'cx')
hold on
title('Linear Polarizations For N = 512 x_m = 0.64, n_i = 0.0226' )
legend('T-Matrix n_r = 1.3','Parametrization n_r = 1.3','T-Matrix n_r = 2.0','Parameterization n_r = 2.0')
hold off
