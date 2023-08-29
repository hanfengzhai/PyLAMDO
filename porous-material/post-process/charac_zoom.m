function charac_zoom(charac_n,charac_r,r_list,UCB2D,r_bench, n_bench,test_n,test_r,n_test,r_test)
% charac_n = [30925.0,30717.0,30868.0,31108.0,31142.0,31292.0,31088.0,31151.0,31214.0,31277.0,31086.0,31099.0,31074.0,31188.0,31161.0];
% charac_r = [0.0,0.0,19703.0,29450.0,29920.0,30173.0,30562.0,30903.0,31161.0];
n_list = 1:15;
% r_list = 0.1:0.1:0.9;
% close all
%%
figure
subplot(2,1,1)
plot(n_list, test_n, '-.', 'Color', 'k', 'LineWidth', 2);hold on; 
plot(n_list, charac_n, '-.', 'Color', 'k', 'LineWidth', 2);
plot(n_list, test_n, 'o', 'MarkerFaceColor', [0.5 0.5 0.5], 'MarkerEdgeColor', 'k', 'LineWidth', 2,'MarkerSize', 10);
plot(n_list, charac_n, 'o', 'MarkerFaceColor', 'b', 'MarkerEdgeColor', 'k', 'LineWidth', 2,'MarkerSize', 10);

xlim([1 15])
texadd; ax = gca;ax.PlotBoxAspectRatio = [3,1,1];colorbar off;%addgradient; 
% xlabel("$N_{\rm unit}$"); ylabel("$\mathcal{N}_{\rm bio}$"); 

subplot(2,1,2)
plot(r_list, test_r, '-.', 'Color', 'k', 'LineWidth', 2);hold on; 
plot(r_list, charac_r, '-.', 'Color', 'k', 'LineWidth', 2);
plot(r_list, test_r, 'o', 'MarkerFaceColor', [0.5 0.5 0.5], 'MarkerEdgeColor', 'k', 'LineWidth', 2,'MarkerSize', 10);
plot(r_list, charac_r, 'o', 'MarkerFaceColor', 'r', 'MarkerEdgeColor', 'k', 'LineWidth', 2,'MarkerSize', 10);

xlim([min(r_list), max(r_list)])
texadd; ax = gca;ax.PlotBoxAspectRatio = [3,1,1];colorbar off;%addgradient; 
% xlabel("$\bar{\mathcal{D}}$"); ylabel("$\mathcal{N}_{\rm bio}$");
end

