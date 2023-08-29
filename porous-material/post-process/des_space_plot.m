function des_space_plot(EI2D, UCB2D,fidelity)
EI2D=EI2D(1:fidelity,:);UCB2D=UCB2D(1:fidelity,:);
EI2D_large = EI2D; UCB2D_large = UCB2D; 
idxei = EI2D(:, 3) < 0.5;idxucb = UCB2D(:, 3) < 0.5;
EI2D_large(idxei, :) = [];UCB2D_large(idxucb, :) = [];

%% reconstruct design space
% close all
% Case I
figure
subplot(2,3,1)
des_contour(EI2D); xlim([1 15]);ylim([10 90]);
title("\bf Design Space")
subplot(2,3,4)
des_contour(UCB2D); xlim([1 15]);ylim([10 90]);
title("\bf Design Space")
subplot(2,3,2)
des_contour(EI2D_large); caxis([0.95 1]);
title("\bf Target Region")
subplot(2,3,5)
des_contour(UCB2D_large); caxis([0.95 1]); 
title("\bf Target Region")
subplot(2,3,3)
scatdens(UCB2D);caxis([0 2]);  
title("\bf Sampling Density")
subplot(2,3,6)
scatdens(EI2D); caxis([0 2]);
title("\bf Sampling Density")
% tightfig
%% visualize exploration process

para_EI2D = EI2D(:,2:3);
para_UCB2D = UCB2D(:,2:3);
obj_EI2D = EI2D(:,1);
obj_UCB2D = UCB2D(:,1);
obj = [obj_EI2D,obj_UCB2D];
%%
% close all
figure
plot(obj_UCB2D, '-.o', 'LineWidth', 1, 'Color', 'b', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'k');hold on
plot(obj_EI2D, '-.o', 'LineWidth', 1, 'Color', 'r', 'MarkerFaceColor', 'r', 'MarkerEdgeColor', 'k');
xlabel("Iterations")
ylabel("$\mathcal{N}_{\rm bio}$")
ylim([2e4 3.5e4])
addgradient;texadd;colorbar off; ax = gca;ax.PlotBoxAspectRatio = [10,2,1];
tightfig
figure
objj = boxchart(obj);box on; ax = gca;ax.PlotBoxAspectRatio = [2,3,1];
texadd;colorbar off
xlabels_tt = {'EI', 'UCB'};
xticklabels(xlabels_tt);xlabel('Acquisition Function');ylabel('$\mathcal{N}_{\rm bio}$');tightfig
figure
subplot(2,1,1)
imagesc([(para_EI2D(:,1)/max(para_EI2D(:,1))),(para_EI2D(:,2)/max(para_EI2D(:,2)))]')
caxis([0 1]);colormap bone;texadd;ax = gca;ax.PlotBoxAspectRatio = [3,1,1];
xlabel("Iterations");ylab_des = {'','$N_{\rm unit}$','','$\bar{\mathcal{D}}$',''};yticklabels(ylab_des)

subplot(2,1,2)
imagesc([(para_UCB2D(:,1)/max(para_UCB2D(:,1))),(para_UCB2D(:,2)/max(para_UCB2D(:,2)))]')
caxis([0 1]);colormap bone;texadd;ax = gca;ax.PlotBoxAspectRatio = [3,1,1];
xlabel("Iterations");yticklabels(ylab_des)
end