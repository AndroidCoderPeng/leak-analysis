% %% 测试程序
% vecA1 = xlsread('3.xlsx',1);
% vecB2 = xlsread('3.xlsx',2);
% fs = 7500;
% freLow = 200;
% freHigh = 1100;
% dis = 97.5;%单位m
% velo = 1190;
% [SNR, disA, disB, coeff, corrCoeffVecAbs, disVec , timeDiff] = typicalFreInter(7, vecA, vecB, fs, freLow, freHigh, dis, velo);
% %%   

% 4.2	选定滤波器后，要调用的算法接口
function [SNR, disA, disB, coeff, corrCoeffVecAbs, disVec, timeDiff] = typicalFreInter(vecA, vecB, fs, freLow, freHigh, dis, velo)

data = zeros(length(vecA), 2);
data(:, 1) = vecA;
data(:, 2) = vecB;
[SNR, disA, disB, coeff, corrCoeffVecAbs, disVec, timeDiff] = correCalcu(data, fs, freLow, freHigh, dis, velo, 0);