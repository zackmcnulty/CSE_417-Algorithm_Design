close all; clear all; clc;

data = csvread('~/Desktop/CSE/417/hw/hw7/results2.txt',1, 0);

N = data(:, 1);

total_time = data(:,2);
nuss_time = data(:,3);
trace_time = data(:,4);

%%

figure (1)
subplot(122);
plot(N, total_time, 'r.'), hold on;
coeffs = polyfit(N, total_time, 3);
fit = polyval(coeffs, N);
plot(N, fit, 'b--')
title("Total Runtime")
xlabel('Input (N)')
ylabel('Runtime (sec)')
legend({'Data', 'O(n^3) fit'})
set(gca, 'fontsize', 15)

subplot(223);
plot(N, nuss_time, 'r.'), hold on;
title("Nussinov Runtime")
xlabel('Input (N)')
ylabel('Runtime (sec)')
coeffs = polyfit(N, nuss_time, 3);
fit = polyval(coeffs, N);
plot(N, fit, 'b--')
legend({'Data', 'O(n^3) fit'})
set(gca, 'fontsize', 15)

subplot(221);
plot(N, trace_time, 'r.'), hold on;
title("traceback Runtime")
xlabel('Input (N)')
ylabel('Runtime (sec)')
coeffs = polyfit(N, trace_time, 1);
fit = polyval(coeffs, N);
plot(N, fit, 'b--')
legend({'Data', 'O(n) fit'})
set(gca, 'fontsize', 15)
