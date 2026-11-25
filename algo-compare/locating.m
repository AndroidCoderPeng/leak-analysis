%调用端已有信息：dis, material, diamLow, diamHigh, velo
% function [snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec, maxFreLowOut, maxFreHighOut, flag, totalNum, timeDiff] = ...
%     locating(vecB, vecA, fs, dis, velo, material, diamLow, diamHigh, currNum, maxSnrIn, maxFreLowIn, maxFreHighIn)

% function [snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec, maxFreLowOut, maxFreHighOut, flag, totalNum, timeDiff] = ...
%     locating(numArgsOut, vecB, vecA, fs, dis, velo,dis2, velo2, dis3, velo3, material, diamLow, diamHigh, currNum, maxSnrIn,...
%     maxFreLowIn, maxFreHighIn, cutFreLow, cutFreHigh)
 
function [snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec, maxFreLowOut, maxFreHighOut, flag, totalNum, timeDiff,t_data,t_als] = ...
    locating( vecB, vecA, fs, dis, velo,dis2, velo2, dis3, velo3, material, diamLow, diamHigh, currNum, maxSnrIn,...
    maxFreLowIn, maxFreHighIn, cutFreLow, cutFreHigh,model)
tic
%%去信号直流偏置
% vecA=vecA-2.4;
% vecB=vecB-2.4;
%给信噪比、模式值赋初值，不会影响
t1=clock;
snr=0;
vecA=vecA-mean(vecA);
vecB=vecB-mean(vecB);
if isempty(model)
    model=1;
end
if length(vecA) ~= length(vecB)
    %初始默认值，如果两列数据长度不同，则各参数返回默认值。
    disA = -1;
    disB = -1;
    snr = -1;
    flag = -1;
    return;
end

data = zeros(length(vecA), 2);
data(:, 1) = vecA;
data(:, 2) = vecB;
% velo = 1500;  % 水听器  
% velo = getVelo(material, diamLow, diamHigh);%单位m/s //加速度计相关仪获取材料参数 

%1.参数赋值
if currNum == 1
    snrMax = 0;
    freLowMax = cutFreLow;
    freHighMax = cutFreHigh;%保证至少能计算一次corr
else
    snrMax = maxSnrIn;
    freLowMax = cutFreLow;
    freHighMax = cutFreHigh;
end

%2.频段列表  %找到相关系数最大的频率段
%%
if model==1
    FreList = xlsread('freList_modified.xlsx',2);  %3是低频更多，用于水听器，2是常规频率
else 
    FreList = xlsread('freList_modified.xlsx',3); 
end
freNum = length(FreList);
% totalNum = ceil(freNum/40);
totalNum = ceil(freNum/16);
if currNum > totalNum
    return; 
end
% % for m=(currNum-1)*40+1:min(currNum*40,freNum)
t2=clock;
for currNum=1:totalNum
 for m=(currNum-1)*16+1:min(currNum*16,freNum) %16个频率段一次循环，用于相关计算，搜索最大SNR处对应的上下限频率范围
    %筛选滤波列表
    freLow = FreList(m,1);
    freHigh= FreList(m,2);
    if freLow>freHigh||freHigh>fs/2||freHigh==fs/2||freLow==freHigh%只筛选异常情况
    continue;
    end
% [SNR, disA, disB, coeff, corrCoeffVecAbs, disVec] = correCalcu(data, fs, freLow, freHigh, dis, velo, draw)
% [snr0, ~, ~, ~, ~, ~, ~] = correCalcu(data, fs, freLow, freHigh, dis, velo, 0);
[snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec,timeDiff] = correCalcu(data, fs, freLow, freHigh, dis, velo,0);%draw=1画图 draw=2 rs循环测试
snr0=snr;%直接赋值就好，参数都是相同的，再次计算一遍snr没必要
    if  snr0 > snrMax
        snrMax = snr0;
        freLowMax = freLow; 
        freHighMax = freHigh;
    end
end %
end
t3=clock;
t_data=etime(t2,t1);
t_als=etime(t3,t2);
%[SNR, disA, disB, coeff, corrCoeffVecAbs, disVec, ~] = correCalcu(data, fs, freLow, freHigh, dis, velo, draw)
%最高信噪比的再计算一遍，输出参数
[snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec,timeDiff] = correCalcu(data, fs, freLowMax, freHighMax, dis, velo, 0);
maxFreLowOut = freLowMax;
maxFreHighOut = freHighMax;
% figure;
% plot(vecA);
% title(['A探头波形','    ','算法版本时间','2023年1月6日']);
% figure;
% plot(vecB)
% title(['B探头波形','    ','算法版本时间','2023年1月6日']);
if disA == -1 && disB == -1
    disA = -2;     
    disB = -2;
    snr = -2;
end
if snr >= 6 
    flag = 1;
else
    flag = 0;
end
toc  %程序运行时间计时