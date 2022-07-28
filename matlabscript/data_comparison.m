%1024 

figure1= figure
plot(theta,pol_tm512639820009,theta,parpol512_0640_200_009000,'o',theta,pol_tm1024639820009,'k--',theta,parpol1024_0640_200_009000,'cx')
hold on
title('Linear Polarizations For x_m = 0.64, n_r = 2.0, n_i = 0.09' )
legend('T-Matrix N = 512','Parametrization N = 512','T-Matrix N = 1024','Parameterization N = 1024')
hold off

%%%%%%%%%%%%%%%%%% error  %%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%% Polarization %%%%%%%%%%%%
figure2= figure
errpol_1024639820009 = pol_tm1024639820009 - parpol1024_0640_200_009000
plot(theta, errpol_1024639820009)
hold on

errpol_512639820009 = pol_tm512639820009 - parpol512_0640_200_009000
plot(theta, errpol_512639820009)

%errorserror= errpol_1024639820009 -errpol_512639820009

%plot(theta,errorserror)

%256
errpol_256639820009 = (pol_tm256639820009 - parpol256_0640_200_009000)
plot(theta, errpol_256639820009)


%128
errpol_128639820009 = pol_tm128639820009 - parpol128_0640_200_009000
plot(theta, errpol_128639820009)


title('Linear Polarizations Comparison x_m = 0.64, n_r = 2.0, n_i = 0.09' )
legend('err1024(tm1024 - par1024)','err512(tm512 - par512)','err256(tm256-par256)','err128(tm128 - par128)')

%relative error

% figure3= figure
% relerrpol_1024639820009 = (pol_tm1024639820009 - parpol1024_0640_200_009000)./pol_tm1024639820009
% plot(theta, relerrpol_1024639820009)
% hold on
% 
% relerrpol_512639820009 = (pol_tm512639820009 - parpol512_0640_200_009000)./pol_tm512639820009
% plot(theta, relerrpol_512639820009)
% 
% 
% %256
% %relerrpol_256639820009 = (pol_tm256639820009 - parpol256_0640_200_009000)./pol_tm256639820009
% %plot(theta, relerrpol_256639820009)
% 
% %128
% relerrpol_128639820009 = (pol_tm128639820009 - parpol128_0640_200_009000)./pol_tm128639820009
% plot(theta, relerrpol_128639820009)
% 
% 




% title('Linear Polarizations Comparison x_m = 0.64, n_r = 2.0, n_i = 0.09' )
% legend('Rel-err1024','Rel-err512','Rel-err256','Rel-err128')
%

%%%%%%%%%%%%% Phase %%%%%%%%%%%%%%%%%%%

figure4=figure


errphs_1024639820009 = S11avg1024639820009 - par1024_0640_200_009000_P11
plot(theta, (errphs_1024639820009))
hold on

errphs_512639820009 = S11avg512639820009 - par512_0640_200_009000_P11
plot(theta, errphs_512639820009)

%errorserror= errpol_1024639820009 -errpol_512639820009

%plot(theta,errorserror)

%256
errphs_256639820009 = S11avg256639820009 - par256_0640_200_009000_P11
plot(theta, errphs_256639820009)


%128
errphs_128639820009 = S11avg128639820009 - par128_0640_200_009000_P11
plot(theta, errphs_128639820009)
legend('err1024(tm1024 - par1024)','err512(tm512 - par512)','err256(tm256 - par256)','err128(tm128 - par128)')
title('Phase Function P11 Comparison x_m = 0.64, n_r = 2.0, n_i = 0.09' )



%%%%%%%%%%%%%%%%%%%% partial functions %%%%%%%%%%%%%%%%
%%%%%%%%%%%%% Polarization %%%%%%%%%%%%
theta_90=(0:90)
figure5= figure
forerrpol_1024639820009 = pol_tm1024639820009 - parpol1024_0640_200_009000
%f= fit
plot(theta_90, forerrpol_1024639820009(1:91))
hold on

forerrpol_512639820009 = pol_tm512639820009 - parpol512_0640_200_009000
plot(theta_90, forerrpol_512639820009(1:91))

%errorserror= forerrpol_1024639820009 -forerrpol_512639820009

%plot(theta,errorserror)

%256
forerrpol_256639820009 = (pol_tm256639820009 - parpol256_0640_200_009000)
plot(theta_90, forerrpol_256639820009(1:91))


%128
forerrpol_128639820009 = pol_tm128639820009 - parpol128_0640_200_009000
plot(theta_90, forerrpol_128639820009(1:91))


title('Linear Polarizations Comparison x_m = 0.64, n_r = 2.0, n_i = 0.09' )
legend('err1024(tm1024 - par1024)','err512(tm512 - par512)','err256(tm256-par256)','err128(tm128 - par128)')


% P22 comparisons

figure5=figure


errphs2_1024639820009 = S22avg1024639820009 - par1024_0640_200_009000_P22
plot(theta, (errphs2_1024639820009))
hold on

errphs2_512639820009 = S22avg512639820009 - par512_0640_200_009000_P22
plot(theta, errphs2_512639820009)

%errorserror= errpol_1024639820009 -errpol_512639820009

%plot(theta,errorserror)

%256
errphs2_256639820009 = S22avg256639820009 - par256_0640_200_009000_P22
plot(theta, errphs2_256639820009)


%128
errphs2_128639820009 = S22avg128639820009 - par128_0640_200_009000_P22
plot(theta, errphs2_128639820009)
legend('err1024(tm1024 - par1024)','err512(tm512 - par512)','err256(tm256 - par256)','err128(tm128 - par128)')
title('Phase Function P22 Comparison x_m = 0.64, n_r = 2.0, n_i = 0.09' )


figure6=figure
subplot(2,2,1)
plot(theta,S22avg1024639820009.*S11avg1024639820009,theta,par1024_0640_200_009000_P22)
hold on
legend('tm','par')
title('Comparison of P22 for N=1024')
subplot(2,2,2)
plot(theta,S22avg512639820009.*S11avg512639820009,theta,par512_0640_200_009000_P22)
legend('tm','par')
title('512')
subplot(2,2,3)
plot(theta,S22avg256639820009.*S11avg256639820009,theta,par256_0640_200_009000_P22)
legend('tm','par')
title('256')
subplot(2,2,4)
plot(theta,S22avg128639820009.*S11avg128639820009,theta,par128_0640_200_009000_P22)
legend('tm','par')
title('128')


