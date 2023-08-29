 h = colorbar;
h.Label.Interpreter = 'latex';
% h.Label.String = '$z$';
h.FontName = 'LaTeX';
h.TickLabelInterpreter = 'latex';
set(0,'DefaultTextFontSize',25,'DefaultAxesFontSize',16)
set(0,'DefaultTextInterpreter','latex')
set(gca, 'TickLabelInterpreter', 'latex')
set(gca,'FontName','latex')