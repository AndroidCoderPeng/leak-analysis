 %% 娴嬭瘯绋嬪簭
clear all;
%%
% filen=['C:\Users\Administrator\Desktop\相关仪测试数据目录\Locate\测试报告20240621.18\18.txt'];  
filen=['D:\A1.相关仪资料\1.测试数据_2023\测试报告20240905.25\25.txt'];  
data=load(filen);
len=length(data);
vecA=data(1:len/2,1);
vecB=data(len/2+1:len,1);
plot(vecA)
%%
%闇?妫?煡鐨勫弬鏁拌緭鍏?
fs = 7500;
Fs=fs;
dis = 209;%鍗曚綅m
cutFreLow=10;%杈撳叆鐨勯珮浣庨棰戠巼
cutFreHigh=fs/2;
%% 
freLow = 100;%鍙槸璧嬪垵鍊?
freHigh = 3000;
velo = 1160;
dis2=0; velo2=0; dis3=0; velo3=0;
material='铁';
diamLow=200;
diamHigh=300;
currNum=1;
maxSnrIn=-1;
samInter = 1e6 / fs;%鏃跺煙閲囬泦闂撮殧锛屽崟浣島s
result=[];
%%?
tic
snr=0;
vecA=vecA-mean(vecA);
vecB=vecB-mean(vecB);
if length(vecA) ~= length(vecB)
    disA = -1;
    disB = -1;
    snr = -1;
    flag = -1;
    return;
end
 
data = zeros(length(vecA), 2);
data(:, 1) = vecA;
data(:, 2) = vecB;

%1.鍙傛暟璧嬪?
if currNum == 1
    snrMax = 0;
    freLowMax = cutFreLow;
    freHighMax = cutFreHigh;%淇濊瘉鑷冲皯鑳借绠椾竴娆orr
else
    snrMax = maxSnrIn;
    freLowMax = cutFreLow;
    freHighMax = cutFreHigh;
end

%2.棰戞鍒楄〃  %鎵惧埌鐩稿叧绯绘暟鏈?ぇ鐨勯鐜囨
%%
FreList = xlsread('freList_modified.xlsx',2);  %3鏄綆棰戞洿澶氾紝鐢ㄤ簬姘村惉鍣紝2鏄父瑙勯鐜?
freNum = length(FreList);
totalNum = ceil(freNum/16);
if currNum > totalNum
    return; 
end
% for m=(currNum-1)*40+1:min(currNum*40,freNum)
for currNum=1:totalNum
for m=(currNum-1)*16+1:min(currNum*16,freNum) 
    freLow = FreList(m,1);
    freHigh= FreList(m,2);
%     if m>1&&(freLow<cutFreLow||freHigh>cutFreHigh||freHigh==cutFreHigh)
%     continue;
%     end
%%
%butter滤波
% N1   = 10;   % Order
% Fc1 = freLow;   % First Cutoff Frequency
% Fc2 = freHigh;  % Second Cutoff Frequency
% h  = fdesign.bandpass('N,F3dB1,F3dB2', N1, Fc1, Fc2, Fs);
% Hd = design(h, 'butter');
% VecA=filter(Hd,data(:, 1));
% VecB=filter(Hd,data(:, 2));
%原先滤波
cutCoefLow = 0.8;
cutCoefHigh = 1.2;
rs=40;
VecA=bandp(data(:, 1),freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,1,rs,fs);
VecB=bandp(data(:, 2),freLow,freHigh,freLow*cutCoefLow,freHigh*cutCoefHigh,1,rs,fs);
%%
N=length(VecA);
t=0:1/Fs:(N-1)/Fs;
y0 =2*(abs(fft(VecA))/N); %蹇?鍌呴噷鍙跺彉鎹㈢殑骞呭?
y1= 2*(abs(fft(VecB))/N);
f=(0:N-1)*Fs/N;
fmax=fs/2;
%%
[corrCoeffVec, disVec] = calcuCorrCoeffVec(VecA, VecB, dis, velo, samInter);
corrCoeffVecAbs = abs(corrCoeffVec);
snr = max(corrCoeffVecAbs) / mean(corrCoeffVecAbs);%淇″櫔姣旀槸鏈?ぇ鐨勭浉鍏崇郴鏁伴櫎骞冲潎鐩稿叧绯绘暟
coeff = max(corrCoeffVecAbs);
snr_radio=max(corrCoeffVecAbs) / mean(corrCoeffVecAbs);
maxCoeffIndexVec = find(corrCoeffVecAbs==max(corrCoeffVecAbs));
if ~isempty(maxCoeffIndexVec) && length(disVec) >= maxCoeffIndexVec(1)
    disA = round(disVec(maxCoeffIndexVec(1))*100)/100;%杩欓噷鏄繚鐣欎袱浣嶆湁鏁堟暟瀛?
    disB = dis - disA;
    timeDiff = (disA - disB) / velo;
end
snr0=snr;
result(m,:)=[freLow,freHigh,snr,coeff,disA,disB];%存数据
    if  snr0 > snrMax
        snrMax = snr0;
        freLowMax = freLow; 
        freHighMax = freHigh;
    end
%% 鐢诲浘璞?
figure,
subplot(231),plot(t,VecA);
title(['Original Signal',num2str(freLow),'-',num2str(freHigh),':A']);
xlabel('Time'); 
ylabel('Amplitude'); 
subplot(232),plot(t,VecB);
title(['Original Signal',num2str(freLow),'-',num2str(freHigh),':B']);
xlabel('Time'); 
ylabel('Amplitude'); 
subplot(233),plot(f(1:N/2),y0(1:N/2));
titlen=['Frequency Signal-A'];
title(titlen);
xlabel('Frequency'); 
ylabel('Amplitude');
axis([0,fmax,-inf,inf]);
subplot(234),plot(f(1:N/2),y1(1:N/2));
titlen=['Frequency Signal-B'];
title(titlen);
xlabel('Frequency'); 
ylabel('Amplitude');
axis([0,fmax,-inf,inf]);
subplot(235),plot(disVec,corrCoeffVecAbs);
end %
end

%%
%鍑芥暟缁撴潫
%% 
%楠岃瘉鐭╅樀妯旱鍧愭爣鍚箟
[corval,corX] =max(corrCoeffVecAbs); 
disval=disVec(corX);
%鏄剧ず鍒囨瘮闆か璁＄畻鐨?
[snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec,timeDiff] = correCalcu(data, fs, freLowMax, freHighMax, dis, velo, 0);
maxFreLowOut = freLowMax;
maxFreHighOut = freHighMax;
freLowMax
freHighMax
disA
disB

%%
%鐢诲浘
corrCoeffVecAbs1= fliplr(corrCoeffVecAbs);
%鐪熸鏄剧ず鏃讹紝鏄弽杩囨潵鐨?
figure,
subplot(211),plot(disVec,corrCoeffVecAbs),xlabel('距离/m'),ylabel('相关系数');title('定位结果'); axis([0,dis,-inf,inf]);
subplot(212),plot(disVec,corrCoeffVecAbs1),xlabel('距离/m'),ylabel('相关系数');title('定位结果')
pause(3);
close all;
%% 画一个频谱对比图
N=length(data(:, 1));
t=0:1/Fs:(N-1)/Fs;
y_Ao =2*(abs(fft(data(:, 1)))/N); %蹇?鍌呴噷鍙跺彉鎹㈢殑骞呭?
y_Bo= 2*(abs(fft(data(:, 2)))/N);
f=(0:N-1)*Fs/N;
fmax=fs/2;
figure,
subplot(231),plot(t,data(:, 1));
title(['Original Signal',num2str(freLow),'-',num2str(freHigh),':A']);
xlabel('Time'); 
ylabel('Amplitude'); 
subplot(232),plot(t,data(:, 2));
title(['Original Signal',num2str(freLow),'-',num2str(freHigh),':B']);
xlabel('Time'); 
ylabel('Amplitude'); 
subplot(233),plot(f(1:N/2),y_Ao(1:N/2));
titlen=['Frequency Signal-A-original'];
title(titlen);
xlabel('Frequency'); 
ylabel('Amplitude');
axis([0,fmax,-inf,inf]);
subplot(234),plot(f(1:N/2),y_Bo(1:N/2));
titlen=['Frequency Signal-B_original'];
title(titlen);
xlabel('Frequency'); 
ylabel('Amplitude');
axis([0,fmax,-inf,inf]);
subplot(235),plot(disVec,corrCoeffVecAbs);