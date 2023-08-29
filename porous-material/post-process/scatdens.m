function scatdens(variab)

    x = int32(round(variab(:,2))); x = double(x);
    y = variab(:,3)*100;
    % scatter(X,Y);
    % 
    % % Compute probability density function using ksdensity
    % % [f, xi, yi] = ksdensity([X Y]);
    % [fff, xi, yi] = ksdensity([X Y], 'Support', [-4 4 -4 4], 'NumPoints', [100 100]);
    % 
    % 
    % % Create contour plot of density function
    % contourf(xi,yi,fff);
    % Generate some example data
% x = randn(1000,1);
% y = randn(1000,1);

% Compute the 2D histogram of the data
    [N,edges] = hist3([x y], [20 20]);
    
    % Normalize the histogram to estimate the PDF
    f = (N'./sum(N(:)))*100;
    
    % Plot the density distribution using contourf
    xgrid = edges{1};
    ygrid = edges{2};
    contourf(xgrid, ygrid, f,'LineStyle', 'none', 'LevelStep', 0.01); hold on
    colorbar
    h = colorbar;
    h.Label.Interpreter = 'latex';
    % h.Label.String = '$z$';
    h.FontName = 'LaTeX';
    h.TickLabelInterpreter = 'latex';

    % caxis([0 2e-3])
    xlabel('$N_{\rm unit}$');
    ylabel('$\bar{\mathcal{D}}$');
    colormap jet
    h = colorbar;
    h.Label.Interpreter = 'latex';
    % h.Label.String = '$z$';
    h.FontName = 'LaTeX';
    h.TickLabelInterpreter = 'latex';
    set(0,'DefaultTextFontSize',25,'DefaultAxesFontSize',16)
    set(0,'DefaultTextInterpreter','latex')
    set(gca, 'TickLabelInterpreter', 'latex')
    set(gca,'FontName','latex')
    ax = gca;ax.PlotBoxAspectRatio = [1,1,1];
end