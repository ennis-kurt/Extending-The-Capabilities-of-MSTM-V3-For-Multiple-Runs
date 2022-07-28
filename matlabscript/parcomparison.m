theta=[0:180]
theta=theta'


figure1 = figure
plot(theta,S11avg10246398171045,theta,par1024_0640_171_004500_P11,'o')
hold on
title('Phase Functions For N = 1024, n_r = 1.71, n_i = 0.045' )
legend('T-Matrix','Parametrization')
hold off

figure2= figure
plot(theta,pol10246398171045,theta,parpol1024_0640_171_004500,'o')
hold on
title('Linear Polarizations - Parametrization ' )
legend('1024\_0.64\_1.3\_.0226','1024\_0.64\_1.3\_.09')

hold off

