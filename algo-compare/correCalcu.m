function [SNR, disA, disB, coeff, corrCoeffVecAbs, disVec, timeDiff] =...
    correCalcu(data,   fs, freLow, freHigh, dis, velo, draw)

%1.参数赋值
VecA = data(1 : min(10*fs, length(data(:,1))), 1);
VecB = data(1 : min(10*fs, length(data(:,2))), 2); 
samInter = 1e6 / fs;%时域采集间隔，单位us
fmax = fs / 2; %信号最大有效频率
disA = -1;
disB = -1;
% freLow=10;
% freHigh=30;
% freLow=300;
% freHigh=2500;
%频域滤波
cutCoefLow = 0.8;
cutCoefHigh = 1.2;
% if freLow<=10 
%     rs=14;
% else if freLow<30
%         rs=14;
%     else
%     rs=27; 
%     end
% end

if draw == 1 || draw == 0
rs=22; %衰减分贝数
VecACut=bandp(VecA',freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,0.5,rs,fs);
% end
% VecACut=VecACut/max(VecACut);
VecBCut=bandp(VecB',freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,0.5,rs,fs);
% VecBCut=VecBCut/max(VecBCut);
VecA = VecACut';
% plot(VecA);
% hold on
% figure;
VecB = VecBCut';
timeDiff=0;
% plot(VecB);
%% test 滤波 
% N=fs;
% YVecACut=fft(VecACut);
% magVecACut=abs(YVecACut(1:1:N/2))*2/N; 
% f=(0:N/2-1)'*fs/N;  %分辨率fs/N=1/N*ts   
% figure;
% plot(f,magVecACut);
% 
%%
%4.计算
[corrCoeffVec, disVec] = calcuCorrCoeffVec(VecA, VecB, dis, velo, samInter);
corrCoeffVecAbs = abs(corrCoeffVec);
SNR = max(corrCoeffVecAbs) / mean(corrCoeffVecAbs);
coeff = max(corrCoeffVecAbs);

maxCoeffIndexVec = find(corrCoeffVecAbs==max(corrCoeffVecAbs));
if ~isempty(maxCoeffIndexVec) && length(disVec) >= maxCoeffIndexVec(1)
    disA = round(disVec(maxCoeffIndexVec(1))*100)/100;
    disB = dis - disA;
    timeDiff = (disA - disB) / velo; 
end
if draw == 1
% figure('NumberTitle', 'off', 'Name', '定位结果');
subplot(2,2,1)
plot(VecACut);
subplot(2,2,2)
plot(VecBCut);
subplot(2,2,3)
    bar(disVec, corrCoeffVecAbs);
    title(['距离左边', num2str(disA), '米，距离右边', num2str(disB),...
           '米；信噪比：', num2str(round(SNR * 10) /10), ...
           '，频段：', num2str(freLow), '-', num2str(freHigh), 'Hz']);
    % axis([-inf inf min(abs(corrCoeffVec)) inf])
       pause(0.01);
end
end

% if draw == 2
% % figure('NumberTitle', 'off', 'Name', '定位结果');
% % hold on
% subplot(2,2,1)
% plot(VecACut);
% subplot(2,2,2)
% plot(VecBCut);
% subplot(2,2,3)
%     bar(disVec, corrCoeffVecAbs);
%     title(['距离左边', num2str(disA), '米，距离右边', num2str(disB),...
%            '米；信噪比：', num2str(round(SNR * 10) /10), ...
%            '，频段：', num2str(freLow), '-', num2str(freHigh), 'Hz',' rs=', num2str(nnn)]);
%     % axis([-inf inf min(abs(corrCoeffVec)) inf])
%     pause(0.1);
% end
% if draw == 1
% % figure('NumberTitle', 'off', 'Name', '定位结果');
% subplot(2,2,1)
% plot(VecACut);
% subplot(2,2,2)
% plot(VecBCut);
% subplot(2,2,3)
%     bar(disVec, corrCoeffVecAbs);
%     title(['距离左边', num2str(disA), '米，距离右边', num2str(disB),...
%            '米；信噪比：', num2str(round(SNR * 10) /10), ...
%            '，频段：', num2str(freLow), '-', num2str(freHigh), 'Hz']);
%     % axis([-inf inf min(abs(corrCoeffVec)) inf])
% end


if draw == 2
for rs=20:40;
% for freLow=5:15;
nnn=rs;
VecACut=bandp(VecA',freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,0.5,rs,fs);
% end

% VecACut=VecACut/max(VecACut);
VecBCut=bandp(VecB',freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,0.5,rs,fs);
% VecBCut=VecBCut/max(VecBCut);
VecA = VecACut';
% plot(VecA);
% hold on
% figure;
VecB = VecBCut';
timeDiff=0;
% plot(VecB);
%% test 滤波 
% N=fs;
% YVecACut=fft(VecACut);
% magVecACut=abs(YVecACut(1:1:N/2))*2/N; 
% f=(0:N/2-1)'*fs/N;  %分辨率fs/N=1/N*ts   
% figure;
% plot(f,magVecACut);
% 
%%
%4.计算
[corrCoeffVec, disVec] = calcuCorrCoeffVec(VecA, VecB, dis, velo, samInter);
corrCoeffVecAbs = abs(corrCoeffVec);
SNR = max(corrCoeffVecAbs) / mean(corrCoeffVecAbs);
coeff = max(corrCoeffVecAbs);

maxCoeffIndexVec = find(corrCoeffVecAbs==max(corrCoeffVecAbs));
if ~isempty(maxCoeffIndexVec) && length(disVec) >= maxCoeffIndexVec(1)
    disA = round(disVec(maxCoeffIndexVec(1))*100)/100;
    disB = dis - disA;
    timeDiff = (disA - disB) / velo;
end

if draw == 2
% figure('NumberTitle', 'off', 'Name', '定位结果');
% hold on
subplot(2,2,1)
plot(VecACut);
subplot(2,2,2)
plot(VecBCut);
subplot(2,2,3)
    bar(disVec, corrCoeffVecAbs);
    title(['距离左边', num2str(disA), '米，距离右边', num2str(disB),...
           '米；信噪比：', num2str(round(SNR * 10) /10), ...
           '，频段：', num2str(freLow), '-', num2str(freHigh), 'Hz',' rs=', num2str(nnn)]);
    % axis([-inf inf min(abs(corrCoeffVec)) inf])
    pause(0.1);
end

% if draw == 1
% % figure('NumberTitle', 'off', 'Name', '定位结果');
% subplot(2,2,1)
% plot(VecACut);
% subplot(2,2,2)
% plot(VecBCut);
% subplot(2,2,3)
%     bar(disVec, corrCoeffVecAbs);
%     title(['距离左边', num2str(disA), '米，距离右边', num2str(disB),...
%            '米；信噪比：', num2str(round(SNR * 10) /10), ...
%            '，频段：', num2str(freLow), '-', num2str(freHigh), 'Hz']);
%     % axis([-inf inf min(abs(corrCoeffVec)) inf])
% end
end
end