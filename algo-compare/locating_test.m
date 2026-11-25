% %% 娴嬭瘯绋嬪簭
clear;
% filen=['D:\A1.鐩稿叧浠祫鏂橽1.娴嬭瘯鏁版嵁_2023\娴嬭瘯鎶ュ憡20240227.64\64.txt'];   
% filen='C:\Users\Administrator\Desktop\相关仪测试数据目录\测试报告20240801.4\4.txt';
filen=['D:\A1.相关仪资料\1.测试数据_2023\测试报告20240227.90\90.txt'];  
data=load(filen);
len=length(data);
vecA=data(1:len/2,1);
vecB=data(len/2+1:len,1);
fs =1000;
% t0=20;
% tc=2;
% vecA=data(1+t0*fs:(t0+tc)*fs,1);
% vecB=data(len/2+1+t0*fs:len/2+(t0+tc)*fs,1);
dis =319;%鍗曚綅m
velo = 1160;
dis2=0; velo2=0; dis3=0; velo3=0;
material='閾搁搧';
diamLow=200;
diamHigh=300;
currNum=1;
maxSnrIn=-1;
maxFreLowIn=100;
maxFreHighIn=450;
cutFreLow=100;
cutFreHigh=3000;
model=1;
[snr, disA, disB, correCoeff, corrCoeffVecAbs, disVec, maxFreLowOut, maxFreHighOut, flag, totalNum, timeDiff,t_data,t_als]=locating(vecB, vecA, fs, dis, velo,dis2, velo2, dis3, velo3, material, diamLow, diamHigh, currNum, maxSnrIn,maxFreLowIn, maxFreHighIn, cutFreLow, cutFreHigh,model);
%
%% 
%楠岃瘉鐭╅樀妯旱鍧愭爣鍚箟
[corval,corX] =max(corrCoeffVecAbs); 
disval=disVec(corX);
disA
disB
%%
%鐢诲浘
corrCoeffVecAbs1= fliplr(corrCoeffVecAbs);
figure,
subplot(211),plot(disVec,corrCoeffVecAbs),xlabel('距离/m'),ylabel('相关系数');
subplot(212),plot(disVec,corrCoeffVecAbs1),xlabel('距离/m'),ylabel('相关技术');title('相关曲线')