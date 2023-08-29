function des_space_single(EI2D, fidelity,low,high,firsteval,interval,lowB1,lowB2,upB,scenario)
EI2D=EI2D(1:fidelity,:);
EI2D_large = EI2D;
% EI2D=EI2D_large;
% length(EI2D)
idxei2 = EI2D(:, 3) < 0.9;
idyei2 = (EI2D(:, 2) < 3) | (EI2D(:, 2) > 10);
idxei3 = EI2D(:, 3) < 0.3;
idyei3 = EI2D(:, 2) > 10;
if scenario == 2
    idxei = idxei2;idyei = idyei2;
end
if scenario == 3
    idxei = idxei3;idyei = idyei3;
end
EI2D_large(idxei | idyei, :) = [];
fprintf("shape")
length(EI2D_large(:,1))

%% reconstruct design space
% close all
% Case I
figure
subplot(1,3,1)
des_contour(EI2D,firsteval,interval); xlim([1 15]);ylim([low*100 high*100]);caxis([lowB1 upB]);
title("\bf Design Space")

subplot(1,3,2)
des_contour(EI2D_large,firsteval/2,interval/2); caxis([lowB2 upB]);
title("\bf Target Region")
subplot(1,3,3)
scatdens(EI2D); caxis([0 2]);
title("\bf Sampling Density")
% tightfig
%% visualize exploration process

para_EI2D = EI2D(:,2:3);
% para_UCB2D = UCB2D(:,2:3);
obj_EI2D = EI2D(:,1);
% obj_UCB2D = UCB2D(:,1);
% obj = [obj_EI2D,obj_UCB2D];
%%
% close all
figure
% plot(obj_UCB2D, '-.o', 'LineWidth', 1, 'Color', 'b', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'k');hold on
subplot(2,1,1)
plot(obj_EI2D, '-.o', 'LineWidth', 1, 'Color', 'r', 'MarkerFaceColor', 'r', 'MarkerEdgeColor', 'k');
xlabel("Iterations")
ylabel("$\mathcal{N}_{\rm bio}$")
ylim([2e4 3.5e4])
addgradient;texadd;colorbar off; %ax = gca;ax.PlotBoxAspectRatio = [10,2,1];
% tightfig
% figure
% objj = boxchart(obj);box on; ax = gca;ax.PlotBoxAspectRatio = [2,3,1];
% texadd;colorbar off
% xlabels_tt = {'EI', 'UCB'};
% xticklabels(xlabels_tt);xlabel('Acquisition Function');ylabel('$\mathcal{N}_{\rm bio}$');tightfig
% figure
% subplot(2,1,1)
subplot(2,1,2)
imagesc([(para_EI2D(:,1)/max(para_EI2D(:,1))),(para_EI2D(:,2)/max(para_EI2D(:,2)))]')
caxis([0 1]);colormap bone;texadd;ax = gca;ax.PlotBoxAspectRatio = [3,1,1];
xlabel("Iterations");ylab_des = {'','$N_{\rm unit}$','','$\bar{\mathcal{D}}$',''};yticklabels(ylab_des)

% subplot(2,1,2)
% imagesc([(para_UCB2D(:,1)/max(para_UCB2D(:,1))),(para_UCB2D(:,2)/max(para_UCB2D(:,2)))]')
% caxis([0 1]);colormap jet;texadd;ax = gca;ax.PlotBoxAspectRatio = [3,1,1];
% xlabel("Iterations");yticklabels(ylab_des)
end